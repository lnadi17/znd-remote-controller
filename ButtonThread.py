import threading
from Instrument import Instrument, RsInstrument


class ButtonThread(threading.Thread):
    def __init__(self, listen: threading.Event, semaphore: threading.Semaphore, instrument: Instrument, callbacks: dict):
        threading.Thread.__init__(self)
        self.semaphore = semaphore
        self.instrument = instrument
        self.callbacks = callbacks
        self.listen = listen

    def run(self):
        while True:
            self.listen.wait()
            while self.listen.is_set():
                with self.semaphore:
                    key = self.instrument.button_query()
                    if key is not None:
                        self.callbacks[key]()
