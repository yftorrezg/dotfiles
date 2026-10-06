-- Environmental variables (for reference https://wiki.hypr.land/Configuring/Advanced-and-Cool/Environment-variables/)
-- if you use UWSM, define your variables in ~/.config/uwsm/env
-- if you don't use UWSM, define your variables here (e.g. hl.env("QT_QPA_PLATFORM", "wayland"))

-- if you have an NVIDIA GPU uncomment the following lines:
-- (25/09/2026) Activadas para la GTX 980 (driver nvidia-580xx). Backup en backups/environment.lua.bak-20260925-nvidia

hl.env("GBM_BACKEND", "nvidia-drm") -- force GBM as a backend
hl.env("__GLX_VENDOR_LIBRARY_NAME", "nvidia") -- force GBM as a backend
hl.env("LIBVA_DRIVER_NAME", "nvidia") -- Hardware acceleration on NVIDIA GPUs
hl.env("NVD_BACKEND", "direct") -- nvidia-vaapi-driver: modo recomendado para driver 525+
-- hl.env("__GL_GSYNC_ALLOWED", "1") -- Controls if G-Sync capable monitors should use Variable Refresh Rate (VRR)
