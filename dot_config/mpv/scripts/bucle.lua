-- bucle.lua — repetir un fragmento del video, fácil y con memoria.
--
--   c            1ª vez: inicio (A) · 2ª vez: fin (B) y empieza a repetir · 3ª: quitar
--   Ctrl+c       repite los últimos 15 s (sin marcar nada antes); otra vez: quitar
--   Shift+L      lista de bucles guardados de este video: eliges uno y se activa
--
-- Mientras repites se ve arriba a la izquierda "🔁 A 12:30 → B 13:10", y el
-- trozo se pinta en la barra de tiempo. Cada bucle que cierras se guarda solo
-- por video en ~/.local/state/mpv/bucles.json (máximo 20, sin duplicados).

local mp = require "mp"
local utils = require "mp.utils"

local LAST = 15 -- segundos que repite Ctrl+c
local state_dir = (os.getenv("XDG_STATE_HOME") or (os.getenv("HOME") .. "/.local/state")) .. "/mpv"
local db_path = state_dir .. "/bucles.json"
local db = {}

local function load_db()
    local f = io.open(db_path, "r")
    if not f then return end
    db = utils.parse_json(f:read("*a")) or {}
    f:close()
end

local function save_db()
    os.execute("mkdir -p '" .. state_dir .. "'")
    local f = io.open(db_path, "w")
    if f then f:write(utils.format_json(db)); f:close() end
end

local function key()
    local path = mp.get_property("path")
    if not path then return nil end
    if not path:match("^%a[%w+.-]*://") and not path:match("^/") then
        path = utils.join_path(mp.get_property("working-directory"), path)
    end
    return path
end

local function fmt(t)
    t = math.floor(t)
    local h, m, s = math.floor(t / 3600), math.floor(t % 3600 / 60), t % 60
    if h > 0 then return string.format("%d:%02d:%02d", h, m, s) end
    return string.format("%d:%02d", m, s)
end

local function get_ab()
    return mp.get_property_number("ab-loop-a"), mp.get_property_number("ab-loop-b")
end

local function save_loop(a, b)
    local k = key()
    if not k then return end
    local list = db[k] or {}
    for _, l in ipairs(list) do
        if math.abs(l.a - a) < 1 and math.abs(l.b - b) < 1 then return end
    end
    list[#list + 1] = { a = a, b = b }
    table.sort(list, function(x, y) return x.a < y.a end)
    while #list > 20 do table.remove(list, 1) end
    db[k] = list
    save_db()
end

local function clear()
    mp.set_property("ab-loop-a", "no")
    mp.set_property("ab-loop-b", "no")
end

local function start(a, b)
    mp.set_property_number("ab-loop-a", a)
    mp.set_property_number("ab-loop-b", b)
    mp.commandv("seek", a, "absolute+exact")
    mp.set_property_bool("pause", false)
end

-- Aviso fijo mientras hay bucle (o mientras falta poner el fin).
local overlay = mp.create_osd_overlay("ass-events")
local function draw()
    local a, b = get_ab()
    if not a then overlay:remove(); return end
    local txt
    if b then
        txt = string.format("🔁 A %s → B %s", fmt(a), fmt(b))
    else
        txt = string.format("🔁 A %s → … (pulsa c en el fin)", fmt(a))
    end
    overlay.res_x, overlay.res_y = 1280, 720
    overlay.data = "{\\an7\\pos(15,12)\\fs24\\b1\\bord2\\3c&H000000&\\1c&H80FF80&}" .. txt
    overlay:update()
end
mp.observe_property("ab-loop-a", "native", draw)
mp.observe_property("ab-loop-b", "native", draw)

mp.add_forced_key_binding("c", "bucle-ciclo", function()
    local a, b = get_ab()
    local now = mp.get_property_number("time-pos")
    if not now then return end
    if not a then
        mp.set_property_number("ab-loop-a", now)
        mp.osd_message("🔁 Inicio en " .. fmt(now) .. " — pulsa c en el final")
    elseif not b then
        if now <= a + 0.5 then
            mp.osd_message("El final debe ir después del inicio")
            return
        end
        mp.set_property_number("ab-loop-b", now)
        save_loop(a, now)
        mp.osd_message(string.format("🔁 Repitiendo %s → %s  (c = quitar)", fmt(a), fmt(now)))
    else
        clear()
        mp.osd_message("Bucle quitado")
    end
end)

mp.add_forced_key_binding("Ctrl+c", "bucle-ultimos", function()
    local a = get_ab()
    if a then clear(); mp.osd_message("Bucle quitado"); return end
    local now = mp.get_property_number("time-pos")
    if not now then return end
    local from = math.max(0, now - LAST)
    save_loop(from, now)
    start(from, now)
    mp.osd_message(string.format("🔁 Repitiendo los últimos %d s  (Ctrl+c = quitar)", LAST))
end)

mp.register_script_message("cargar-bucle", function(a, b) start(tonumber(a), tonumber(b)) end)
mp.register_script_message("borrar-bucles", function()
    local k = key()
    if k then db[k] = nil; save_db() end
    clear()
    mp.osd_message("Se borraron los bucles guardados de este video")
end)

mp.add_forced_key_binding("L", "bucle-menu", function()
    local list = db[key() or ""] or {}
    if #list == 0 then
        mp.osd_message("Sin bucles guardados. Usa c (inicio/fin) o Ctrl+c (últimos 15 s)")
        return
    end
    local items = {}
    for _, l in ipairs(list) do
        items[#items + 1] = {
            title = fmt(l.a) .. " → " .. fmt(l.b),
            hint = string.format("%d s", math.floor(l.b - l.a + 0.5)),
            value = { "script-message-to", mp.get_script_name(), "cargar-bucle", tostring(l.a), tostring(l.b) },
        }
    end
    items[#items + 1] = {
        title = "Borrar todos los bucles de este video",
        value = { "script-message-to", mp.get_script_name(), "borrar-bucles" },
    }
    mp.commandv("script-message-to", "uosc", "open-menu",
        utils.format_json({ type = "bucles", title = "Bucles guardados", items = items }))
end)

mp.register_event("file-loaded", function() load_db(); clear() end)
