-- Escritorios virtuales dinámicos (laptop + Arzopa opcional) — 2026-10
--
-- Modelo (igual que en la PC): escritorio virtual i = ws i ("cara principal")
-- + ws i+NUM_WPM ("cara secundaria"). Con 1 pantalla solo se usa la principal (1..5).
--
--  * Solo la interna (eDP-1): 5 escritorios (ws 1..5). No hay cara secundaria:
--    "voltear" no hace nada y los chats (WhatsApp/Telegram) van al ws 1 (junto a redes).
--  * Con la Arzopa conectada (cualquier nombre: HDMI-A-1, DP-1, DP-2...): igual que la
--    PC, eDP-1 = ws 1..5 y la Arzopa = ws 6..10; SUPER+N cambia ambas. "Voltear" pasa
--    el foco a la otra pantalla.
--  * Hotplug: al conectar/desconectar la Arzopa (o recargar la config) se reubican los
--    ws 6..10 solos (eventos monitor.added / monitor.removed).
--
-- Las funciones van en la tabla global VD para poder llamarlas desde binds.lua,
-- inputs.lua (gestos), scripts (hyprctl eval 'VD.mostrarWorkspace(6)') y el Stream Deck.

VD = VD or {}
VD.ultimo = VD.ultimo or 1   -- último escritorio virtual (1..NUM_WPM) usado

local N = NUM_WPM

