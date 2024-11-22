#!/bin/bash
# This script installs the ble-setup service

### BLE SETUP

# Create service file
cat >/etc/systemd/system/ble-setup.service <<EOF
[Unit]
Description=Setup BLE

[Service]
Type=oneshot
ExecStart=/home/pi/bleval/ble.sh
StandardOutput=journal
StandardError=journal
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

# Create shell script
mkdir -p /home/pi/bleval
cat >/home/pi/bleval/ble.sh <<EOF
#!/bin/bash
sudo btmgmt power off
sudo btmgmt discov on
sudo btmgmt io-cap 3
sudo btmgmt connectable on
sudo btmgmt pairable on
sudo btmgmt power on
EOF

chmod +x /home/pi/bleval/ble.sh

# Enable and start service
systemctl enable --now ble-setup
