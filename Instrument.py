from RsInstrument.RsInstrument import RsInstrument
import Types


class Instrument:
    def __init__(self, resource_string: str):
        self.instr = RsInstrument(resource_string, True, False)

    def write(self, command: str):
        self.instr.write_str_with_opc(command)

    def query(self, command: str):
        return self.instr.query_str_with_opc(command)

    def greet(self):
        idn = self.query("*IDN?")
        print(f"\nHello, I am: '{idn}'")
        print(f"RsInstrument driver version: {self.instr.driver_version}")
        print(f"Visa manufacturer: {self.instr.visa_manufacturer}")
        print(f"Instrument full name: {self.instr.full_instrument_model_name}")
        print(f"Instrument installed options: {','.join(self.instr.instrument_options)}")

    def rename_trace(self, trace_id: int, trace_name: str):
        self.write(f"configure:trace{trace_id}:name {trace_name}")

    def reset(self):
        self.instr.reset()

    def correction_state(self):
        return self.query("correction:state?")

    def set_display_mode(self, display_mode: str):
        self.write(f"system:display:update {display_mode}")
        # self.write("initiate1:continuous off")

    def set_visa_timeout(self, timeout: int):
        self.instr.visa_timeout = timeout

    def set_status_checking(self, status_checking: bool):
        self.instr.instrument_status_checking = status_checking

    def create_trace(self, channel: int, name: str, result: str):
        self.write(f"calculate{channel}:parameter:sdefine '{name}', '{result}'")

    def set_touchscreen_lock(self, ts_lock_mode: str):
        self.write(f"system:tslock {ts_lock_mode}")

    def set_trace_points(self, channel: int, points: int):
        self.write(f"sense{channel}:sweep:points {points}")

    def copy_trace(self, memory_trace_name: str, data_trace_name: str):
        self.write(f"trace:copy '{memory_trace_name}', '{data_trace_name}'")

    def assign_trace_to_window(self, window_id: int, trace_id: int, trace_name: str):
        self.write(f"display:window{window_id}:trace{trace_id}:feed '{trace_name}'")

    def create_window(self, window_id: int):
        self.write(f"display:window{window_id}:state on")

    def remove_window(self, window_id: int):
        self.write(f"display:window{window_id}:state off")

    def load_calibration_data(self, channel: int, file_name: str):
        self.write(f"mmemory:load:correction {channel}, '{file_name}'")

    def save_all_traces(self, channel: int, path: 'str',
                        formatted: bool = True,
                        save_format: str = Types.SaveFormat.COMPLEX,
                        dec_separator: str = Types.DecimalSeparator.POINT,
                        field_separator: str = Types.FieldSeparator.SEMICOLON):
        formatted = 'formatted' if formatted else 'unformatted'
        self.write(
            f"mmemory:store:trace:channel {channel}, '{path}', {formatted}, {save_format}, {dec_separator}, {field_separator}")

    def close(self):
        self.instr.close()
