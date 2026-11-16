# 🖱️ Mouse y Stream Deck · Botones, capas y teclas

> Lo que hace cada botón del mouse Corsair Scimitar y del MX Master 4, y cómo el Stream Deck manda atajos. El MX Master 4 tiene su hoja propia (20) con todos los gestos.

## 🧭 Resumen en 30 segundos

Hay tres aparatos y cada uno trabaja distinto:

| Aparato | Cómo manda acciones | Hoja |
|---|---|---|
| **Corsair Scimitar** | Su memoria manda `CTRL+C`, `F11`… y **keyd** los convierte en `F14`…`F24`. Hyprland decide la acción | Esta (abajo) |
| **MX Master 4** | Gestos y anillo radial por programa | 20 |
| **Stream Deck** | Botones que simulan atajos o ejecutan scripts (OpenDeck) | Abajo |

🧠 Concepto: el Scimitar tiene **capas** (M1, M2, M3). Los botones 7, 8 y 9 hacen cosas distintas según la capa en la que estés; los demás siempre hacen lo mismo.

## 🐭 Scimitar: botones fijos (los 3 modos)

Los botones van en cuadrícula: `1 2 3 / 4 5 6 / 7 8 9 / 10 11 12`.

| Botón | Qué hace | Cómo llega a Hyprland |
|---|---|---|
| 1 / 4 | Adelante / atrás (nativos) | Sin cambios |
| 2 | Escritorio 2 | `F14` |
| 3 | Escritorio 3 | `F15` |
| 5 | Escritorio 4 | `F17` |
| 6 | Escritorio 5 | `F18` |
| 10 | Cambiar a capa **M1** | `F22` |
| 11 | Cambiar a capa **M2** | `F23` |
| 12 | Cambiar a capa **M3** | `F24` |

🧠 Concepto: por qué `F14`…`F24`: son teclas que casi ningún teclado usa, así que no chocan con nada. Hyprland las liga por **código de tecla** (`code:192`…`code:202`), porque con el teclado en `us` no reconoce sus nombres.

## 🧭 Scimitar: botones 7, 8 y 9 según la capa

| Botón | M1 Estudio | M2 Programación | M3 Redes |
|---|---|---|---|
| 7 | Leer la selección en voz alta (`SUPER + R`) | Guardar (`Ctrl + S`) | YouTube |
| 8 | Captura solo al portapapeles (`SUPER + SHIFT + S`) | Abrir archivo (`Ctrl + P`) | Telegram |
| 9 | Modo estudiar (`SUPER + I`) | Terminal (Ctrl + acento invertido) | Instagram |

💡 Consejo: el modo actual se guarda, así que si cambias a M2 y reinicias, sigue en M2. Revísalo en la configuración de capas antes de usar 7/8/9 en clase.

## ⌨️ Scimitar: botones especiales (keyd)

| Botón | Lo que manda la memoria | Se convierte en |
|---|---|---|
| 2 | `Ctrl + C` | `F14` (escritorio 2) |
| 5 | `Ctrl + V` | `F17` (escritorio 4) |
| 10 | `Ctrl + W` | `F22` (capa M1) |
| 3 | `Ctrl + Win + ←` | `F15` (escritorio 3) |
| 6 | `Ctrl + Win + →` | `F18` (escritorio 5) |
| 7 | `Ctrl + Shift + Q` | `F19` (botón 7) |
| 8 | `Enter` | `F20` (botón 8) |
| 9 | `Supr` | `F21` (botón 9) |
| 11 | `F11` | `F23` (capa M2) |
| 12 | `Alt + F4` | `F24` (capa M3) |

⚠️ Cuidado: el botón 10 manda `Ctrl+W`, pero dentro de keyd **no** cierra pestañas: lo convierte en `F22`. Si cambias la memoria del mouse, cambia también `keyd-scimitar.conf`.

## 🎛️ Stream Deck

El Stream Deck usa **OpenDeck**. Cada botón puede simular un atajo o ejecutar un script (`Run Command`).

| Qué hace un botón | Cómo se configura |
|---|---|
| Simula un atajo (p. ej. escritorios) | Acción de tecla en OpenDeck |
| Ejecuta un script | `Run Command` apuntando a `scripts/` |
| Cambia de perfil (p. ej. Escritorios) | Perfiles de OpenDeck |

⚠️ Cuidado: el perfil **Escritorios** simula teclas de escritorio. Si cambias un atajo de Hyprland, revisa ese perfil también.

🧠 Concepto: como el deck simula atajos, un botón del deck **es** un atajo más. Si cambias el atajo en `binds.lua`, el botón deja de funcionar hasta que lo actualices en OpenDeck.

## 📚 Dónde está cada cosa

| Qué | Dónde |
|---|---|
| Acciones de los botones 7/8/9 | `~/.config/hypr/scripts/mouse-accion.sh` |
| Mapa keyd del Scimitar | `~/.config/hypr/keyd-scimitar.conf` (copia en `/etc/keyd/default.conf`) |
| Bindings de escritorios y mouse | `~/.config/hypr/config/binds_equipo.lua` |
| Gestos del MX Master 4 | Hoja 20 |

## 🧠 Practica

::: desplegable 🧩 Estoy en M2 y pulso el botón 8. ¿Qué pasa?
Abre el **archivo** en VS Code (`Ctrl + P`). En M1, el mismo botón hace captura al portapapeles.
:::

::: desplegable 🧩 ¿Cómo voy al escritorio 4 con el mouse?
Botón 5. Lo convierte keyd en `F17`, y Hyprland cambia al escritorio 4 fijo.
:::

::: desplegable 🧩 ¿Por qué el botón 10 no cierra pestañas?
Porque keyd lo convierte en `F22`, que Hyprland usa para cambiar a la capa M1. Cerrar pestañas sería `Ctrl+W` directo, sin pasar por keyd.
:::

> 📌 Nota: el documento viejo `~/Documentos/atajos-y-mouse.md` (05/10) tiene partes desactualizadas (por ejemplo, el botón 8 de M1). Esta hoja sigue el código actual de `mouse-accion.sh` y `keyd-scimitar.conf`.
