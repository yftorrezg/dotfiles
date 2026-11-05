# 🖱️ MX Master 4 · Botones y gestos

> 5 botones × (clic + 4 gestos) + el **anillo radial** del panel háptico. Mantén el botón, mueve el mouse y suelta. Clic = sin mover.

## 🧭 Cómo se lee
Tres botones son **globales** (hacen lo mismo en todo el sistema) y tres **cambian según la app** con foco.

| Botón | Dónde está | Tema | Alcance |
|---|---|---|---|
| Rueda | Clic central | Pantalla y escritorios | Global |
| Superior | Botón plano detrás de la rueda | Ventanas | Global |
| Gestos | Apoyo del pulgar | Lanzadores | Global |
| Atrás | Lateral | Navegar | Por app |
| Adelante | Lateral | Pestañas / Ver | Por app |
| Háptico | Panel con puntitos | **Anillo radial** (12 acciones) | Por app |

💡 Consejo: el gesto no necesita ser largo; unos 2 cm bastan. Las diagonales no hacen nada.

## 🌐 Globales (igual en todo)
| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Rueda | Captura | Pantalla completa | Cerrar ventana (Super+Q) | Escritorio anterior | Escritorio siguiente |
| Superior | Esc | Gemini | ChatGPT | Claude | DeepSeek |
| Gestos | Portapapeles | YouTube | Terminal | Archivos | WhatsApp |

📌 Nota: las IAs y YouTube se abren como ventana de app de Brave; si ya está abierta, la enfoca en vez de abrir otra.

## 🦁 Brave
| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Atrás | Atrás | Seleccionar todo | Enter | Copiar | Pegar |
| Adelante | Adelante | Barra de direcciones | Añadir a marcadores | Recargar página | Buscar en la página |

- `Rueda del pulgar` :: Pestaña anterior / siguiente

## 🎬 mpv
| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Atrás | Video anterior | +30 s | −30 s | −10 s | +10 s |
| Adelante | Video siguiente | Velocidad ×2 | Velocidad ×1.5 | Velocidad +0.1 | Velocidad −0.1 |

- `Rueda del pulgar` :: −5 s / +5 s
💡 Consejo: la lista de videos es la de la tecla Tab de mpv; no muestra la duración (se puede añadir luego).

## 🖼️ Fotos (Gwenview)
| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Atrás | Deshacer | Miniaturas | Abrir en nueva ventana | Copiar | Abrir la carpeta contenedora |
| Adelante | Guardar | Modo foco | Reflejar | Copiar a… | Mover a… |

- `Rueda del pulgar` :: Foto anterior / siguiente
- `Rueda del mouse` :: Ampliar / reducir la imagen

## 📁 Dolphin
| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Atrás | Atrás | Barra de direcciones (F6) | Carpeta superior | Renombrar (F2) | Duplicar (Ctrl+D) |
| Adelante | Adelante | Nueva pestaña | Cerrar pestaña | Pestaña anterior | Pestaña siguiente |

- `Rueda del pulgar` :: Iconos más chicos / más grandes

## 💬 WhatsApp
| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Atrás | Esc | Chat anterior | Chat siguiente | Esc | Buscar |
| Adelante | Chat nuevo | Fijar chat | Archivar | Silenciar | Marcar no leído |

- `Rueda del pulgar` :: Chat anterior / siguiente

⚠️ Cuidado: los atajos de Fijar, Archivar, Silenciar y No leído son los de WhatsApp Web; si alguno no responde, se corrige en el script.

## 🧰 Resto de programas
| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Atrás | Atrás nativo | Inicio | Fin | Alt + ← | Alt + → |
| Adelante | Adelante nativo | Ctrl + T | Ctrl + W | Ctrl + Shift + Tab | Ctrl + Tab |

- `Rueda del pulgar` :: Volumen − / +

## ⚙️ Dónde se cambia
- `~/.config/hypr/scripts/mx-accion.py` :: Tabla PERFILES: aquí vive todo lo de arriba
- `~/.config/hypr/scripts/mx-reglas.py` :: Regenera las reglas de Solaar (solo si cambian los botones)
- `~/.local/state/mx-accion.log` :: Registro de cada acción (para depurar)

📌 Nota: Solaar debe estar corriendo (arranca solo con Hyprland). No guarda perfiles por app en Wayland; por eso el script mira la ventana activa.

## 🎯 Anillo radial (panel háptico)
Mantén el panel háptico → aparece un anillo de **12 acciones del programa con foco** → mueve hacia una (el mouse vibra) → suelta.

| Gesto | Qué hace |
|---|---|
| Soltar sobre una burbuja | Ejecuta esa acción |
| Soltar en el centro | Cancela |
| Burbuja con puntito | Tiene sub-opciones: aleja más el mouse en esa dirección y salen en un arco |
| Toque corto | El anillo queda abierto: elige con clic (clic en el centro = cerrar) |
| Rueda sobre una burbuja | Su ajuste: volumen, zoom, pestañas, velocidad, chat siguiente… |
| Rueda en el centro | Volumen (en cualquier programa) |
| SUPER+ALT+O (mantener) | Lo mismo desde el teclado |

Perfiles: Sistema (global) · Brave · YouTube (+ Video Speed Controller) · WhatsApp · Telegram · mpv · Dolphin · Fotos (Gwenview) · Terminal (kitty) · VS Code.
💡 Para cambiar qué hay en cada uno: `~/.config/hypr/scripts/anillo_apps.py` (y `python3 anillo-tests.py` para comprobar).

