#!/bin/bash
# This script configures and enables/starts the pigpiod service
# with full access to every resource (option: -1)


# install apt package
sudo apt install pigpiod


# Create service file
cat >/etc/systemd/system/pigpiod.service <<EOF                                                                       
[Unit]
Description=Daemon required to control GPIO pins via pigpio
[Service]
ExecStart=/usr/bin/pigpiod -x -1
ExecStop=/bin/systemctl kill pigpiod
Type=forking
[Install]
WantedBy=multi-user.target
EOF

# Enable and start pigpiod service
systemctl enable --now pigpiod.service
