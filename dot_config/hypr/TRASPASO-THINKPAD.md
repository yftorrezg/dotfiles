# Traspaso Surface → ThinkPad (24/10/2026)

Nota de contexto para OpenCode (u otro agente) cuando se ejecute **EN la ThinkPad** (equipo `laptop`).
Objetivo: dejar la ThinkPad con el mismo comportamiento dinámico de escritorios + gestos de trackpad
que la Surface, pero **adaptado a su hardware** (touchpad Elan, teclado gb+extd, 1 pantalla + Arzopa opcional).

## Ya viene de GitHub (archivos COMUNES — NO tocar)

Correr `dotsync` primero para traerlos. Ya quedaron listos en la Surface:

- `config/escritorios.lua` → dinámico: **1 pantalla = 5 escritorios, 2 pantallas = 10**.
  `VD.voltear()` ya **NO hace nada en 1 pantalla**. Hotplug (conectar/desconectar monitor) recarga la
  config sola (`hl.on("monitor.added"/"monitor.removed")`). Incluye `VD.moverVentanaRelativo(delta)`.
- `config/windowrules.lua` → WhatsApp/Telegram al **ws 1** (1 pantalla) / **ws 6** (2 pantallas).
  El chequeo está protegido con `if secondaryMonitor and ... then` para no romper la PC (que NO carga escritorios.lua).
- `scripts/app-web.sh` → mismo comportamiento (cuenta monitores con `hyprctl monitors -j`).

## A adaptar EN la ThinkPad (archivos POR-EQUIPO)

### 1. `config/inputs.lua` — gestos del trackpad

Reemplazar el bloque de `hl.gesture(...)` por:

```lua
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
```

> Mantener la línea `hl.device({ name = "elan-touchpad", accel_profile = "adaptive" })` tal cual.

### 2. `config/workspaces.lua` — 5 puntitos en 1 pantalla

En el bucle de la cara secundaria (ws 6-10), cambiar:

```lua
local regla = { workspace = tostring(NUM_WPM + i), persistent = true }
```
por
```lua
local regla = { workspace = tostring(NUM_WPM + i), persistent = (sec ~= nil) }
```

## Gotchas (errores ya aprendidos en la Surface)

- En gestos usar `hl.exec_cmd` (NO `hl.dsp.exec_cmd`: solo "prepara" el dispatcher, no ejecuta).
- Ctrl+W con ydotool: `29` = Ctrl izquierdo, `17` = W. El daemon `ydotoold` debe estar corriendo.
- `secondaryMonitor()` solo existe si `escritorios.lua` está cargado (en la PC NO existe; por eso
  `windowrules.lua` usa el guard `if secondaryMonitor and ...`).
- **Adaptar a la ThinkPad**: si el touchpad Elan dispara gestos sin querer, cambia los "abajo"
  (cerrar pestaña/ventana) por otra dirección o quítalos.

## Verificación

```bash
luac -p config/*.lua && hyprctl reload && hyprctl configerrors   # debe quedar vacío
dotsync subir
```
