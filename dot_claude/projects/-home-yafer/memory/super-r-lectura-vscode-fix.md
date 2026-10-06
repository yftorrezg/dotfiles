---
name: super-r-lectura-vscode-fix
description: "Atajo SUPER+R (leer selección en voz alta) usa ydotool en vez de wtype para que funcione en webviews de VSCode; \"no lee\" casi siempre es el mouse fuera de la selección, no un bug."
metadata: 
  node_type: memory
  type: project
  originSessionId: c05b7e2d-aa22-4771-a96f-60360e106ec8
  modified: 2026-09-01T19:43:31.945Z
---

El atajo SUPER+R (`~/.config/hypr/scripts/leer-seleccion.sh`, bind en `~/.config/hypr/config/binds.lua`) lee en voz alta el texto seleccionado con el mouse, vía Piper/edge-tts. Para apps Chromium/Electron (VSCode, Brave) que no exponen la selección como primary selection en Wayland, el script simula Ctrl+C y lee el portapapeles normal.

Ese Ctrl+C simulado usa **`ydotool`** (inyecta el evento a nivel de kernel por `/dev/uinput`), no `wtype` (protocolo `virtual-keyboard` de Wayland). `wtype` no llega a los **webviews** de VSCode (ej. Markdown Preview, un iframe de Chromium embebido) — se verificó en vivo: con texto seleccionado en el preview, ni `wtype ctrl+c` ni `wtype ctrl+a`+`ctrl+c` dejaban nada en el portapapeles, pero `ydotool key 29:1 46:1 46:0 29:0` sí. `ydotool.service` (systemd --user) ya está habilitado y corriendo, así que no hace falta arrancarlo a mano.

El tope de espera del copy quedó en 300ms (15 intentos × 20ms), el valor original — se probó subirlo a 1s porque a veces el copy tardaba más de 300ms (~400ms en un caso observado), pero el usuario prefirió mantener 300ms por velocidad de dictado y descartó que ese fuera el problema real.

**Why:** la mayoría de los reportes de "apreté Super+R y no leyó nada" (real, no notificación de error) resultaron ser el mouse fuera del área de la selección de texto en el momento de apretar el atajo, no un bug del script — el usuario lo confirmó explícitamente después de probar prestando atención a la posición del mouse.

**How to apply:** si vuelve a fallar la lectura en VSCode (u otra app Electron/Chromium) specíficamente:
1. Primero descartar que el mouse esté fuera de la selección al apretar el atajo (causa más común).
2. Si de verdad es un bug de copy, revisar que sea `ydotool` (no `wtype`) el que dispara el Ctrl+C simulado en `leer-seleccion.sh`, y que `ydotool.service --user` esté activo.
3. Si el copy tarda más de 300ms de forma consistente (no solo un pico aislado), recién ahí considerar subir el tope de polling — pero el usuario ya lo rechazó una vez por preferir velocidad, así que preguntar antes de volver a subirlo.
