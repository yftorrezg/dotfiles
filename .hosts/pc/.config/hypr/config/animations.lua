-- Curvas y animaciones, ver https://wiki.hypr.land/Configuring/Advanced-and-Cool/Animations/
-- (18/10/2026) Más elegantes: escritorios con deslizamiento + desvanecido, ventanas que "brotan".
-- Copia de las de fábrica en el historial de git (dotfiles) si quieres volver.

-- Beziers
hl.curve("easeOutQuint",   { type = "bezier", points = { {0.23, 1},    {0.32, 1}    } })
hl.curve("easeInOutCubic", { type = "bezier", points = { {0.65, 0.05}, {0.36, 1}    } })
hl.curve("linear",         { type = "bezier", points = { {0, 0},       {1, 1}       } })
hl.curve("almostLinear",   { type = "bezier", points = { {0.5, 0.5},   {0.75, 1}    } })
hl.curve("quick",          { type = "bezier", points = { {0.15, 0},    {0.1, 1}     } })
hl.curve("overshoot",      { type = "bezier", points = { {0.5, 0.9}, {0.1, 1.1}     } })
hl.curve("seda",           { type = "bezier", points = { {0.16, 1},    {0.3, 1}     } })  -- arranca rápido, frena suave

-- Springs (muelles: se asientan con un rebote mínimo)
hl.curve("easy",           { type = "spring", mass = 1, stiffness = 500, dampening = 35 })
hl.curve("rubber",         { type = "spring", mass = 1, stiffness = 200,  dampening = 15 })
hl.curve("suave",          { type = "spring", mass = 1, stiffness = 260, dampening = 26 })

-- Animaciones
hl.animation({ leaf = "global",              enabled = true, speed = 3,   bezier = "quick"                          })
hl.animation({ leaf = "windowsIn",           enabled = true, speed = 3,   spring = "suave", style = "popin 85%"     })  -- ventana nueva: crece desde el centro
hl.animation({ leaf = "windowsOut",          enabled = true, speed = 2.5, bezier = "seda",  style = "popin 85%"     })
hl.animation({ leaf = "windowsMove",         enabled = true, speed = 3,   spring = "easy",  style = "slide"         })
hl.animation({ leaf = "fade",                enabled = true, speed = 3,   bezier = "seda"                           })
hl.animation({ leaf = "workspaces",          enabled = true, speed = 4.5, bezier = "seda",  style = "slidefade 18%" })  -- cambio de escritorio
hl.animation({ leaf = "layersIn",            enabled = true, speed = 3,   bezier = "seda",  style = "popin 90%"     })  -- menús, lanzador, avisos
hl.animation({ leaf = "layersOut",           enabled = true, speed = 2.5, bezier = "seda",  style = "fade"          })
hl.animation({ leaf = "specialWorkspaceIn",  enabled = true, speed = 3,   bezier = "seda",  style = "slidefadevert 20%" })
hl.animation({ leaf = "specialWorkspaceOut", enabled = true, speed = 2.5, bezier = "seda",  style = "slidefadevert 20%" })

-- Efecto elegido en SUPER+SHIFT+A → ✨ Efectos (archivo generado; si no existe, queda lo de arriba)
pcall(require, "config.transicion")
