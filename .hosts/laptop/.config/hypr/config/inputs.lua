-- Input configuration (LAPTOP ThinkPad E14 Gen4)

hl.config({
    input = {
        -- Teclado físico inglés UK. Variante "extd" (= "UK extendido" de Windows): igual que gb,
        -- pero con AltGr (Alt derecha) da los caracteres del español SIN cambiar de distribución:
        --   AltGr+a/e/i/o/u = á é í ó ú (con Shift: Á É Í Ó Ú)
        --   AltGr+# y luego n = ñ (# es la tecla junto a Enter; tilde muerta)
        --   AltGr+2 y luego u = ü     AltGr+Shift+1 = ¡     AltGr+Shift+- = ¿     AltGr+4 = €
        -- Todo lo demás (símbolos, £, @ en Shift+') queda como en el teclado impreso.
        -- Ojo: la tecla ` (bajo Esc) pasa a ser "acento grave muerto"; por eso el atajo de
        -- "voltear" (SUPER+`) se define por keycode en binds.lua.
        kb_layout  = "gb",
        kb_variant = "extd",
        kb_options = "",

        -- Repetición más ágil que el default (600 ms / 25 por s)
        repeat_delay = 300,
        repeat_rate  = 35,

        accel_profile = "flat", -- mouse (M720): sin aceleración, como en la PC. El touchpad va aparte abajo.

        touchpad = {
            natural_scroll       = true,  -- dos dedos hacia arriba = el contenido sube (como el móvil)
            tap_to_click         = true,  -- tocar = clic (2 dedos = derecho, 3 = medio)
            disable_while_typing = true,  -- evita clics fantasma con la palma
            tap_and_drag         = true,  -- doble toque y arrastrar = seleccionar/mover
            -- clickfinger_behavior = true, -- (desactivado) clic físico con 2 dedos = derecho;
            -- se deja el default: esquina inferior derecha = clic derecho.
        },
    },
    gestures = {
        workspace_swipe_create_new = false,
    },
    -- Uncomment the section below to enable software cursors; this can help with cursor display or behavior issues
    -- cursor = {
    --     no_hardware_cursors = 1,
    -- },
})

-- Touchpad (y TrackPoint si lo hubiera) con aceleración adaptativa: con "flat" se siente lento.
-- Nombres tomados de `hyprctl devices` en la laptop.
hl.device({ name = "elan-touchpad",   accel_profile = "adaptive" })
hl.device({ name = "elan-trackpoint", accel_profile = "adaptive" })

-- Gestos del touchpad (LAPTOP). Ninguno es destructivo: se QUITÓ "3 dedos abajo = cerrar ventana"
-- (se disparaba sin querer); para cerrar: SUPER+Q.
--   3 dedos izquierda/derecha = escritorio virtual siguiente/anterior (igual que SUPER+CTRL+→/←)
--   3 dedos arriba/abajo      = voltear a la cara secundaria (chats, Drive) y volver (= SUPER+`)
--   4 dedos arriba            = pantalla completa
--   4 dedos abajo             = ventana flotante
hl.gesture({ fingers = 3, direction = "left",  action = function() VD.relativo(1) end })
hl.gesture({ fingers = 3, direction = "right", action = function() VD.relativo(-1) end })
hl.gesture({ fingers = 3, direction = "up",    action = function() VD.voltear() end })
hl.gesture({ fingers = 3, direction = "down",  action = function() VD.voltear() end })
hl.gesture({ fingers = 4, direction = "up",    action = "fullscreen" })
hl.gesture({ fingers = 4, direction = "down",  action = "float" })
