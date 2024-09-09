import concurrent.futures
import TwitchPlays_Connection
from TwitchPlays_KeyCodes import *
from PyQt5.QtCore import QThread
import json


class TwitchGECController(QThread):
    def __init__(self,mainWindow,file):
        super().__init__()
        self.mainWindow=mainWindow
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
            msg = message['message'].lower()
            username = message['username'].lower()
            print("Got this message from " + username + ": " + msg)
            if username in self.allowedMods:
                if msg.startswith(">markmon"):
                    monName=msg.replace(">markmon","").strip()
                    self.mainWindow.twitchUpdateMons(monName)
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
