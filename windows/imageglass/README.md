# ImageGlass con los atajos de Gwenview

Se instala la versión **MSI** oficial (la MSIX de winget no se registra como visor de imágenes ni
guarda su configuración en un archivo). Configuración: `%LOCALAPPDATA%\ImageGlass\igconfig.json`.

`menu-hotkeys.json` es el bloque `MenuHotkeys` con los atajos de Gwenview; `bootstrap.ps1` lo aplica
si `igconfig.json` todavía tiene `"MenuHotkeys": {}`.

| Tecla | Acción |
|---|---|
| A / D | Imagen anterior / siguiente (también ← → y RePág/AvPág) |
| Q / E | Girar a la izquierda / derecha |
| C | Herramienta Recortar |
| X | Mover a la papelera (también Supr) |
| F | Pantalla completa (también F11) |
| W / Shift+W | Escalar para ajustar / para rellenar |
| T | Mostrar u ocultar la galería |

No portados: R (redimensionar), I (barra lateral) y S (modo foco), sin acción equivalente.
Rueda del ratón = navegar: configurar en Configuración → Ratón.
Tras instalar: Configuración de Windows → Aplicaciones predeterminadas → ImageGlass para cada formato.
