-- curso.lua — un curso entero (todos los capítulos) como UNA sola lista de reproducción.
--
-- AUTOMÁTICO (08/11/2026): al abrir un video que es parte de un curso, la lista pasa a ser el curso
-- completo, capítulo tras capítulo, sin cortar el video actual. Así `>` / `<` (o N / P) y el panel de
-- Shift+H pasan del último video de un capítulo al primero del siguiente.
-- Es "parte de un curso" si, subiendo hasta 4 carpetas, alguna tiene Apuntes/ (o capturas/,
-- capturas-clave/: lo que dejan SUPER+ALT+A/Y), o si la carpeta del video es un capítulo: su carpeta
-- padre tiene 2+ subcarpetas con videos.
--
--   Alt+c    lo mismo a mano, con la carpeta PADRE del video (por si no se detectó el curso)
--   Alt+C    a mano, con la carpeta del video actual y sus subcarpetas

local mp = require "mp"
local utils = require "mp.utils"

local VIDEO = {}
for ext in ("3g2 3gp avi flv m2ts m4v mkv mov mp4 mpeg mpg ogv ts webm wmv"):gmatch("%S+") do
    VIDEO[ext] = true
end
-- carpetas que arma el sistema de apuntes: no tienen videos y son grandes (no se recorren)
local SALTAR = { Apuntes = true, capturas = true, ["capturas-clave"] = true, ["capturas-esenciales"] = true,
                 ["todas-las-capturas"] = true, ["codigo-en-imagenes"] = true, node_modules = true }
local MARCAS = { "Apuntes", "capturas", "capturas-clave" }

-- Orden natural: "2 intro" va antes que "10 cierre".
local function natural_key(s)
    return s:lower():gsub("%d+", function(n) return string.format("%012d", tonumber(n)) end)
end

local function natural_sort(list)
    table.sort(list, function(a, b) return natural_key(a) < natural_key(b) end)
end

local function es_video(f)
    local ext = f:match("%.([^.]+)$")
    return ext and VIDEO[ext:lower()] and not f:match("%.part$")
end

local function collect(dir, out)
    local files = utils.readdir(dir, "files") or {}
    natural_sort(files)
    -- "clase.mp4" y "clase.es.mp4" (doblado): queda solo el doblado, como en curso-a-apuntes.sh
    local hay = {}
    for _, f in ipairs(files) do hay[f] = true end
    for _, f in ipairs(files) do
        if es_video(f) then
            local base, ext = f:match("^(.*)%.([^.]+)$")
            if not (hay[base .. ".es." .. ext] or hay[base .. ".en." .. ext]) then
                out[#out + 1] = utils.join_path(dir, f)
            end
        end
    end
    local dirs = utils.readdir(dir, "dirs") or {}
    natural_sort(dirs)
    for _, d in ipairs(dirs) do
        if d:sub(1, 1) ~= "." and not SALTAR[d] then collect(utils.join_path(dir, d), out) end
    end
end

local function padre(dir)
    local p = utils.split_path((dir:gsub("/$", "")))
    return (p:gsub("/$", ""))
end

local function tiene_videos(dir)
    for _, f in ipairs(utils.readdir(dir, "files") or {}) do
        if es_video(f) then return true end
    end
    return false
end

local function raiz_del_curso(video_dir)
    local d = video_dir
    for _ = 0, 4 do
        for _, m in ipairs(MARCAS) do
            local info = utils.file_info(utils.join_path(d, m))
            if info and info.is_dir then return d end
        end
        local p = padre(d)
        if p == d or p == "" then break end
        d = p
    end
    -- sin marcas (curso todavía sin apuntes): la carpeta del video es un capítulo si tiene 2+ hermanos con videos
    local p = padre(video_dir)
    local n = 0
    for _, s in ipairs(utils.readdir(p, "dirs") or {}) do
        if s:sub(1, 1) ~= "." and not SALTAR[s] and tiene_videos(utils.join_path(p, s)) then n = n + 1 end
    end
    if n >= 2 then return p end
    return nil
end

local function ruta_actual()
    local path = mp.get_property("path")
    if not path or path:match("^%a[%w+.-]*://") then return nil end
    if not path:match("^/") then path = utils.join_path(mp.get_property("working-directory"), path) end
    return path
end

local function cargar(dir, avisar)
    local path = ruta_actual()
    if not path or not dir then return end
    local all = {}
    collect(dir, all)
    if #all <= 1 then return end
    -- deja solo el video actual y arma la lista alrededor de él
    mp.commandv("playlist-clear")
    local actual
    for i, f in ipairs(all) do
        if f == path then
            actual = i - 1
        else
            mp.commandv("loadfile", f, "append")
        end
    end
    if actual then
        mp.commandv("playlist-move", 0, actual + 1)
    end
    if avisar then
        mp.osd_message(string.format("📚 Curso entero: %d videos · «%s»", #all, dir:match("[^/]+$") or dir), 3)
    end
end

-- automático: una sola vez por mpv, con el primer video que se abre
local hecho = false
mp.register_event("file-loaded", function()
    if hecho then return end
    hecho = true
    local path = ruta_actual()
    if not path then return end
    local dir = utils.split_path(path):gsub("/$", "")
    local raiz = raiz_del_curso(dir)
    if raiz and raiz ~= dir then cargar(raiz, true) end
end)

mp.add_forced_key_binding("Alt+c", "curso-padre", function()
    local path = ruta_actual()
    if path then cargar(padre(utils.split_path(path)), true) end
end)
mp.add_forced_key_binding("Alt+C", "curso-actual", function()
    local path = ruta_actual()
    if path then cargar((utils.split_path(path):gsub("/$", "")), true) end
end)

-- lo llama el panel de notas (botón «Todo el curso» tras reproducir solo los importantes)
mp.register_script_message("curso-completo", function()
    local path = ruta_actual()
    if not path then return end
    local dir = utils.split_path(path):gsub("/$", "")
    cargar(raiz_del_curso(dir) or dir, true)
end)
