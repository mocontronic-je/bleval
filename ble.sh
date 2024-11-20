#!/bin/bash
sudo btmgmt power off
sudo btmgmt discov on
sudo btmgmt io-cap 3
sudo btmgmt connectable on
sudo btmgmt pairable on
sudo btmgmt power on
