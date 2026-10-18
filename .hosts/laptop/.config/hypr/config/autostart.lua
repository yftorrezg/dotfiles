-- Auto-start config
-- if you dont use UWSM add your auto start programs here, otherwise use XDG autostart https://wiki.archlinux.org/title/XDG_Autostart

hl.on("hyprland.start", function ()
    hl.exec_cmd("dbus-update-activation-environment --systemd --all")
    hl.exec_cmd("noctalia")
    hl.exec_cmd("xhost +SI:localuser:root")
    -- LAPTOP: se quitó "powerprofilesctl set balanced" (era para la PC). El perfil de energía
    -- lo elige power-profiles-daemon / Noctalia (centro de control) y recuerda el último.
    -- Recuerda el escritorio de cada ventana y lo restaura al reabrirlas (ej. Brave)
    hl.exec_cmd("python3 " .. os.getenv("HOME") .. "/.config/hypr/scripts/sesion-ventanas.py")
    -- Fondo propio y aviso bonito por escritorio (config: ~/.config/hypr/escritorios-temas.toml)
    hl.exec_cmd("python3 " .. os.getenv("HOME") .. "/.config/hypr/scripts/escritorios-vivos.py")
end)
