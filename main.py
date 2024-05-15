import requests
import time
import meshtastic
import meshtastic.tcp_interface
from pubsub import pub

from modules import webhook
from modules import canned_response

MESHTASTIC_DEVICE = "<DEVICE HOSTNAME>"

print("Connecting...")

canned_response.init()
webhook.init()

interface = meshtastic.tcp_interface.TCPInterface(hostname=MESHTASTIC_DEVICE)

print("Connected to meshtastic device.\nRunning!")

while True:
    time.sleep(1000)

interface.close()
