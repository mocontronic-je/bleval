#!/bin/bash
# This script installs and enables/starts the blevald service

# Create service file
cat >/etc/systemd/system/blevald.service <<EOF
[Unit]
Description=blevald service
After=pigpiod.service
Requires=pigpiod.service
Requires=bluetooth.service
After=bluetooth.service
[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/bleval
ExecStartPre=/usr/bin/sleep 3
ExecStart=/home/pi/bleval/daemon.py
ExecReload=/bin/kill -1 -- $MAINPID
ExecStop=/bin/kill -- $MAINPID
TimeoutStopSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Enable and start pigpiod service
systemctl enable --now pigpiod.service

# Enable and start blevald service
systemctl enable --now blevald.service
