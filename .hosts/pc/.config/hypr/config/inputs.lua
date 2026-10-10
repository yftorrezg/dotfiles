-- Input configuration

hl.config({
    input = {
        -- sensitivity = -0.25,
        accel_profile = "flat",
    },
    -- Uncomment the section below to enable software cursors; this can help with cursor display or behavior issues
    -- cursor = {
    --     no_hardware_cursors = 1,
    -- },
})

-- (09/10/2026) El Stream Deck XL aparece como "teclado" y al pulsar cualquier tecla manda KEY_UNKNOWN;
-- Hyprland lo trataba como si se apretaran a la vez todos los atajos F14..F24 del mouse Scimitar
-- (abría estudiar, Telegram, Instagram, YouTube...). El deck funciona por hidraw con OpenDeck, así que
-- se le quitan los atajos a ese dispositivo.
hl.device({ name = "elgato-stream-deck-xl", keybinds = false })

hl.gesture({ fingers = 4, direction = "horizontal", action = "workspace" })
hl.gesture({ fingers = 3, direction = "down",       action = "close" })
hl.gesture({ fingers = 3, direction = "up",         action = "fullscreen" })
hl.gesture({ fingers = 3, direction = "left",       action = "float" })
