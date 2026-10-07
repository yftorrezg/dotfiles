local mainMod = "SUPER"
local noctCall = "noctalia msg "
local launchPrefix = "uwsm app -- " -- if you are not using UWSM, make this empty (e.g. "")

---------------------------
---- WINDOW MANAGEMENT ----
---------------------------

-- Window manipulation
-- (24/09/2026) Quitado SUPER+Escape ("hyprctl kill", matar ventana con click): peligroso
-- y sin uso. Para colgados: CTRL+ALT+Escape (LibreOffice) o CTRL+SHIFT+Escape (btop).
hl.bind(mainMod .. " + Q",          hl.dsp.window.close())
hl.bind(mainMod .. " + ALT + Space", hl.dsp.window.float({ action = "toggle" }))
-- (07/10/2026) SUPER+D era "maximizar" (igual que SUPER+F, que ya cubre eso): ahora abre el menú de descargas
-- (link copiado -> video/720p/MP3/lista). Ver scripts/descargar-menu.sh y ~/.local/bin/descargar.
hl.bind(mainMod .. " + D",           hl.dsp.exec_cmd(launchPrefix .. "bash " .. os.getenv("HOME") .. "/.config/hypr/scripts/descargar-menu.sh"))
hl.bind(mainMod .. " + F",           hl.dsp.window.fullscreen())
hl.bind(mainMod .. " + J",           hl.dsp.layout("togglesplit"))

-- Change focus
hl.bind(mainMod .. " + Left",  hl.dsp.focus({ direction = "left" }))
hl.bind(mainMod .. " + Right", hl.dsp.focus({ direction = "right" }))
hl.bind(mainMod .. " + Up",    hl.dsp.focus({ direction = "up" }))
hl.bind(mainMod .. " + Down",  hl.dsp.focus({ direction = "down" }))
hl.bind("ALT + Tab",           hl.dsp.window.cycle_next())
-- SUPER+Tab: está en config/binds_equipo.lua (depende de los monitores de cada equipo).

-- Move active window around workspaces & monitors
hl.bind(mainMod .. " + SHIFT + Up",                   hl.dsp.window.move({ direction = "u" }))
hl.bind(mainMod .. " + SHIFT + Right",                hl.dsp.window.move({ direction = "r" }))
hl.bind(mainMod .. " + SHIFT + Left",                 hl.dsp.window.move({ direction = "l" }))
hl.bind(mainMod .. " + SHIFT + Down",                 hl.dsp.window.move({ direction = "d" }))
hl.bind(mainMod .. " + CONTROL + SHIFT + Right",      hl.dsp.window.move({ workspace = "m+1" }))
hl.bind(mainMod .. " + CONTROL + SHIFT + Left",       hl.dsp.window.move({ workspace = "m-1" }))
-- Mover ventana al escritorio N (en su mismo monitor): ver SUPER+CONTROL+N mas abajo.
-- (24/09/2026) Quitados: SUPER+SHIFT+3 (no hay 3er monitor), mover con rueda del mouse
-- (SUPER+SHIFT+rueda, SUPER+CTRL+SHIFT+rueda: se disparaban sin querer) y
-- SUPER+SHIFT+CTRL+N (4 teclas, reemplazado por SUPER+CTRL+N).

-- Move & Resize with mouse
hl.bind(mainMod .. " + mouse:272", hl.dsp.window.drag())
hl.bind(mainMod .. " + mouse:273", hl.dsp.window.resize())

-- Zoom
local function zoomfunction(value)
    local zoomvalue = hl.get_config("cursor:zoom_factor")
    if (zoomvalue + value) > 3.0 then
        hl.config({ cursor = { zoom_factor = 3.0 } })
    elseif (zoomvalue + value) < 1.0 then
        hl.config({ cursor = { zoom_factor = 1.0 } })
    else
        hl.config({ cursor = { zoom_factor = zoomvalue + value } })
    end
