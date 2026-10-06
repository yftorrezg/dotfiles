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
hl.bind(mainMod .. " + D",           hl.dsp.window.fullscreen({ mode = 1 }))
hl.bind(mainMod .. " + F",           hl.dsp.window.fullscreen())
hl.bind(mainMod .. " + J",           hl.dsp.layout("togglesplit"))

-- Change focus
hl.bind(mainMod .. " + Left",  hl.dsp.focus({ direction = "left" }))
hl.bind(mainMod .. " + Right", hl.dsp.focus({ direction = "right" }))
hl.bind(mainMod .. " + Up",    hl.dsp.focus({ direction = "up" }))
hl.bind(mainMod .. " + Down",  hl.dsp.focus({ direction = "down" }))
hl.bind("ALT + Tab",           hl.dsp.window.cycle_next())
-- SUPER+Tab: definido mas abajo (seccion WORKSPACES & MONITORS), porque necesita
-- monitorSlots/currentVirtualDesktopIndex para ciclar entre TODOS los monitores
-- del "escritorio virtual" actual (ver nota ahi).

-- Move active window around workspaces & monitors
hl.bind(mainMod .. " + SHIFT + Up",                   hl.dsp.window.move({ direction = "u" }))
hl.bind(mainMod .. " + SHIFT + Right",                hl.dsp.window.move({ direction = "r" }))
hl.bind(mainMod .. " + SHIFT + Left",                 hl.dsp.window.move({ direction = "l" }))
hl.bind(mainMod .. " + SHIFT + Down",                 hl.dsp.window.move({ direction = "d" }))
hl.bind(mainMod .. " + SHIFT + 1",                    hl.dsp.window.move({ monitor = MONITOR1 }))
hl.bind(mainMod .. " + SHIFT + 2",                    hl.dsp.window.move({ monitor = MONITOR2 }))
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
-- (29/09/2026) Centro de estudio: SUPER+ALT+Z abre la próxima clase (pre-test, apuntes, práctica, tests)
hl.bind(mainMod .. " + ALT + Z", hl.dsp.exec_cmd(launchPrefix .. "python3 " .. os.getenv("HOME") .. "/.config/hypr/scripts/estudiar.py"))
-- SUPER+ALT+V: verificar (correr) los tests de la práctica de la clase actual → notificación ✅/❌
hl.bind(mainMod .. " + ALT + V", hl.dsp.exec_cmd(launchPrefix .. "python3 " .. os.getenv("HOME") .. "/.config/hypr/scripts/estudiar.py --tests"))

-- (24/09/2026) Quitado SUPER+SHIFT+W (fondos de pantalla): sin uso, sigue en el Stream Deck.

-- Clipboard
hl.bind(mainMod .. " + V", hl.dsp.exec_cmd(noctCall .. "panel-toggle clipboard"))

-- Notifications
hl.bind(mainMod .. " + A", hl.dsp.exec_cmd(noctCall .. "panel-toggle control-center notifications"))

-------------------------------
---- WORKSPACES & MONITORS ----
-------------------------------

-- "Escritorio virtual": cambia el workspace en TODOS los monitores a la vez,
-- sin robarle el foco al monitor que ya lo tenía. Cada monitor tiene su propio
-- rango de workspaces (MONITOR1: 1..NUM_WPM, MONITOR2: NUM_WPM+1..2*NUM_WPM, etc.)
-- y el índice de "escritorio virtual" i selecciona el workspace correspondiente
-- de ese rango en cada monitor conectado.
local monitorSlots = { MONITOR1, MONITOR2, MONITOR3 }

local function switchVirtualDesktop(i)
    for slot, output in ipairs(monitorSlots) do
        if output ~= "" then
            local mon = hl.get_monitor(output)
            if mon then
                mon:set_workspace({ workspace = (slot - 1) * NUM_WPM + i })
            end
        end
    end
end

