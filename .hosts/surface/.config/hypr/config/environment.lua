-- Environmental variables (for reference https://wiki.hypr.land/Configuring/Advanced-and-Cool/Environment-variables/)
-- if you use UWSM, define your variables in ~/.config/uwsm/env
-- if you don't use UWSM, define your variables here (e.g. hl.env("QT_QPA_PLATFORM", "wayland"))

-- SURFACE (Intel UHD Graphics 620): SIN variables NVIDIA.
-- En la PC (GTX 980) estaban activas GBM_BACKEND/__GLX_VENDOR_LIBRARY_NAME/LIBVA_DRIVER_NAME/NVD_BACKEND;
-- en Intel rompen GL/VA-API, así que NO se activan aquí.
-- VA-API (intel-media-driver, iHD) se autodetecta; descomentar solo si `vainfo` eligiera mal el driver:
-- hl.env("LIBVA_DRIVER_NAME", "iHD")