end
hl.bind(mainMod .. " + Minus", function() zoomfunction(-0.3) end, { repeating = true})
hl.bind(mainMod .. " + Plus", function() zoomfunction(0.3) end, { repeating = true })
-- (24/09/2026) Quitado el zoom duplicado con teclado numerico (code:82/86).


------------------
---- LAUNCHER ----
------------------

hl.bind(mainMod .. " + Return",     hl.dsp.exec_cmd(launchPrefix .. TERMINAL))
hl.bind(mainMod .. " + E",          hl.dsp.exec_cmd(launchPrefix .. FILE_MANAGER))
-- (25/09/2026) Quitado SUPER+T = editor de texto (queda en el launcher): ahora es TikTok.
hl.bind("XF86Calculator",           hl.dsp.exec_cmd(launchPrefix .. CALCULATOR))
hl.bind(mainMod .. " + W",          hl.dsp.exec_cmd(launchPrefix .. BROWSER))
-- (24/09/2026) SUPER+N = Obsidian (N de notas).
hl.bind(mainMod .. " + N",          hl.dsp.exec_cmd(launchPrefix .. "obsidian"))

-- Apps web / VS Code: enfocar-o-abrir en su escritorio fijo (scripts/app-web.sh, 25/09/2026).
-- Todo con la mano izquierda. SUPER+I (VS Code) paso a SUPER+G. YouTube se abre en el escritorio actual.
local appWeb = "bash " .. os.getenv("HOME") .. "/.config/hypr/scripts/app-web.sh "
hl.bind(mainMod .. " + ALT + Q", hl.dsp.exec_cmd(appWeb .. "youtube"))
hl.bind(mainMod .. " + ALT + W", hl.dsp.exec_cmd(appWeb .. "whatsapp"))
hl.bind(mainMod .. " + ALT + T", hl.dsp.exec_cmd(appWeb .. "telegram"))
hl.bind(mainMod .. " + ALT + F", hl.dsp.exec_cmd(appWeb .. "facebook"))
hl.bind(mainMod .. " + ALT + I", hl.dsp.exec_cmd(appWeb .. "instagram"))
hl.bind(mainMod .. " + ALT + D", hl.dsp.exec_cmd(appWeb .. "drive"))
hl.bind(mainMod .. " + T",       hl.dsp.exec_cmd(appWeb .. "tiktok"))
hl.bind(mainMod .. " + G",       hl.dsp.exec_cmd(appWeb .. "code"))
hl.bind("CONTROL + SHIFT + Escape", hl.dsp.exec_cmd(launchPrefix .. TERMINAL .. " -e btop"))

-- Matar LibreOffice colgado en 1 paso (SIGKILL directo a soffice.bin), sin pasar por btop.
hl.bind("CONTROL + ALT + Escape", hl.dsp.exec_cmd(launchPrefix .. "bash " .. os.getenv("HOME") .. "/.config/hypr/scripts/matar-libreoffice.sh"))
hl.bind(mainMod .. " + Z",          hl.dsp.exec_cmd(noctCall .. "settings-toggle"))
hl.bind(mainMod .. " + X",          hl.dsp.exec_cmd(noctCall .. "panel-toggle control-center"))
-- Buscador: SUPER solo (tap y soltar). Antes era SUPER+Space (cambiado 18/09/2026).
-- Es un bind de "release" sobre la propia tecla Super_L, asi que dispara al soltarla.
hl.bind(mainMod .. " + Super_L",    hl.dsp.exec_cmd(noctCall .. "panel-toggle launcher"), { release = true })
hl.bind(mainMod .. " + period",     hl.dsp.exec_cmd(noctCall .. "panel-toggle launcher /emo"))
hl.bind(mainMod .. " + L",          hl.dsp.exec_cmd(noctCall .. "session lock"))
hl.bind(mainMod .. " + K",          hl.dsp.exec_cmd(launchPrefix .. "opendeck")) -- Abrir/enfocar la ventana de config del Stream Deck (el backend sigue corriendo aunque la cierres con SUPER+Q)

