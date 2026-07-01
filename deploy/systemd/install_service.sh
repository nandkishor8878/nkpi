#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="/home/nkpi/smart-reception-assistant"
SERVICE_SOURCE="${PROJECT_DIR}/deploy/systemd/aura.service"
SERVICE_TARGET="/etc/systemd/system/aura.service"

sudo cp "${SERVICE_SOURCE}" "${SERVICE_TARGET}"
sudo systemctl daemon-reload
sudo systemctl enable aura.service
sudo systemctl restart aura.service
sudo systemctl status aura.service --no-pager
