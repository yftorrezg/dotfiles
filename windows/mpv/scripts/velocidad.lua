-- velocidad.lua — control de velocidad con visor fijo en pantalla.
--
--   ] / [        +0.1 / -0.1
--   } / {        +0.5 / -0.5
--   Retroceso    volver a 1.0x
--   Ctrl+v       mostrar u ocultar el visor fijo de velocidad
--
-- El visor queda fijo en la esquina superior derecha mientras la velocidad no
-- sea 1.0x. La última velocidad usada se recuerda para el próximo video, aunque
-- cierres mpv.

local mp = require "mp"

local MIN, MAX = 0.25, 4.0
-- Carpeta de estado portable: Linux = $XDG_STATE_HOME/mpv o ~/.local/state/mpv;
-- Windows = %LOCALAPPDATA%\mpv (fuera del repo, que está enlazado en %APPDATA%\mpv).
local function default_state_dir()
    if os.getenv("XDG_STATE_HOME") then return os.getenv("XDG_STATE_HOME") .. "/mpv" end
    if os.getenv("HOME") then return os.getenv("HOME") .. "/.local/state/mpv" end
    return (os.getenv("LOCALAPPDATA") or ".") .. "/mpv"
end
local state_dir = default_state_dir()

local function ensure_state_dir()
    if (require "mp.utils").file_info(state_dir) then return end
    local args = package.config:sub(1, 1) == "\\" and { "cmd", "/c", "mkdir", (state_dir:gsub("/", "\\")) }
                                                  or { "mkdir", "-p", state_dir }
    mp.command_native({ name = "subprocess", args = args, playback_only = false })
end
local speed_file = state_dir .. "/ultima-velocidad"

local overlay = mp.create_osd_overlay("ass-events")
local visor_on = true

local function draw()
    local s = mp.get_property_number("speed", 1)
    if not visor_on or math.abs(s - 1) < 0.001 then
        overlay:remove()
        return
    end
    overlay.res_x, overlay.res_y = 1280, 720
    overlay.data = string.format(
        "{\\an9\\pos(1265,12)\\fs26\\b1\\bord2\\3c&H000000&\\1c&H66D9FF&}⏩ %.2fx", s)
    overlay:update()
end

local function save_speed(s)
    ensure_state_dir()
    local f = io.open(speed_file, "w")
    if f then f:write(string.format("%.2f", s)); f:close() end
end

local function set_speed(s)
    s = math.floor(s * 100 + 0.5) / 100 -- evita cosas como 1.2000000001
    s = math.max(MIN, math.min(MAX, s))
    mp.set_property_number("speed", s)
    mp.osd_message(string.format("Velocidad: %.2fx", s))
end

local function change(delta)
    set_speed(mp.get_property_number("speed", 1) + delta)
end

mp.add_forced_key_binding("]", "vel-mas", function() change(0.1) end, { repeatable = true })
mp.add_forced_key_binding("[", "vel-menos", function() change(-0.1) end, { repeatable = true })
mp.add_forced_key_binding("}", "vel-mas-mucho", function() change(0.5) end, { repeatable = true })
mp.add_forced_key_binding("{", "vel-menos-mucho", function() change(-0.5) end, { repeatable = true })
mp.add_forced_key_binding("BS", "vel-normal", function() set_speed(1) end)
mp.add_forced_key_binding("Ctrl+v", "vel-visor", function()
    visor_on = not visor_on
    mp.osd_message(visor_on and "Visor de velocidad: visible" or "Visor de velocidad: oculto")
    draw()
end)

mp.observe_property("speed", "number", function(_, s)
    draw()
    if s then save_speed(s) end
end)

-- Al arrancar mpv, recuperar la última velocidad usada.
local f = io.open(speed_file, "r")
if f then
    local s = tonumber(f:read("*l"))
    f:close()
    if s and s >= MIN and s <= MAX then mp.set_property_number("speed", s) end
end