-- Sesión de estudio: abrir curso+apuntes (SUPER+C) y configurar/actualizar links (SUPER+ALT+C)
-- NOTA (30/08/2026): "SUPER+C" se liberó de "Calculadora" (queda accesible por XF86Calculator)
-- y "SUPER+ALT+C" se liberó de "menú de sesión" (usás el cursor arriba/derecha para eso).
hl.bind(mainMod .. " + C",       hl.dsp.exec_cmd(launchPrefix .. "bash " .. os.getenv("HOME") .. "/.config/hypr/scripts/curso-abrir.sh"))
hl.bind(mainMod .. " + ALT + C", hl.dsp.exec_cmd(launchPrefix .. "bash " .. os.getenv("HOME") .. "/.config/hypr/scripts/curso-configurar.sh"))

---------------------------
---- HARDWARE CONTROLS ----
---------------------------

-- Audio
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd(noctCall .. "volume-up"),   { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd(noctCall .. "volume-down"), { locked = true, repeating = true })
hl.bind("XF86AudioMute",        hl.dsp.exec_cmd(noctCall .. "volume-mute"), { locked = true })
hl.bind("XF86AudioMicMute",     hl.dsp.exec_cmd(noctCall .. "mic-mute"),    { locked = true })

-- Media
hl.bind("XF86AudioPlay",  hl.dsp.exec_cmd(noctCall .. "media toggle"),   { locked = true })
hl.bind("XF86AudioPause", hl.dsp.exec_cmd(noctCall .. "media toggle"),   { locked = true })
hl.bind("XF86AudioNext",  hl.dsp.exec_cmd(noctCall .. "media next"),     { locked = true })
hl.bind("XF86AudioPrev",  hl.dsp.exec_cmd(noctCall .. "media previous"), { locked = true })

