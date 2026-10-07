-- notas.lua — notas con tiempo, título, anotación y captura, ligadas a cada video.
--
--   Ctrl+n   nueva nota en este instante: pausa, escribes título (Enter) y anotación (Enter), sigue
--            (Esc en el título cancela · Esc en la anotación guarda solo con título)
--   h        ver / ocultar el panel de notas al lado (20 % a la derecha, video 80 %)
--
-- Las notas se guardan en ~/Documentos/Notas-cursos/<nombre del video>/ (notas.md, notas.json, capturas/).
-- El panel (panel-notas/servidor.py + panel.html) habla con mpv por un socket IPC; aquí se abre ese
-- socket. Clic en el minuto de una nota = mpv salta ahí. Detalles en GUIA-MPV.md.

local mp = require "mp"
local utils = require "mp.utils"
local input = require "mp.input"

local base = mp.command_native({ "expand-path", "~~/panel-notas" })
local servidor = base .. "/servidor.py"
local toggle = base .. "/panel-toggle.sh"
local rundir = os.getenv("XDG_RUNTIME_DIR") or "/tmp"
local sock = rundir .. "/mpv-notas.sock"

local function fmt(t)
    t = math.floor(t)
    local h, m, s = math.floor(t / 3600), math.floor(t % 3600 / 60), t % 60
    if h > 0 then return string.format("%d:%02d:%02d", h, m, s) end
    return string.format("%d:%02d", m, s)
end

local function ruta_video()
    local path = mp.get_property("path")
    if not path then return nil end
    if not path:match("^%a[%w+.-]*://") and not path:match("^/") then
        path = utils.join_path(mp.get_property("working-directory"), path)
    end
    return path
end

-- La ventana de mpv donde pulses h/Ctrl+n pasa a ser la que controla el panel.
local function abrir_socket()
    mp.set_property("input-ipc-server", "")
    mp.set_property("input-ipc-server", sock)
end
abrir_socket()

local nueva_en_curso = false

local function nueva()
    if nueva_en_curso then return end
    local t, video = mp.get_property_number("time-pos"), ruta_video()
    if not t or not video then return end
    local estaba_pausado = mp.get_property_bool("pause")
    mp.set_property_bool("pause", true)
    local tmp = string.format("%s/nota-mpv-%d.jpg", rundir, os.time())
    mp.commandv("screenshot-to-file", tmp, "video")
    nueva_en_curso = true

    local function seguir() if not estaba_pausado then mp.set_property_bool("pause", false) end end
    local function cancelar()
        os.remove(tmp)
        nueva_en_curso = false
        seguir()
        mp.osd_message("Nota cancelada")
    end
    local function guardar(titulo, texto)
        local r = mp.command_native({ name = "subprocess", playback_only = false, capture_stdout = true,
            capture_stderr = true, args = { "python3", servidor, "nota", video, tostring(t), titulo, texto, tmp } })
        nueva_en_curso = false
        seguir()
        if r.status == 0 then
            mp.osd_message(string.format("📝 Nota guardada  ⏱ %s  %s", fmt(t), titulo ~= "" and ("— " .. titulo) or ""), 2.5)
        else
            mp.osd_message("No se pudo guardar la nota: " .. (r.stderr or ""), 4)
        end
    end

    local titulo_ok = false
    input.get({
        prompt = string.format("Título ⏱ %s: ", fmt(t)),
        submit = function(titulo)
            titulo_ok = true
            input.terminate()
            -- pequeña espera para que la 1ª caja termine de cerrarse antes de abrir la 2ª
            mp.add_timeout(0.05, function()
                local enviado = false
                input.get({
                    prompt = "Anotación: ",
                    submit = function(texto)
                        enviado = true
                        input.terminate()
                        guardar(titulo, texto)
                    end,
                    closed = function()
                        if not enviado then guardar(titulo, "") end -- Esc = guardar solo con título
                    end,
                })
            end)
        end,
        closed = function()
            if not titulo_ok then cancelar() end
        end,
    })
end

local function panel()
    abrir_socket()
    local salio = false
    if mp.get_property_bool("fullscreen") then
        mp.set_property_bool("fullscreen", false)
        salio = true
    end
    mp.add_timeout(salio and 0.5 or 0, function()
        mp.command_native_async({ name = "subprocess", playback_only = false, args = { toggle } }, function() end)
    end)
end

mp.add_forced_key_binding("Ctrl+n", "nota-nueva", nueva)
mp.add_forced_key_binding("h", "nota-panel", panel)
