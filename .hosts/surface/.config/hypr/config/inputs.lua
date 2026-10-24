-- Input configuration (SURFACE Pro 6 — Type Cover)

hl.config({
    input = {
        -- Teclado en español (es). Si el Type Cover físico es US y prefieres las tildes
        -- sin cambiar de distribución, dímelo y lo paso a us+intl (como el gb+extd de la ThinkPad).
        kb_layout  = "es",
        kb_variant = "",
        kb_options = "",

        -- Repetición más ágil que el default (600 ms / 25 por s)
        repeat_delay = 300,
        repeat_rate  = 35,

        accel_profile = "flat", -- mouse: sin aceleración. El touchpad va aparte abajo.

        touchpad = {
            natural_scroll       = true,  -- dos dedos hacia arriba = el contenido sube (como el móvil)
            tap_to_click         = true,  -- tocar = clic (2 dedos = derecho, 3 = medio)
            disable_while_typing = true,  -- evita clics fantasma con la palma
            tap_and_drag         = true,  -- doble toque y arrastrar = seleccionar/mover
        },
    },
    gestures = {
        workspace_swipe_create_new = false,
    },
})

-- Touchpad del Type Cover con aceleración adaptativa: con "flat" se siente lento.
-- Nombre tomado de `hyprctl devices` en la Surface.
hl.device({ name = "microsoft-surface-type-cover-touchpad", accel_profile = "adaptive" })

-- Gestos del touchpad (SURFACE). 3 dedos = navegación; 4 dedos = gestión de ventanas.
--   3 dedos izquierda/derecha = escritorio virtual siguiente/anterior (igual que SUPER+CTRL+→/←)
--   3 dedos arriba            = abrir terminal (1 pantalla) / voltear monitor (2 pantallas, HDMI)
--   3 dedos abajo             = cerrar pestaña (Ctrl+W)
--   4 dedos izquierda/derecha = mover ventana al escritorio virtual siguiente/anterior
--   4 dedos arriba            = pantalla completa
--   4 dedos abajo             = cerrar ventana
hl.gesture({ fingers = 3, direction = "left",  action = function() VD.relativo(1) end })
hl.gesture({ fingers = 3, direction = "right", action = function() VD.relativo(-1) end })
hl.gesture({ fingers = 3, direction = "up",    action = function()
    if secondaryMonitor() then VD.voltear() else hl.exec_cmd("uwsm app -- " .. TERMINAL) end
end })
hl.gesture({ fingers = 3, direction = "down",  action = function() hl.exec_cmd("ydotool key 29:1 17:1 17:0 29:0") end }) -- Ctrl+W: cerrar pestaña
hl.gesture({ fingers = 4, direction = "left",  action = function() VD.moverVentanaRelativo(1) end })
hl.gesture({ fingers = 4, direction = "right", action = function() VD.moverVentanaRelativo(-1) end })
hl.gesture({ fingers = 4, direction = "up",    action = "fullscreen" })
hl.gesture({ fingers = 4, direction = "down",  action = "close" })
