-- marcadores.lua — marcar puntos de un video y volver a ellos.
--
--   b            agrega un marcador en el primer hueco libre (1-9)
--   Ctrl+1..9    guarda el marcador en ese número (lo reemplaza)
--   1..9         salta a ese marcador
--   Alt+1..9     borra ese marcador
--   B            lista de marcadores (menú de uosc) para elegir y saltar
--   Ctrl+B       borra todos los marcadores del video
--
-- Los marcadores se guardan por video en ~/.local/state/mpv/marcadores.json y
-- aparecen como rayitas en la barra de tiempo (se añaden como capítulos,
-- así que RePág/AvPág también saltan entre ellos).

local mp = require "mp"
local utils = require "mp.utils"

local state_dir = (os.getenv("XDG_STATE_HOME") or (os.getenv("HOME") .. "/.local/state")) .. "/mpv"
local db_path = state_dir .. "/marcadores.json"

local db = {}
local original_chapters = {}

local function load_db()
    local f = io.open(db_path, "r")
    if not f then return end
    db = utils.parse_json(f:read("*a")) or {}
    f:close()
end

local function save_db()
    os.execute("mkdir -p '" .. state_dir .. "'")
    local f = io.open(db_path, "w")
    if not f then
        mp.osd_message("No se pudo guardar " .. db_path)
        return
    end
    f:write(utils.format_json(db))
    f:close()
end

local function key()
    local path = mp.get_property("path")
    if not path then return nil end
    if not path:match("^%a[%w+.-]*://") and not path:match("^/") then
        path = utils.join_path(mp.get_property("working-directory"), path)
    end
    return path
end

local function marks()
    local k = key()
    if not k then return nil end
    db[k] = db[k] or {}
    return db[k]
end

local function fmt(t)
    t = math.floor(t)
    local h, m, s = math.floor(t / 3600), math.floor(t % 3600 / 60), t % 60
    if h > 0 then return string.format("%d:%02d:%02d", h, m, s) end
    return string.format("%d:%02d", m, s)
end

-- Pinta los marcadores en la barra de tiempo mezclándolos con los capítulos reales.
local function refresh_chapters()
    local list = {}
    for _, c in ipairs(original_chapters) do list[#list + 1] = c end
    local m = marks() or {}
    for i = 1, 9 do
        local t = m[tostring(i)]
        if t then list[#list + 1] = { title = "★ Marca " .. i, time = t } end
    end
    table.sort(list, function(a, b) return a.time < b.time end)
    mp.set_property_native("chapter-list", list)
end

local function set_mark(i)
    local m, t = marks(), mp.get_property_number("time-pos")
    if not m or not t then return end
    m[tostring(i)] = t
    save_db()
    refresh_chapters()
    mp.osd_message(string.format("★ Marca %d guardada en %s", i, fmt(t)))
end

local function jump_mark(i)
    local m = marks()
    local t = m and m[tostring(i)]
    if not t then
        mp.osd_message(string.format("La marca %d está vacía (Ctrl+%d o b para crearla)", i, i))
        return
    end
    mp.commandv("seek", t, "absolute+exact")
    mp.osd_message(string.format("→ Marca %d (%s)", i, fmt(t)))
end

local function delete_mark(i)
    local m = marks()
    if not m or not m[tostring(i)] then
        mp.osd_message(string.format("La marca %d ya estaba vacía", i))
        return
    end
    m[tostring(i)] = nil
    save_db()
    refresh_chapters()
    mp.osd_message(string.format("Marca %d borrada", i))
end

local function add_mark()
    local m = marks()
    if not m then return end
    for i = 1, 9 do
        if not m[tostring(i)] then return set_mark(i) end
    end
    mp.osd_message("Ya tienes las 9 marcas ocupadas. Usa Ctrl+número para reemplazar una.")
end

local function clear_marks()
    local k = key()
    if not k then return end
    db[k] = nil
    save_db()
    refresh_chapters()
    mp.osd_message("Se borraron todas las marcas de este video")
end

local function show_menu()
    local m = marks() or {}
    local items = {}
    for i = 1, 9 do
        local t = m[tostring(i)]
        if t then
            items[#items + 1] = {
                title = "Marca " .. i,
                hint = fmt(t),
                value = { "script-message-to", mp.get_script_name(), "saltar-marca", tostring(i) },
            }
        end
    end
    if #items == 0 then
        mp.osd_message("Este video no tiene marcas. Pulsa b para crear una.")
        return
    end
    local menu = { type = "marcadores", title = "Marcadores", items = items }
    mp.commandv("script-message-to", "uosc", "open-menu", utils.format_json(menu))
end

mp.register_script_message("saltar-marca", function(i) jump_mark(tonumber(i)) end)

for i = 1, 9 do
    mp.add_forced_key_binding(tostring(i), "saltar-marca-" .. i, function() jump_mark(i) end)
    mp.add_forced_key_binding("Ctrl+" .. i, "guardar-marca-" .. i, function() set_mark(i) end)
    mp.add_forced_key_binding("Alt+" .. i, "borrar-marca-" .. i, function() delete_mark(i) end)
end
mp.add_forced_key_binding("b", "agregar-marca", add_mark)
mp.add_forced_key_binding("B", "menu-marcas", show_menu)
mp.add_forced_key_binding("Ctrl+b", "borrar-marcas", clear_marks)

mp.register_event("file-loaded", function()
    load_db()
    original_chapters = mp.get_property_native("chapter-list") or {}
    refresh_chapters()
end)
