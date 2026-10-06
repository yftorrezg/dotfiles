-- curso.lua — cargar un curso entero (carpeta + subcarpetas) como una sola lista.
--
--   Alt+c    toma la carpeta PADRE del video actual (la raíz del curso, p. ej.
--            "Curso/Módulo 1/video.mp4" → "Curso") y arma la lista con todos
--            sus videos, módulo tras módulo, sin cortar el video que estás viendo.
--   Alt+C    igual, pero con la carpeta del video actual (solo ese nivel y sus
--            subcarpetas).
--
-- Así, al terminar el último video del módulo 1 sigue solo con el módulo 2.

local mp = require "mp"
local utils = require "mp.utils"

local VIDEO = {}
for ext in ("3g2 3gp avi flv m2ts m4v mkv mov mp4 mpeg mpg ogv ts webm wmv"):gmatch("%S+") do
    VIDEO[ext] = true
end

-- Orden natural: "2 intro" va antes que "10 cierre".
local function natural_key(s)
    return s:lower():gsub("%d+", function(n) return string.format("%012d", tonumber(n)) end)
end

local function natural_sort(list)
    table.sort(list, function(a, b) return natural_key(a) < natural_key(b) end)
end

local function collect(dir, out)
    local files = utils.readdir(dir, "files") or {}
    natural_sort(files)
    for _, f in ipairs(files) do
        local ext = f:match("%.([^.]+)$")
        if ext and VIDEO[ext:lower()] then out[#out + 1] = utils.join_path(dir, f) end
    end
    local dirs = utils.readdir(dir, "dirs") or {}
    natural_sort(dirs)
    for _, d in ipairs(dirs) do
        if d:sub(1, 1) ~= "." then collect(utils.join_path(dir, d), out) end
    end
end

local function load_course(levels_up)
    local path = mp.get_property("path")
    if not path or path:match("^%a[%w+.-]*://") then return end
    if not (path:match("^/") or path:match("^%a:[/\\]")) then path = utils.join_path(mp.get_property("working-directory"), path) end

    path = path:gsub("\\", "/")   -- Windows: normalizar separadores para comparar rutas
    local dir = utils.split_path(path)
    for _ = 1, levels_up do dir = utils.split_path((dir:gsub("/$", ""))) end
    dir = dir:gsub("/$", "")

    local all = {}
    collect(dir, all)
    if #all == 0 then return end

    -- Deja solo el video actual y vuelve a armar la lista alrededor de él.
    mp.commandv("playlist-clear")
    local current_index
    for i, f in ipairs(all) do
        if f:gsub("\\", "/") == path then
            current_index = i - 1
        else
            mp.commandv("loadfile", f, "append")
        end
    end
    if current_index then mp.commandv("playlist-move", 0, current_index + 1) end

    mp.osd_message(string.format("Curso cargado: %d videos de «%s»", #all, dir:match("[^/]+$") or dir), 3)
end

mp.add_forced_key_binding("Alt+c", "curso-padre", function() load_course(1) end)
mp.add_forced_key_binding("Alt+C", "curso-actual", function() load_course(0) end)
