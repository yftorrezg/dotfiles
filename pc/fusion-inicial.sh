#!/usr/bin/env bash
# PC — primer paso de la sincronización. SEGURO: respalda, baja el repo y muestra diferencias.
# NO aplica nada a $HOME. La fusión la hace Claude siguiendo CLAUDE.md (sección "Fusión inicial en la PC").
#
# Uso (en la PC, con chezmoi y github-cli instalados y `gh auth login` hecho):
#   bash <(gh api repos/yftorrezg/dotfiles/contents/pc/fusion-inicial.sh -H 'Accept: application/vnd.github.raw')
set -euo pipefail

for c in chezmoi gh git luac; do command -v $c >/dev/null || { echo "Falta $c → sudo pacman -S --needed chezmoi github-cli git lua"; exit 1; }; done
gh auth status >/dev/null 2>&1 || { echo "Primero: gh auth login"; exit 1; }
gh auth setup-git   # git usa el token de gh para el repo privado

TS=$(date +%Y%m%d-%H%M)
RESP="$HOME/respaldo-antes-dotsync-$TS.tar"
echo "==> Respaldo de la config actual de la PC → $RESP"
tar -cf "$RESP" -C "$HOME" .config .local/bin .local/share/applications .local/share/doblar \
    .local/state/noctalia .claude/projects/-home-yafer/memory .gitconfig .gtkrc-2.0 2>/dev/null || true
ls -lh "$RESP"

SRC="$HOME/.local/share/chezmoi"
if [[ -d $SRC/.git ]]; then
    echo "==> El repo ya estaba en $SRC (no se vuelve a clonar)"
else
    echo "==> Bajando el repo (sin aplicar)"
    chezmoi init https://github.com/yftorrezg/dotfiles.git
fi

EQ=$(chezmoi execute-template '{{ .equipo }}')
echo "==> Este equipo es: $EQ"
[[ $EQ == pc ]] || { echo "Se esperaba 'pc'. Si el hostname no es 'yf', ajusta .chezmoi.toml.tmpl o responde 'pc' al prompt."; exit 1; }

OUT="$HOME/dotsync-fusion-$TS"
mkdir -p "$OUT"
chezmoi status > "$OUT/status.txt" || true
chezmoi diff > "$OUT/diff.patch" || true
echo
echo "==> Archivos que cambiarían si se aplicara el repo tal cual (NO se aplicó nada):"
sed 's/^/    /' "$OUT/status.txt"
echo
echo "Diferencias completas: $OUT/diff.patch"
echo "Respaldo:              $RESP"
echo
echo "SIGUIENTE: abre Claude Code en la PC y dile:"
echo "   «Lee ~/.local/share/chezmoi/CLAUDE.md y haz la fusión inicial de la PC. Diferencias en $OUT»"