local function currentVirtualDesktopIndex()
    local mon = hl.get_active_monitor()
    if not mon or not mon.active_workspace then return 1 end
    for slot, output in ipairs(monitorSlots) do
        if output == mon.name then
            local rel = mon.active_workspace.id - (slot - 1) * NUM_WPM
            if rel >= 1 and rel <= NUM_WPM then return rel end
        end
    end
    return 1
end

local function switchVirtualDesktopRelative(delta)
    local cur = currentVirtualDesktopIndex()
    local nextI = ((cur - 1 + delta) % NUM_WPM) + 1
    switchVirtualDesktop(nextI)
end

-- SUPER+Tab: cicla entre las ventanas del "escritorio virtual" actual sumando
-- TODOS los monitores que lo componen (no solo el monitor enfocado). Reemplaza
-- el overlay de Noctalia (window-switcher), que mostraba ventanas de TODOS los
-- escritorios virtuales sin poder filtrar por el actual (2026-09).
local function cycleVirtualDesktopWindows()
    local cur = currentVirtualDesktopIndex()
    local windows = {}
    for slot, output in ipairs(monitorSlots) do
        if output ~= "" then
            for _, w in ipairs(hl.get_windows({ workspace = (slot - 1) * NUM_WPM + cur })) do
                windows[#windows + 1] = w
            end
        end
    end
    if #windows < 2 then return end
    table.sort(windows, function(a, b) return a.stable_id < b.stable_id end)
    local active = hl.get_active_window()
    local idx = 1
    if active then
        for i, w in ipairs(windows) do
            if w.address == active.address then idx = i break end
        end
    end
    hl.dispatch(hl.dsp.focus({ window = windows[(idx % #windows) + 1] }))
end
hl.bind(mainMod .. " + Tab", cycleVirtualDesktopWindows)


-- Focus on monitors
hl.bind(mainMod .. " + ALT + 1", hl.dsp.focus({ monitor = MONITOR1 }))
hl.bind(mainMod .. " + ALT + 2", hl.dsp.focus({ monitor = MONITOR2 }))

-- Focus on workspace number
-- Absolute: cambia el "escritorio virtual" i en todos los monitores a la vez
for i = 1, NUM_WPM do
    local key = i % 10
    hl.bind(mainMod .. " + " .. key, function() switchVirtualDesktop(i) end)
end
-- SUPER+CONTROL+N: mover la ventana enfocada al escritorio N (en su mismo monitor).
-- (24/09/2026) Antes era "enfocar workspace N solo del monitor actual", redundante con
-- SUPER+N; y mover ventana requeria 4 teclas (SUPER+SHIFT+CTRL+N / SUPER+SHIFT+ALT+N).
-- Tambien sirve para sacar una ventana del special workspace (SUPER+S).
for i = 1, NUM_WPM do
    local key = i % 10
    hl.bind(mainMod .. " + CONTROL + " .. key, hl.dsp.window.move({ workspace = "m~" .. i }))
end

-- Escritorio virtual siguiente/anterior (todos los monitores a la vez).
-- OJO: el Stream Deck (perfil Escritorios) simula estas teclas, no cambiarlas.
-- (24/09/2026) Quitado SUPER+CTRL+Down (proximo vacio): sigue en el Stream Deck.
hl.bind(mainMod .. " + CONTROL + Right",       function() switchVirtualDesktopRelative(1) end)
hl.bind(mainMod .. " + CONTROL + Left",        function() switchVirtualDesktopRelative(-1) end)

-- Scroll para cambiar de escritorio virtual (todos los monitores a la vez)
-- (24/09/2026) Quitado SUPER+CTRL+rueda: hacia lo mismo que SUPER+rueda pero invertido.
hl.bind(mainMod .. " + mouse_down",           function() switchVirtualDesktopRelative(-1) end)
hl.bind(mainMod .. " + mouse_up",             function() switchVirtualDesktopRelative(1) end)

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
