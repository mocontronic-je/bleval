#!/home/pi/bleval/.venv-rpi/bin/python -u
# coding: utf-8

"""
Example for a BLE 4.0 Server
"""
import sys
import logging
import asyncio
import threading

from typing import Any, Union

from bless import (  # type: ignore
    BlessServer,
    BlessGATTCharacteristic,
    GATTCharacteristicProperties,
    GATTAttributePermissions,
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(name=__name__)

# NOTE: Some systems require different synchronization methods.
trigger: Union[asyncio.Event, threading.Event]
if sys.platform in ["darwin", "win32"]:
    trigger = threading.Event()
else:
    trigger = asyncio.Event()






# def notify(server, service_uuid, char_uuid, value):
#     server.get_characteristic(char_uuid).value = value
#     server.update_value(service_uuid, char_uuid)


run_forever = True

async def run(loop):
    ### GATT Konfiguration:
    nus_service_uuid = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
    # RX Characteristic
    rx_char_uuid = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
    rx_char_flags = (
        GATTCharacteristicProperties.write
        | GATTCharacteristicProperties.write_without_response
    )
    rx_char_permissions = GATTAttributePermissions.writeable
    # TX Characteristic
    tx_char_uuid = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
    tx_char_flags = (GATTCharacteristicProperties.notify)
    tx_char_permissions = GATTAttributePermissions.readable
    tx_buffer = bytearray(b'oKaY')

    # Instantiate the server
    my_service_name = "UART Test Service"
    server = BlessServer(name=my_service_name, loop=loop)

    

    # read handler (wird der überhaupt genutzt? - wird über notify/update_value)
    def read_request(characteristic: BlessGATTCharacteristic, **kwargs) -> bytearray:
        logger.debug(f"Reading {characteristic.value}")
        #trigger.set()
        return characteristic.value

    # write handler
    def write_request(characteristic: BlessGATTCharacteristic, value: Any, **kwargs):
        characteristic.value = value
        logger.debug(f"Serial input over BLE:{characteristic.value}")
        if characteristic.value == bytearray(b'quit'):
            global run_forever
            run_forever = False
        else:
            # echo input:
            server.get_characteristic(tx_char_uuid).value = bytearray(b'okay: ' + characteristic.value)
            server.update_value(nus_service_uuid, tx_char_uuid)

    # Set read/write callback functions
    server.read_request_func = read_request
    server.write_request_func = write_request

    # Add Service  
    await server.add_new_service(nus_service_uuid)
    # Add RX Characteristic to the service
    await server.add_new_characteristic(
        nus_service_uuid, rx_char_uuid, rx_char_flags, None, rx_char_permissions
    )
    # Add TX Characteristic to the service 
    await server.add_new_characteristic(
        nus_service_uuid, tx_char_uuid, tx_char_flags, tx_buffer, tx_char_permissions
    )

    logger.debug(server.get_characteristic(rx_char_uuid))
    logger.debug(server.get_characteristic(tx_char_uuid))
    
    # Start GATT Server
    await server.start()
    logger.debug("GATT Server started ..")
    logger.debug("Starting loop forever")

    while run_forever:
        pass
        await asyncio.sleep(2)
        
    await server.stop()


loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))
