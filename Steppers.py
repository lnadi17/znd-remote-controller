import serial


class Steppers:
    def __init__(self, port='COM3', baudrate=9600, timeout=10):
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        print("Serial connection: ", self.arduino)
        print("Note: Any read command will stop reading if the line contains '~' symbol.")
        print("Note: All occurrences of '~' symbol will be erased.")
        print(self.read())

    def move_x(self, mm: int):
        self.query(f'movex {mm}')

    def move_y(self, mm: int):
        self.query(f'movey {mm}')

    def write(self, command):
        self.arduino.write(bytes(command, 'utf-8'))

    def query(self, command):
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