local function monitores()
    local ok, ms = pcall(hl.get_monitors)
    if not ok or type(ms) ~= "table" then return {} end
    local activos = {}
    for _, m in ipairs(ms) do
        if not m.is_mirror then activos[#activos + 1] = m end
    end
    return activos
end

-- Pantalla principal: la interna si está activa; si no (tapa cerrada con Arzopa), la primera que haya.
function primaryMonitor()
    local ms = monitores()
    for _, m in ipairs(ms) do
        if m.name == MONITOR1 then return m.name end
    end
    return ms[1] and ms[1].name or nil
end

-- Lista ordenada de pantallas: la principal primero, el resto por nombre (orden estable).
-- Pantalla k (1..M) = ws (k-1)*N+1 .. k*N. Se adapta sola a cuántas haya conectadas.
local function listaMonitores()
    local p = primaryMonitor()
    local otros = {}
    for _, m in ipairs(monitores()) do
        if m.name ~= p then otros[#otros + 1] = m.name end
    end
    table.sort(otros)
    if p then table.insert(otros, 1, p) end
    return otros
end
VD.lista = listaMonitores

-- Pantalla secundaria: la primera que no sea la principal, o nil.
function secondaryMonitor()
    return listaMonitores()[2]
end

-- set_workspace cambió de firma entre versiones de Hyprland (0.56: tabla, 0.57: número): prueba las dos.
local function setWs(m, n)
    if not pcall(m.set_workspace, m, n) then pcall(m.set_workspace, m, { workspace = n }) end
end
local function dispatch(d) hl.dispatch(d) end

-- Índice del escritorio virtual actual (1..N), sea cual sea la cara visible.
function VD.indiceActual()
    local mon = hl.get_active_monitor()
    local ws = mon and mon.active_workspace
    if ws and ws.id >= 1 and ws.id <= math.max(#listaMonitores(), 2) * N then
        VD.ultimo = ((ws.id - 1) % N) + 1
    end
    return VD.ultimo
end

-- Número de pantalla (1 = principal, 2.. = las demás) según el ws enfocado
function VD.ladoActual()
    local mon = hl.get_active_monitor()
    local ws = mon and mon.active_workspace
    if ws and ws.id >= 1 and ws.id <= #listaMonitores() * N then
        return math.floor((ws.id - 1) / N) + 1
    end
    return 1
end

-- Ir al escritorio virtual i (SUPER+1..5)
function VD.ir(i)
    VD.ultimo = i
    local lista = listaMonitores()
    if #lista >= 2 then
        -- 2 o más pantallas: cambia todas sin robar el foco; la principal al final
        for k = #lista, 1, -1 do
            local m = hl.get_monitor(lista[k])
            if m then setWs(m, (k - 1) * N + i) end
        end
    else
        -- 1 pantalla: siempre a la cara principal del escritorio i
        dispatch(hl.dsp.focus({ workspace = tostring(i) }))
    end
end

function VD.relativo(delta)
    local cur = VD.indiceActual()
    VD.ir(((cur - 1 + delta) % N) + 1)
end

-- Mover la ventana enfocada al escritorio virtual siguiente/anterior (misma cara) e ir con ella.
-- Lo usa el gesto de 4 dedos izquierda/derecha del touchpad (inputs.lua).
function VD.moverVentanaRelativo(delta)
    local i = ((VD.indiceActual() - 1 + delta) % N) + 1
    local destino = (VD.ladoActual() - 1) * N + i
    dispatch(hl.dsp.window.move({ workspace = tostring(destino) }))
end

-- Voltear (SUPER+`, gesto 3 dedos arriba/abajo):
--  1 pantalla: sin cara secundaria (solo 5 escritorios) -> no hace nada;
--  2 pantallas: foco a la otra pantalla.
function VD.voltear()
    local lista = listaMonitores()
    if #lista >= 2 then
        local mon = hl.get_active_monitor()
        local idx = 0
        for k, nombre in ipairs(lista) do
            if mon and mon.name == nombre then idx = k break end
        end
        dispatch(hl.dsp.focus({ monitor = lista[(idx % #lista) + 1] }))
    end
end

-- SUPER+ALT+1 / SUPER+ALT+2: ir a la cara/pantalla principal o secundaria.
-- 1 pantalla: no hay cara secundaria, no hace nada.
function VD.enfocarLado(lado)
    local lista = listaMonitores()
    if #lista >= 2 then
        dispatch(hl.dsp.focus({ monitor = lista[lado] or lista[1] }))
    end
end

-- SUPER+SHIFT+1 / SUPER+SHIFT+2: mandar la ventana a la cara/pantalla principal o secundaria.
-- 1 pantalla: no hay cara secundaria, no hace nada.
function VD.moverVentanaALado(lado)
    local lista = listaMonitores()
    if #lista >= 2 then
        dispatch(hl.dsp.window.move({ monitor = lista[lado] or lista[1] }))
    end
end

-- Mostrar el escritorio que contiene el ws w y enfocar ese ws (lo usa scripts/app-web.sh)
function VD.mostrarWorkspace(w)
    w = tonumber(w)
    if not w then return end
    local i = (w >= 1 and w <= math.max(#listaMonitores(), 2) * N) and (((w - 1) % N) + 1) or nil
    if i and secondaryMonitor() then
        VD.ir(i)
    elseif i then
        VD.ultimo = i
    end
    dispatch(hl.dsp.focus({ workspace = tostring(w) }))
end

-- SUPER+Tab: cicla entre las ventanas de las dos caras del escritorio virtual actual
function VD.ciclarVentanas()
    local cur = VD.indiceActual()
    local windows = {}
    for k = 0, math.max(#listaMonitores(), 1) - 1 do
        for _, w in ipairs(hl.get_windows({ workspace = cur + k * N })) do
            windows[#windows + 1] = w
        end
    end
    if #windows < 2 then return end
    table.sort(windows, function(a, b) return a.stable_id < b.stable_id end)
    local active = hl.get_active_window()
    local idx = 1
    if active then
        for k, w in ipairs(windows) do
            if w.address == active.address then idx = k break end
        end
    end
    dispatch(hl.dsp.focus({ window = windows[(idx % #windows) + 1] }))
end

-- Reubica los ws 1..N en la principal y N+1..2N en la secundaria (o en la principal si no hay).
function VD.redistribuir()
    local lista = listaMonitores()
    local p, s = lista[1], lista[2]
    if not p then return end
    for _, ws in ipairs(hl.get_workspaces()) do
        local id = ws.id
        if id and id >= 1 and id <= 8 * N and not ws.special then
            local destino = lista[math.floor((id - 1) / N) + 1] or p
            if ws.monitor and ws.monitor.name ~= destino then
                dispatch(hl.dsp.workspace.move({ workspace = tostring(id), monitor = destino }))
            end
        end
    end
    if s then VD.ir(VD.ultimo or 1) end
end

-- Pequeña espera: al conectar, el monitor tarda un instante en estar listo.
local function programarRedistribucion()
    VD._timer = hl.timer(function() VD.redistribuir() end, { timeout = 500, type = "oneshot" })
end

-- Spec de la pantalla interna (la usan monitors.lua y el manejo de la tapa)
INTERNAL_MONITOR_SPEC = { output = MONITOR1, mode = "preferred", position = "0x0", scale = INTERNAL_SCALE }

hl.on("hyprland.start", programarRedistribucion)
hl.on("config.reloaded", programarRedistribucion)

-- Hotplug: al conectar/desconectar un monitor, recargar la config para que se adapte sola
-- (1 pantalla = 5 escritorios + chats en ws 1; 2 pantallas = 10 + chats en ws 6).
-- La recarga re-evalúa windowrules/workspaces con el nuevo número de monitores.
local function recargarTrasHotplug()
    hl.timer(function()
        -- Seguridad: si al desconectar quedó sin monitores (tapa cerrada), reencender la interna.
        if #monitores() == 0 then hl.monitor(INTERNAL_MONITOR_SPEC) end
        hl.exec_cmd("hyprctl reload")
    end, { timeout = 500, type = "oneshot" })
end

hl.on("monitor.added", recargarTrasHotplug)
hl.on("monitor.removed", recargarTrasHotplug)

-- Tapa (switch "Lid Switch" de hyprctl devices). "on" = cerrada.
hl.bind("switch:on:Lid Switch", function()
    if TAPA_APAGA_INTERNA and secondaryMonitor() then
        hl.monitor({ output = MONITOR1, disabled = true })
    end
end, { locked = true })
hl.bind("switch:off:Lid Switch", function()
    hl.monitor(INTERNAL_MONITOR_SPEC)
end, { locked = true })
