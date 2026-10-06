---
name: gwenview-tema-atajos
description: Gwenview oscuro (UiSettings ColorScheme=noctalia) y atajos personalizados en kxmlgui5; plantilla qt de Noctalia corregida.
metadata:
  type: project
---
Configurado 2026-09-28 en Hyprland + Noctalia (sin Plasma):
- Gwenview ignora qt6ct: su KColorSchemeManager busca "Noctalia" (kdeglobals) pero el archivo es noctalia.colors → cae a Breeze claro. Fix: `~/.config/gwenviewrc` [UiSettings] ColorScheme=noctalia. Otras apps KDE con menú "Esquema de color" (Okular, Kate…) podrían necesitar lo mismo.
- Plantilla qt de Noctalia fijaba light/mid a blanco/gris → bordes claros. Sustituida por plantilla de usuario `~/.config/noctalia/templates/qtct-oscuro.conf` ([theme.templates.user.qt-oscuro] en config.toml, "qt" quitado de builtin_ids).
- Rueda del ratón: [ImageView] MouseWheelBehavior=MouseWheelBehavior::Browse (navega; Ctrl+rueda = zoom).
- Atajos extra en `~/.local/share/kxmlgui5/gwenview/gwenviewui.rc` (ActionProperties): A/D ant/sig, Q/E rotar, C recortar, R redimensionar, X papelera, F pantalla completa, W ajustar, Shift+W rellenar, T miniaturas, I barra lateral, S modo foco. Si Gwenview sube la versión del .rc (71), revisar.
- Hyprland usa config Lua: `hyprctl dispatch` con sintaxis vieja falla; para probar teclas usar `ydotool key` (ojo: combos con Ctrl dejaron teclas "pegadas" en pruebas).
Relacionado: [[auto-captura-cursos]]
