#!/bin/bash
cd "$(dirname "$0")"
for i in $(seq 1 120); do grep -qE "added [0-9]+ packages|up to date|ERR!|npm error" npm_install.log && break; sleep 3; done
[ -x node_modules/.bin/lighthouse ] || { echo "LH_INSTALL_FAILED"; tail -5 npm_install.log; echo DONE; exit 1; }
export CHROME_PATH=/opt/pw-browsers/chromium
FLAGS="--headless=new --no-sandbox --disable-gpu --ignore-certificate-errors"
[ -n "$HTTPS_PROXY" ] && FLAGS="$FLAGS --proxy-server=$HTTPS_PROXY"
run() { name=$1; url=$2; shift 2
  if node_modules/.bin/lighthouse "$url" --output=json --output-path="lh_${name}.json" --chrome-flags="$FLAGS" --only-categories=performance,accessibility,best-practices,seo --quiet "$@" 2>>lh_err.log; then echo "OK $name"; else echo "FAIL $name"; fi; }
run home_mobile https://provision-infra.de/
run home_desktop https://provision-infra.de/ --preset=desktop
run zutritt_mobile https://provision-infra.de/zutrittssystem/
run kamera_mobile https://provision-infra.de/kamerasysteme/
run lueneburg_mobile https://provision-infra.de/lueneburg/
echo DONE
