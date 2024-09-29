import concurrent.futures
import TwitchPlays_Connection
from TwitchPlays_KeyCodes import *
from PyQt5.QtCore import QThread
import json


accentDict = {"À":"\u00C0","Á":"\u00C1",
             "È":"\u00C8","É":"\u00C9",
              "Ì":"\u00CC", "Í":"\u00CD",
              "Ò":"\u00D2","Ó":"\u00D3",
              "Ù":"\u00D9","Ú": "\u00DA","'":"\u2019" }

class TwitchGECController(QThread):
    def __init__(self,mainWindowSignal,file):
        super().__init__()
        self.mainWindow=mainWindowSignal
        with open(file) as savefile:
            jload=json.load(savefile)
            self.TWITCH_CHANNEL = jload["channel"]
            self.allowedMods = jload["mods"]
            self.MESSAGE_RATE = jload["message_rate"]#0.5
            self.MAX_QUEUE_LENGTH = jload["queue_length"]#= 10
            self.MAX_WORKERS = jload["workers"]#5 # Maximum number of threads you can process at a time
            # Replace this with your Twitch username. Must be all lowercase.
            self.last_time = time.time()
            self.message_queue = []
            self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=self.MAX_WORKERS)
            self.active_tasks = []
            self.t = TwitchPlays_Connection.Twitch()
            self.t.twitch_connect(self.TWITCH_CHANNEL)

    def handle_message(self,message):
        try:
            msg = message['message'].upper().replace(" ","")
            username = message['username'].lower()
            for acc in accentDict:
                msg=msg.replace(acc,accentDict[acc])
            print("Got this message from " + username + ": " + msg)
            if username in self.allowedMods:
                if msg.startswith("!MARKTRAINER"):
                    trainName=msg.replace("!MARKTRAINER","").replace("\U000e0000","")
                    self.mainWindow.emit("TR",trainName+"@"+str(1))
                elif msg.startswith("!UNMARKTRAINER"):
                    trainName=msg.replace("!UNMARKTRAINER","").replace("\U000e0000","")
                    self.mainWindow.emit("TR",trainName+"@"+str(0))
                elif msg.startswith("!MARKITEM"):
                    item=msg.replace("!MARKITEM","").replace("\U000e0000","")
                    self.mainWindow.emit("ITEM-",item+"@"+str(1))
                elif msg.startswith("!UNMARKITEM"):
                    item=msg.replace("!UNMARKITEM","").replace("\U000e0000","")
                    self.mainWindow.emit("ITEM-",item+"@"+str(0))
                elif msg.startswith("!MARKMISC"):
                    item=msg.replace("!MARKMISC","").replace("\U000e0000","")
                    self.mainWindow.emit("EVENT",item+"@"+str(1))
                elif msg.startswith("!UNMARKMISC"):
                    item=msg.replace("!UNMARKMISC","").replace("\U000e0000","")
                    self.mainWindow.emit("EVENT",item+"@"+str(0))
                elif msg.startswith("!MARKMOVE"):
                    movename=msg.replace("!MARKMOVE","").replace("\U000e0000","").strip()
                    self.mainWindow.emit("MOVE",movename+"@"+str(1))
                elif msg.startswith("!UNMARKMOVE"):
                    movename=msg.replace("!UNMARKMOVE","").replace("\U000e0000","").strip()
                    self.mainWindow.emit("MOVE",movename+"@"+str(0))
                elif msg.startswith("!MARKMON"):
                    monName=msg.replace("!MARKMON","").replace("\U000e0000","").strip()
                    self.mainWindow.emit("MON",monName+"@"+str(1))
                elif msg.startswith("!MARKBLU"):
                    monName=msg.replace("!MARKBLU","").replace("\U000e0000","").strip()
                    self.mainWindow.emit("MON",monName+"@"+str(2))
                elif msg.startswith("!UNMARKMON"):
                    monName=msg.replace("!UNMARKMON","").replace("\U000e0000","").strip()
                    self.mainWindow.emit("MON",monName+"@"+str(0))
                
                #do stuff
        except Exception as e:
            print("Encountered exception: " + str(e))
    
    def run(self):
        print("Chat controller online")
        while True:
            self.active_tasks = [t for t in self.active_tasks if not t.done()]
            #Check for new messages
            new_messages = self.t.twitch_receive_messages()
            if new_messages:
                self.message_queue += new_messages; # New messages are added to the back of the queue
                self.message_queue = self.message_queue[-self.MAX_QUEUE_LENGTH:] # Shorten the queue to only the most recent X messages

            messages_to_handle = []
            if not self.message_queue:
                # No messages in the queue
                last_time = time.time()
            else:
                # Determine how many messages we should handle now
                r = 1 if self.MESSAGE_RATE == 0 else (time.time() - last_time) / self.MESSAGE_RATE
                n = int(r * len(self.message_queue))
                if n > 0:
                    # Pop the messages we want off the front of the queue
                    messages_to_handle = self.message_queue[0:n]
                    del self.message_queue[0:n]
                    last_time = time.time()

            if not messages_to_handle:
                continue
            else:
                for message in messages_to_handle:
                    if len(self.active_tasks) <= self.MAX_WORKERS:
                        self.active_tasks.append(self.thread_pool.submit(self.handle_message, message))
                    else:
                        print(f'WARNING: active tasks ({len(self.active_tasks)}) exceeds number of workers ({self.MAX_WORKERS}). ({len(self.message_queue)} messages in the queue)')
