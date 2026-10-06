-- binds_equipo.lua — atajos que dependen del hardware de este equipo: PC (DP-3 + HDMI-A-1 vertical).
-- Lo cargan los binds comunes (config/binds.lua). Sincronizado por equipo con dotsync (.hosts/pc/).

local mainMod = "SUPER"
local noctCall = "noctalia msg "
local launchPrefix = "uwsm app -- "

-- Mover ventana a la pantalla/cara 1 o 2
hl.bind(mainMod .. " + SHIFT + 1",                    hl.dsp.window.move({ monitor = MONITOR1 }))
hl.bind(mainMod .. " + SHIFT + 2",                    hl.dsp.window.move({ monitor = MONITOR2 }))


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

-- reemplazado por SUPER+CONTROL+N.

-- (05/10/2026) Mouse Corsair Scimitar. keyd (/etc/keyd/default.conf, copia en ~/.config/hypr/keyd-scimitar.conf)
-- convierte los atajos que manda su memoria en F14..F24 solo para ese mouse; aqui se les da la accion.
-- Se bindea por keycode porque xkb no resuelve los nombres F13-F24: F14=192 ... F24=202.
-- Botones 1/4 = adelante/atras (nativos). Escritorios fijos: 2->ws2, 3->ws3, 5->ws4, 6->ws5.
-- Botones 7/8/9 cambian segun la capa M1/M2/M3 (scripts/mouse-accion.sh). Botones 10/11/12 = capa M1/M2/M3.
local scripts = os.getenv("HOME") .. "/.config/hypr/scripts/"
hl.bind("code:192", function() switchVirtualDesktop(2) end)                         -- boton 2
hl.bind("code:193", function() switchVirtualDesktop(3) end)                         -- boton 3
hl.bind("code:195", function() switchVirtualDesktop(4) end)                         -- boton 5
hl.bind("code:196", function() switchVirtualDesktop(5) end)                         -- boton 6
hl.bind("code:197", hl.dsp.exec_cmd("bash " .. scripts .. "mouse-accion.sh 7"))    -- boton 7
hl.bind("code:198", hl.dsp.exec_cmd("bash " .. scripts .. "mouse-accion.sh 8"))    -- boton 8
hl.bind("code:199", hl.dsp.exec_cmd("bash " .. scripts .. "mouse-accion.sh 9"))    -- boton 9
hl.bind("code:200", hl.dsp.exec_cmd("bash " .. scripts .. "mouse-modo.sh 1"))      -- boton 10 = M1
hl.bind("code:201", hl.dsp.exec_cmd("bash " .. scripts .. "mouse-modo.sh 2"))      -- boton 11 = M2
hl.bind("code:202", hl.dsp.exec_cmd("bash " .. scripts .. "mouse-modo.sh 3"))      -- boton 12 = M3
