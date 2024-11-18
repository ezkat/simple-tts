import asyncio
import schedule
from threading import Thread, Event
from time import sleep
from logging import getLogger
from .models import ConversionRequest

logger = getLogger()


class Poll:
    def __init__(self):
        self.currently_processing = []
        self.loop = asyncio.get_event_loop()
        self.thread = Thread(target=self.poll)
        self.signal = Event()
        self.thread.setDaemon(True)
        self.thread.start()

    def process_pending_tts(self):
        processing = ConversionRequest.objects.filter(status=ConversionRequest.PENDING).exclude(pk__in=self.currently_processing)
        self.currently_processing.extend([con_req.id for con_req in processing])
        for conversion_request in processing:
            conversion_request.process_tts()
            self.currently_processing.remove(conversion_request.id)

    def poll(self):
        schedule.every(5).seconds.do(self.process_pending_tts)
        self.process_pending_tts()
        while not self.signal.wait(0):
            schedule.run_pending()
            sleep(1)
        
    
    def stop(self):
        self.signal.set()
