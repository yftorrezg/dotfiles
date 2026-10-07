-- capturas.lua — carpeta propia de capturas para los videos largos.
--
-- Videos de MÁS de 1 hora: s / S guardan en
--     ~/Imágenes/Capturas-mpv/<nombre del video>/<hora.min.seg>.png
-- Videos de 1 hora o menos: todo junto en ~/Imágenes/Capturas-mpv/
--     (con el nombre del video en cada archivo, como siempre).
-- Para cambiar el límite, edita MIN_SEGUNDOS.

local mp = require "mp"

local MIN_SEGUNDOS = 3600
local base = (os.getenv("HOME") or "") .. "/Imágenes/Capturas-mpv"
local template_normal = mp.get_property("screenshot-template")

local function aplicar()
    local dur = mp.get_property_number("duration")
    local nombre = mp.get_property("filename/no-ext")
    if dur and dur > MIN_SEGUNDOS and nombre and nombre ~= "" then
        nombre = nombre:gsub("[/%z]", "-"):sub(1, 100)
        local dir = base .. "/" .. nombre
        mp.set_property("screenshot-directory", dir)
        mp.set_property("screenshot-template", "%wH.%wM.%wS")
    else
        mp.set_property("screenshot-directory", base)
        mp.set_property("screenshot-template", template_normal)
    end
end

mp.register_event("file-loaded", aplicar)
mp.observe_property("duration", "number", function(_, d) if d then aplicar() end end)
