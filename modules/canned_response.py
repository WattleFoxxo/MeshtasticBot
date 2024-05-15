import meshtastic
import meshtastic.tcp_interface
from pubsub import pub
import json
import time

RESPONDERS = {
    "/help": { "response": "Commands:\n/help : This menu\n/ping : Replies with \"pong\"\n/about : Info about this node\n/discord : Replies with discord invite", "directOnly": True },
    "/ping": { "response": "pong", "directOnly": True },
    "/about": { "response": "This node is owned by WattleFoxxo (TISM) made for the Meshtastic Canberra Discord server.", "directOnly": True },
    "/discord": { "response": "https://discord.gg/4QgFsuaC3Z", "directOnly": True },
    "*": { "response": "Welcome to the Meshtastic Canberra Discord bot!\nSend /help for help.", "directOnly": True }
}

CHUNK_SIZE = 128

def onReceive(packet, interface):
    try:
        message = packet["decoded"]

        if (message["portnum"] != "TEXT_MESSAGE_APP"): return

        
        responder = RESPONDERS["*"]

        if (message["text"] in RESPONDERS):
            responder = RESPONDERS[message["text"]]
            
        if (responder["directOnly"]):
            if (packet["to"] != interface.myInfo.my_node_num): return

        print(f"[Info][canned_response] Node: !{str(hex(int(packet["from"])))[2:]} ran \"{message["text"]}\"")
        
        chunks = [responder["response"][i:i+CHUNK_SIZE] for i in range(0, len(responder["response"]), CHUNK_SIZE)]

        for chunk in chunks:
            interface.sendText(chunk, packet["from"], True)
            time.sleep(1)

    except Exception as e:
        print(f"[Error][canned_response] Exception in \"onReceive()\": {e}")

def init():
    pub.subscribe(onReceive, "meshtastic.receive")