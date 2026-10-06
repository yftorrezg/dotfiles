# ImageGlass con los atajos de Gwenview

ImageGlass 10 (MSIX) guarda su configuración en
`%LOCALAPPDATA%\Packages\DuongDieuPhap.ImageGlass_dhvarhd5k2r8t\LocalCache\Local\ImageGlass\igconfig.json`,
pero solo la escribe cuando cambias algo desde la app. Por eso se configura a mano, una sola vez:
**Configuración (Ctrl+,) → Teclado → editar el atajo de cada acción.** Después de hacerlo, copia
`igconfig.json` a esta carpeta para tenerlo versionado.

| Tecla (como en Gwenview) | Acción de ImageGlass |
|---|---|
| A / D | Ver anterior / Ver siguiente (dejar también ← / →) |
| Q / E | Girar a la izquierda / Girar a la derecha |
| C | Herramienta Recortar |
| X | Mover a la papelera de reciclaje (dejar también Supr) |
| F | Pantalla completa |
| W | Escalar para ajustar |
| Shift+W | Escalar para rellenar |
| T | Mostrar u ocultar la galería (miniaturas) |

Otros ajustes:
- **Ratón → Rueda:** navegar entre imágenes; Ctrl+rueda = zoom (como `MouseWheelBehavior::Browse`).
- **Apariencia:** tema oscuro.
- **Predeterminada:** Configuración de Windows → Aplicaciones → Aplicaciones predeterminadas → ImageGlass, o desde ImageGlass → Configuración → Asociaciones de archivos (incluye webp/avif).

Gwenview tenía además I (barra lateral) y S (modo foco). En ImageGlass equivalen a "información de la imagen" y "sin marco"; asígnalos si los usas.
