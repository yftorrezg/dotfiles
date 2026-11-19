-- binds_equipo.lua — atajos que dependen del hardware de este equipo: LAPTOP ThinkPad (eDP-1 + Arzopa opcional).
-- Lo cargan los binds comunes (config/binds.lua). Sincronizado por equipo con dotsync (.hosts/laptop/).

local mainMod = "SUPER"
local noctCall = "noctalia msg "
local launchPrefix = "uwsm app -- "

-- Mover ventana a la pantalla/cara 1 o 2
-- LAPTOP: 1 = principal / 2 = secundaria. Con Arzopa mueve a esa pantalla; solo con la
-- interna manda la ventana a la otra "cara" del escritorio actual (ver config/escritorios.lua).
hl.bind(mainMod .. " + SHIFT + 1",                    function() VD.moverVentanaALado(1) end)
hl.bind(mainMod .. " + SHIFT + 2",                    function() VD.moverVentanaALado(2) end)

-- Teclas Fn de la ThinkPad E14 Gen4 (F1-F6 = mute/vol/mic/brillo ya cubiertas arriba;
-- XF86AudioMicMute = F4). Wi-Fi/avión (F8) lo maneja el kernel (rfkill) sin bind.
-- Las de abajo son "por si acaso": si la tecla no emite ese keysym, no pasa nada.
hl.bind("XF86Display",  hl.dsp.exec_cmd(launchPrefix .. "nwg-displays")) -- F7: ajustes de pantallas (Arzopa)
hl.bind("XF86Tools",    hl.dsp.exec_cmd(noctCall .. "settings-toggle"))  -- F9 (engranaje): ajustes de Noctalia
hl.bind("XF86Favorites", hl.dsp.exec_cmd(noctCall .. "panel-toggle control-center")) -- F12 (estrella)


-- "Escritorio virtual": la lógica vive en config/escritorios.lua (tabla global VD),
-- que se adapta sola a "solo la interna" o "interna + Arzopa" (hotplug).
--   Escritorio virtual i = ws i (cara principal) + ws i+NUM_WPM (cara secundaria).
--   Solo interna: SUPER+N va a la cara principal; SUPER+` (tecla bajo Esc) voltea a la secundaria.
--   Con Arzopa: SUPER+N cambia las dos pantallas a la vez (como en la PC).

-- SUPER+Tab: cicla entre las ventanas de las dos caras del escritorio virtual actual.
hl.bind(mainMod .. " + Tab", function() VD.ciclarVentanas() end)

-- Voltear: SUPER+` (tecla bajo Esc). Por keysym: "code:49" no funciona en la config Lua y
-- con gb-extd esa tecla es "muerta" (dead_grave). Con Arzopa: pasa el foco a la otra pantalla.
for _, tecla in ipairs({ "dead_grave", "grave" }) do -- gb+extd da dead_grave; gb normal da grave
    hl.bind(mainMod .. " + " .. tecla, function() VD.voltear() end)
end

-- Ir a la cara/pantalla principal (1) o secundaria (2)
hl.bind(mainMod .. " + ALT + 1", function() VD.enfocarLado(1) end)
hl.bind(mainMod .. " + ALT + 2", function() VD.enfocarLado(2) end)

-- SUPER+1..5: escritorio virtual N
for i = 1, NUM_WPM do
    local key = i % 10
    hl.bind(mainMod .. " + " .. key, function() VD.ir(i) end)
end
-- SUPER+CONTROL+N: mover la ventana enfocada al escritorio N, en la misma cara/pantalla donde está.
-- Tambien sirve para sacar una ventana del special workspace (SUPER+S).
for i = 1, NUM_WPM do
    local key = i % 10
    hl.bind(mainMod .. " + CONTROL + " .. key, function()
        hl.dispatch(hl.dsp.window.move({ workspace = tostring((VD.ladoActual() - 1) * NUM_WPM + i) }))
    end)
end

-- Escritorio virtual siguiente/anterior (todos los monitores a la vez).
-- OJO: el Stream Deck (perfil Escritorios) simula estas teclas, no cambiarlas.
-- (24/09/2026) Quitado SUPER+CTRL+Down (proximo vacio): sigue en el Stream Deck.
hl.bind(mainMod .. " + CONTROL + Right",       function() VD.relativo(1) end)
hl.bind(mainMod .. " + CONTROL + Left",        function() VD.relativo(-1) end)

-- Scroll para cambiar de escritorio virtual (todos los monitores a la vez)
-- (24/09/2026) Quitado SUPER+CTRL+rueda: hacia lo mismo que SUPER+rueda pero invertido.
hl.bind(mainMod .. " + mouse_down",           function() VD.relativo(-1) end)
hl.bind(mainMod .. " + mouse_up",             function() VD.relativo(1) end)

