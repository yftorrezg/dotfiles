-- Workspace rules wiki https://wiki.hypr.land/Configuring/Basics/Workspace-Rules/
-- (25/09/2026) Quitado default=true: hacía que al iniciar todo se abriera en "gaming" (sin atajo para llegar).
hl.workspace_rule({ workspace = "name:gaming", monitor = PRIMARY_MONITOR })
hl.workspace_rule({ workspace = "name:estudio", monitor = PRIMARY_MONITOR })

-- LAPTOP: cara principal 1..NUM_WPM siempre en la interna.
for i = 1, NUM_WPM do
    hl.workspace_rule({ workspace = tostring(i), monitor = MONITOR1, default = (i == 1), persistent = true })
end
-- Cara secundaria NUM_WPM+1..2*NUM_WPM: en la Arzopa si está conectada al cargar la config;
-- si no, sin monitor fijo (viven en la interna). Al conectar/desconectar en caliente las
-- reubica config/escritorios.lua (VD.redistribuir), así que aquí no se fija un nombre.
local sec = secondaryMonitor and secondaryMonitor() or nil
for i = 1, NUM_WPM do
    local regla = { workspace = tostring(NUM_WPM + i), persistent = true }
    if sec then
        regla.monitor = sec
        regla.default = (i == 1)
    end
    hl.workspace_rule(regla)
end
