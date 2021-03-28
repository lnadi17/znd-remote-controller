from typing import Callable
import threading
from RsInstrument.RsInstrument import RsInstrument
import Types


class Instrument:
    def __init__(self, resource_string: str):
        self.instr = RsInstrument(resource_string, True, False)
        self.button_callbacks = {}
        self.button_semaphore = threading.Semaphore()
        self.button_listen = threading.Event()
        self.lock_main_thread = threading.Event()
        self.lock_main_thread.set()
        self.button_thread = ButtonThread(self.button_listen, self.lock_main_thread, self.button_semaphore, self,
                                          self.button_callbacks)
        self.button_thread.start()

    def write(self, command: str):
        if self.lock_main_thread.is_set():
            with self.button_semaphore:
                self.instr.write_str_with_opc(command)
        else:
            self.instr.write_str_with_opc(command)

    def query(self, command: str):
        if self.lock_main_thread.is_set():
            with self.button_semaphore:
                return self.instr.query_str_with_opc(command)
        else:
            return self.instr.query_str_with_opc(command)

    def greet(self):
        idn = self.query("*IDN?")
        print(f"\nHello, I am: '{idn}'")
        print(f"RsInstrument driver version: {self.instr.driver_version}")
        print(f"Visa manufacturer: {self.instr.visa_manufacturer}")
        print(f"Instrument full name: {self.instr.full_instrument_model_name}")
        print(f"Instrument installed options: {','.join(self.instr.instrument_options)}")

    # Button
    def button_define(self, key: Types.ButtonNumber, name: str, callback: Callable):
        self.write(f"system:user:key {key.value}, 'User {name}'")
        self.button_callbacks[key] = callback

    def button_query(self) -> Types.ButtonNumber:
        key = int(self.query(f"system:user:key?")[0])
        return None if key == 0 else Types.ButtonNumber(key)

    def button_clear_all(self):
        self.write("system:user:key 0")

    def button_start_listening(self):
        self.button_listen.set()

    def button_stop_listening(self):
        self.button_listen.clear()

    # Instrument Settings
    def reset(self):
        self.instr.reset()

    def set_visa_timeout(self, timeout: int):
        self.instr.visa_timeout = timeout

    def set_status_checking(self, status_checking: bool):
        self.instr.instrument_status_checking = status_checking

    # Correction
    def correction_state(self, channel: int = 1):
        return self.query(f"sense{channel}:correction:sstate?")

    def correction_load(self, channel: int, file_name: str):
        self.write(f"mmemory:load:correction {channel}, '{file_name}'")

    # Display
    def display_set_mode(self, display_mode: Types.DisplayMode):
        self.write(f"system:display:update {display_mode.value}")

    # Window
    def window_create(self, window_id: int):
        self.write(f"display:window{window_id}:state on")

    def window_remove(self, window_id: int):
        self.write(f"display:window{window_id}:state off")

    # Touchscreen
    def touchscreen_set_lock(self, ts_lock_mode: Types.TSLockMode):
        self.write(f"system:tslock {ts_lock_mode.value}")

    # Traces
    def trace_create(self, channel: int, name: str, result: str):
        self.write(f"calculate{channel}:parameter:sdefine '{name}', '{result}'")

    def trace_rename(self, trace_id: int, trace_name: str):
        self.write(f"configure:trace{trace_id}:name '{trace_name}'")

    def trace_set_points(self, channel: int, points: int):
        self.write(f"sense{channel}:sweep:points {points}")

    def trace_copy(self, memory_trace_name: str, data_trace_name: str):
        self.write(f"trace:copy '{memory_trace_name}', '{data_trace_name}'")

    def trace_assign_to_window(self, window_id: int, trace_id: int, trace_name: str):
        self.write(f"display:window{window_id}:trace{trace_id}:feed '{trace_name}'")

    def trace_save_all(self, channel: int, path: 'str',
                       formatted: bool = True,
                       save_format: Types.SaveFormat = Types.SaveFormat.COMPLEX,
                       dec_separator: Types.DecimalSeparator = Types.DecimalSeparator.POINT,
                       field_separator: Types.FieldSeparator = Types.FieldSeparator.SEMICOLON):
        formatted = 'formatted' if formatted else 'unformatted'
        self.write(
            f"mmemory:store:trace:channel {channel}, '{path}', {formatted}, "
            f"{save_format.value}, {dec_separator.value}, {field_separator.value}")


class ButtonThread(threading.Thread):
    def __init__(self, listen: threading.Event, lock_main_thread: threading.Event, semaphore: threading.Semaphore,
                 instrument: Instrument,
                 callbacks: dict):
        threading.Thread.__init__(self)
        self.semaphore = semaphore
        self.lock_main_thread = lock_main_thread
        self.instrument = instrument
        self.callbacks = callbacks
        self.listen = listen

    def run(self):
        while True:
            self.listen.wait()
            while self.listen.is_set():
                with self.semaphore:
                    self.lock_main_thread.clear()
                    key = self.instrument.button_query()
                    if key is not None:
                        self.callbacks[key]()
                    self.lock_main_thread.set()
