-- Hyprland default apps

TERMINAL     = "kitty"
FILE_MANAGER = "dolphin"
BROWSER      = "brave"
EDITOR       = "gnome-text-editor --new-window"
CALCULATOR   = "gnome-calculator"

-- Monitores (SURFACE Pro 6)
-- MONITOR1 = pantalla interna (siempre). Un externo (Mini DisplayPort = DP-x) NO se fija
-- aquí: se resuelve en tiempo real con secondaryMonitor() (ver config/escritorios.lua).
MONITOR1 = "eDP-1"
MONITOR2 = ""
MONITOR3 = ""
PRIMARY_MONITOR = MONITOR1

-- Escala de la interna 12.3" 2736x1824 (~267 ppi): 2.0 -> 1368x912 lógicos (HiDPI, nítido).
INTERNAL_SCALE = 2

-- Si se cierra la tapa con un externo conectado: apagar la interna. Sin externo, cerrar la
-- tapa suspende (logind) y Noctalia bloquea antes (lock_before_suspend).
TAPA_APAGA_INTERNA = true

-- Workspaces
NUM_WPM = 5 -- Escritorios virtuales (cara principal 1..5, cara secundaria 6..10)
