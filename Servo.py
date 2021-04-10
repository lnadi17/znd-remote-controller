import serial
import io
import time


class Servo:
    def __init__(self, port='COM3', baudrate=9600, timeout=10):
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        print("Serial connection: ", self.arduino)
        print("Note: Any read command will stop reading if the line contains '~' symbol.")
        print("Note: All occurrences of '~' symbol will be erased.")
        print(self.read())

    def read_angle(self):
        return self.query('get').split()[1]

    def start_sweep(self):
        self.query('start')

    def stop_sweep(self):
        self.query('stop')

    def write_angle(self, angle):
        return self.query(f'goto {angle}')

    def set_speed(self, speed):
        return self.query(f'speed {speed}')

    def set_range(self, start, stop):
        return self.query(f'range {start} {stop}')

    def write(self, command):
        self.arduino.write(bytes(command, 'utf-8'))

    def query(self, command):
        # self.write(command)
        self.write(command)
        return self.read()

    def read(self):
        data = ''
        while True:
            line = self.arduino.readline().decode('utf-8')
            if line == '':
                break
            data += str(line)
            if '~' in line:
                break
        return data.replace('~', '')


servo = Servo()
print(servo.read_angle())
servo.set_range(0, 90)
servo.set_speed(100)
servo.write_angle(45)
servo.start_sweep()
time.sleep(5)
servo.stop_sweep()

