#!/bin/bash
# This script installs and enables/starts the debugpy service

# Create service file
cat >/etc/systemd/system/debugpy.service <<EOF                                                                       
[Unit]
Description=debugpy service
After=pigpiod.service
Requires=pigpiod.service

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/bleval
ExecStart=/home/pi/bleval/.venv/bin/python -u -m debugpy --listen 0.0.0.0:5678 --wait-for-client /home/pi/bleval/daemon.py
ExecReload=/bin/kill -1 -- \$MAINPID
ExecStop=/bin/kill -- \$MAINPID
TimeoutStopSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Enable and start pigpiod service
systemctl enable --now pigpiod.service
