import meshtastic
import meshtastic.tcp_interface
from pubsub import pub
import json

def onReceive(packet, interface):
    try:
        message = packet["decoded"]

        if (message["portnum"] == "TEXT_MESSAGE_APP"): 
            if (packet["to"] == interface.myInfo.my_node_num):
                if (message["text"] == "ping"):
                    interface.sendText("pong", packet["from"], True)
    except  Exception as e:
        print(f"Error while running onReceive() in module pingpong: {e}")

def init():
    pub.subscribe(onReceive, "meshtastic.receive")