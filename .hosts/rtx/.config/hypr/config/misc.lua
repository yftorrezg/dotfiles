hl.config({
    dwindle = {
        preserve_split = true,
    },
    ecosystem = {
        no_update_news = true,
        no_donation_nag = true,
    },
    misc = {
        col = {
            splash = CACHYLGREEN,
        },
        middle_click_paste = false,
        enable_swallow = true,
        swallow_regex = "(kitty|ghostty|[Kk]onsole|Alacritty|gnome-terminal|xfce[0-9]?-terminal)",
        -- VRR: la interna (AU Optronics 60 Hz) no tiene VRR; 3 = solo en pantalla completa
        -- con contenido de juego/video, inofensivo y útil si algún día hay un externo VRR.
        vrr = 3,
        -- LAPTOP: sin logo/splash de fondo (menos dibujo) y despertar la pantalla con teclado/mouse
        -- tras el "apagar pantalla" de Noctalia.
        disable_hyprland_logo = true,
        disable_splash_rendering = true,
        key_press_enables_dpms = true,
        mouse_move_enables_dpms = true,
    },
    -- VFR (no redibujar si nada cambia = menos batería). En 0.56 es debug.vfr y ya viene en true;
    -- se deja explícito para que nadie lo apague.
    debug = {
        vfr = true,
    },
    render = {
        direct_scanout = 2,
    },
    xwayland = {
        force_zero_scaling = true
    },
})
