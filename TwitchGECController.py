import concurrent.futures
import TwitchPlays_Connection
from TwitchPlays_KeyCodes import *
from QTExtra import colors
import json

class TwitchGECController:
    def __init__(self,mainWindows,savefile):
        self.mainWindow=mainWindows
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
                

    def handle_message(self,message):
        try:
            msg = message['message'].lower()
            username = message['username'].lower()
            if username in self.allowedMods:
                if msg.startswith("/markmon"):
                    monName=msg.strip().replace("/markmon","")
                    self.mainWindow.twitchUpdateMons(monName)
                #do stuff
            print("Got this message from " + username + ": " + msg)
        except Exception as e:
            print("Encountered exception: " + str(e))

    def run(self):
        while True:
            active_tasks = [t for t in active_tasks if not t.done()]
            #Check for new messages
            new_messages = t.twitch_receive_messages();
            if new_messages:
                message_queue += new_messages; # New messages are added to the back of the queue
                message_queue = message_queue[-self.MAX_QUEUE_LENGTH:] # Shorten the queue to only the most recent X messages

            messages_to_handle = []
            if not message_queue:
                # No messages in the queue
                last_time = time.time()
            else:
                # Determine how many messages we should handle now
                r = 1 if self.MESSAGE_RATE == 0 else (time.time() - last_time) / self.MESSAGE_RATE
                n = int(r * len(message_queue))
                if n > 0:
                    # Pop the messages we want off the front of the queue
                    messages_to_handle = message_queue[0:n]
                    del message_queue[0:n]
                    last_time = time.time()

            if not messages_to_handle:
                continue
            else:
                for message in messages_to_handle:
                    if len(active_tasks) <= self.MAX_WORKERS:
                        active_tasks.append(self.thread_pool.submit(self.handle_message, message))
                    else:
                        print(f'WARNING: active tasks ({len(active_tasks)}) exceeds number of workers ({self.MAX_WORKERS}). ({len(message_queue)} messages in the queue)')