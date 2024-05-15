import meshtastic
import meshtastic.tcp_interface
from pubsub import pub
import requests

WEBHOOK_URL = "<WEBHOOK URL>"

def onReceive(packet, interface):
    try:
        message = packet["decoded"]


        if (message["portnum"] != "TEXT_MESSAGE_APP"): return
        if (packet["toId"] != meshtastic.BROADCAST_ADDR): return

        node = interface.nodesByNum.get(packet["from"])
        user = node.get("user")

        webhook_message = {
            "username": f"{user.get("longName", "UNK")} ({user.get("shortName", "UNK")})",
            "content": None,
            "embeds": [
                {
                    "title": f"{message["text"]}",
                    "description": f"snr: {packet["rxSnr"]} rssi: {packet["rxRssi"]} id: !{str(hex(int(packet["from"])))[2:]}",
                    "color": None,
                    "footer": {
                        "text": "Recived via \"Meshtastic Canberra Discord (MCD)\""
                    }
                }
            ],
            "attachments": []
        }

        requests.post(WEBHOOK_URL, json=webhook_message)

    except Exception as e:
        print(f"[Error][webhook] Exception in \"onReceive()\": {e}")

def init():
    pub.subscribe(onReceive, "meshtastic.receive")
