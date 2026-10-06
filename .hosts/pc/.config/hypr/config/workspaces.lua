-- Workspace rules wiki https://wiki.hypr.land/Configuring/Basics/Workspace-Rules/
-- Add your workspace rules here. Increment the workspace number as you go. Do not have duplicate workspaces.
-- (25/09/2026) Quitado default=true: hacía que al iniciar todo se abriera en "gaming" (sin atajo para llegar).
hl.workspace_rule({ workspace = "name:gaming", monitor = PRIMARY_MONITOR })
hl.workspace_rule({ workspace = "name:estudio", monitor = PRIMARY_MONITOR })
-- Generadas a partir de NUM_WPM: MONITOR1 se queda con 1..NUM_WPM,
-- MONITOR2 con NUM_WPM+1..2*NUM_WPM (mismo esquema que usa binds.lua
-- para el "escritorio virtual" sincronizado entre monitores).
for i = 1, NUM_WPM do
    hl.workspace_rule({ workspace = tostring(i), monitor = MONITOR1, default = true, persistent = true })
end
for i = 1, NUM_WPM do
    hl.workspace_rule({ workspace = tostring(NUM_WPM + i), monitor = MONITOR2, default = true, persistent = true })
end

-- For other layouts such as scrolling, see example below
-- hl.workspace_rule({ workspace = "1", monitor = MONITOR1, default = true, persistent = true, layout = scroling })
