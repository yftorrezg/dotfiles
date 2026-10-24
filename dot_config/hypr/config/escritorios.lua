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

-- Pantalla secundaria: la primera que no sea la principal (la Arzopa), o nil.
function secondaryMonitor()
    local p = primaryMonitor()
    for _, m in ipairs(monitores()) do
        if m.name ~= p then return m.name end
    end
    return nil
end

local function dispatch(d) hl.dispatch(d) end

-- Índice del escritorio virtual actual (1..N), sea cual sea la cara visible.
function VD.indiceActual()
    local mon = hl.get_active_monitor()
    local ws = mon and mon.active_workspace
    if ws and ws.id >= 1 and ws.id <= 2 * N then
        VD.ultimo = (ws.id > N) and (ws.id - N) or ws.id
    end
    return VD.ultimo
end

-- 1 = cara principal, 2 = cara secundaria (según el ws enfocado)
function VD.ladoActual()
    local mon = hl.get_active_monitor()
    local ws = mon and mon.active_workspace
    if ws and ws.id > N and ws.id <= 2 * N then return 2 end
    return 1
end

-- Ir al escritorio virtual i (SUPER+1..5)
function VD.ir(i)
    VD.ultimo = i
    local p, s = primaryMonitor(), secondaryMonitor()
    if s then
        -- 2 pantallas: cambia las dos sin robar el foco (como en la PC)
        local ms, mp = hl.get_monitor(s), hl.get_monitor(p)
        if ms then ms:set_workspace({ workspace = N + i }) end
        if mp then mp:set_workspace({ workspace = i }) end
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
    local destino = (VD.ladoActual() == 1) and i or (i + N)
    dispatch(hl.dsp.window.move({ workspace = tostring(destino) }))
end

-- Voltear (SUPER+`, gesto 3 dedos arriba/abajo):
--  1 pantalla: sin cara secundaria (solo 5 escritorios) -> no hace nada;
--  2 pantallas: foco a la otra pantalla.
function VD.voltear()
    local p, s = primaryMonitor(), secondaryMonitor()
    if s then
        local mon = hl.get_active_monitor()
        dispatch(hl.dsp.focus({ monitor = (mon and mon.name == s) and p or s }))
    end
end

-- SUPER+ALT+1 / SUPER+ALT+2: ir a la cara/pantalla principal o secundaria.
-- 1 pantalla: no hay cara secundaria, no hace nada.
function VD.enfocarLado(lado)
    local p, s = primaryMonitor(), secondaryMonitor()
    if s then
        dispatch(hl.dsp.focus({ monitor = (lado == 2) and s or p }))
    end
end

-- SUPER+SHIFT+1 / SUPER+SHIFT+2: mandar la ventana a la cara/pantalla principal o secundaria.
-- 1 pantalla: no hay cara secundaria, no hace nada.
function VD.moverVentanaALado(lado)
    local p, s = primaryMonitor(), secondaryMonitor()
    if s then
        dispatch(hl.dsp.window.move({ monitor = (lado == 2) and s or p }))
    end
end

-- Mostrar el escritorio que contiene el ws w y enfocar ese ws (lo usa scripts/app-web.sh)
function VD.mostrarWorkspace(w)
    w = tonumber(w)
    if not w then return end
    local i = (w > N and w <= 2 * N) and (w - N) or w
    if secondaryMonitor() and i >= 1 and i <= N then
        VD.ir(i)
    elseif i >= 1 and i <= N then
        VD.ultimo = i
    end
    dispatch(hl.dsp.focus({ workspace = tostring(w) }))
end

-- SUPER+Tab: cicla entre las ventanas de las dos caras del escritorio virtual actual
function VD.ciclarVentanas()
    local cur = VD.indiceActual()
    local windows = {}
    for _, id in ipairs({ cur, cur + N }) do
        for _, w in ipairs(hl.get_windows({ workspace = id })) do
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
    local p, s = primaryMonitor(), secondaryMonitor()
    if not p then return end
    for _, ws in ipairs(hl.get_workspaces()) do
        local id = ws.id
        if id and id >= 1 and id <= 2 * N and not ws.special then
            local destino = (id > N and s) or p
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
hl.on("monitor.added", programarRedistribucion)
hl.on("monitor.removed", function()
    -- Seguridad: si se desconecta la Arzopa con la tapa cerrada y la interna apagada,
    -- volver a encender la interna para no quedar sin pantalla.
    if #monitores() == 0 then hl.monitor(INTERNAL_MONITOR_SPEC) end
    programarRedistribucion()
end)

-- Tapa (switch "Lid Switch" de hyprctl devices). "on" = cerrada.
hl.bind("switch:on:Lid Switch", function()
    if TAPA_APAGA_INTERNA and secondaryMonitor() then
        hl.monitor({ output = MONITOR1, disabled = true })
    end
end, { locked = true })
hl.bind("switch:off:Lid Switch", function()
    hl.monitor(INTERNAL_MONITOR_SPEC)
end, { locked = true })