-- Brightness
hl.bind("XF86MonBrightnessUp",   hl.dsp.exec_cmd(noctCall .. "brightness-up"),   { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown", hl.dsp.exec_cmd(noctCall .. "brightness-down"), { locked = true, repeating = true })

-------------------
---- UTILITIES ----
-------------------

-- Screen Capture
-- (24/09/2026) Quitado SUPER+P (selector de color): sin uso, sigue en el Stream Deck.
hl.bind("Print",              hl.dsp.exec_cmd(noctCall .. "screenshot-region"))
hl.bind(mainMod .. " + Print", hl.dsp.exec_cmd(noctCall .. "screenshot-fullscreen"))

-- Capturas personalizadas: carpeta configurable + guardar/portapapeles en 2 pasos, sin confirmar
hl.bind("CONTROL + SHIFT + D", hl.dsp.exec_cmd(launchPrefix .. "bash " .. os.getenv("HOME") .. "/.config/hypr/scripts/elegir-carpeta-capturas.sh"))
hl.bind("CONTROL + SHIFT + S", hl.dsp.exec_cmd(launchPrefix .. "bash " .. os.getenv("HOME") .. "/.config/hypr/scripts/captura-guardar.sh"))
-- (26/09/2026) Auto-captura de cursos: captura el monitor con foco solo cuando cambia (ajustes en auto-captura.conf).
-- Videos de YouTube/archivos sin reproducir: scripts/video-a-capturas.sh <url|archivo>
hl.bind(mainMod .. " + ALT + S", hl.dsp.exec_cmd(launchPrefix .. "bash " .. os.getenv("HOME") .. "/.config/hypr/scripts/auto-captura-toggle.sh"))
-- SUPER+ALT+Y: capturas del link de YouTube copiado (lo baja y procesa en segundo plano)
hl.bind(mainMod .. " + ALT + Y", hl.dsp.exec_cmd(launchPrefix .. "bash " .. os.getenv("HOME") .. "/.config/hypr/scripts/youtube-capturas.sh"))
-- SUPER+ALT+A: elegir la carpeta de un curso y sacar capturas + apuntes de todas las clases (segundo plano)
hl.bind(mainMod .. " + ALT + A", hl.dsp.exec_cmd(launchPrefix .. "bash " .. os.getenv("HOME") .. "/.config/hypr/scripts/curso-apuntes-elegir.sh"))
-- (29/09/2026) Centro de estudio: SUPER+I abre la próxima clase (pre-test, apuntes, práctica, tests)
hl.bind(mainMod .. " + I", hl.dsp.exec_cmd(launchPrefix .. "python3 " .. os.getenv("HOME") .. "/.config/hypr/scripts/estudiar.py"))
-- SUPER+ALT+V: verificar (correr) los tests de la práctica de la clase actual → notificación ✅/❌
hl.bind(mainMod .. " + ALT + V", hl.dsp.exec_cmd(launchPrefix .. "python3 " .. os.getenv("HOME") .. "/.config/hypr/scripts/estudiar.py --tests"))
-- (06/10/2026) Pomodoro sin atajo de teclado (el usuario no lo usa); sigue en el Stream Deck (scripts/pomodoro-toggle.sh).

-- (24/09/2026) Quitado SUPER+SHIFT+W (fondos de pantalla): sin uso, sigue en el Stream Deck.

-- Clipboard
hl.bind(mainMod .. " + V", hl.dsp.exec_cmd(noctCall .. "panel-toggle clipboard"))

-- Notifications
hl.bind(mainMod .. " + A", hl.dsp.exec_cmd(noctCall .. "panel-toggle control-center notifications"))

-------------------------------
---- WORKSPACES & MONITORS ----
-------------------------------
-- Lo que depende de los monitores de cada equipo (escritorios virtuales, mover entre
-- pantallas, teclas Fn) está en config/binds_equipo.lua (distinto en PC y laptop).
require("config.binds_equipo")

-- Workspaces con nombre (gaming/estudio): no tienen número asignado y solo se
-- llenan por las reglas de windowrules.lua/workspaces.lua, así que sin estos
-- atajos quedan "perdidos" para saltar a ellos manualmente.
-- (24/09/2026) Quitado SUPER+G (workspace gaming): Steam no esta instalado.
hl.bind(mainMod .. " + ALT + E",  hl.dsp.focus({ workspace = "name:estudio" }))

-- Special workspace (scratchpad)
-- NOTA: "SUPER + SHIFT + S" se liberó de "mover ventana al special workspace" (30/08/2026)
-- y ahora es "captura rápida al portapapeles" (ver más abajo). El toggle de mostrar/ocultar
-- el special workspace (SUPER+S) sigue funcionando, pero ya no hay atajo para enviar
-- ventanas ahí -- si se vuelve a necesitar, agregar otro combo.
hl.bind(mainMod .. " + S", hl.dsp.workspace.toggle_special())

-- Captura rápida: seleccionar región en 1 paso -> solo portapapeles, sin guardar archivo
hl.bind(mainMod .. " + SHIFT + S", hl.dsp.exec_cmd(launchPrefix .. "bash " .. os.getenv("HOME") .. "/.config/hypr/scripts/captura-portapapeles.sh"))

-- Lectura en voz alta: SUPER+R lee el texto seleccionado (mouse). Apretar de nuevo mientras lee = interrumpe.
-- SUPER+ALT+R elige qué voz usar (edge-tts online o Piper offline). Config en voz.conf.
hl.bind(mainMod .. " + R",       hl.dsp.exec_cmd(launchPrefix .. "bash " .. os.getenv("HOME") .. "/.config/hypr/scripts/leer-seleccion.sh"))
hl.bind(mainMod .. " + ALT + R", hl.dsp.exec_cmd(launchPrefix .. "bash " .. os.getenv("HOME") .. "/.config/hypr/scripts/actualizar-voz.sh"))

-- (24/09/2026) Quitado SUPER+SHIFT+ALT+N (mover ventana a workspace N): 4 teclas,
-- reemplazado por SUPER+CONTROL+N.
