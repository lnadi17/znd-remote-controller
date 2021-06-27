import serial


class Steppers:
    def __init__(self, port='COM3', baudrate=9600, timeout=10):
        self.home = (0, 0)
        self.position = (0, 0)
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        print("Serial connection: ", self.arduino)
        print("Note: Any read command will stop reading if the line contains '~' symbol.")
        print("Note: All occurrences of '~' symbol will be erased.")
        print(self.read())

    def set_home(self):
        self.home = self.position
        self.position = (0, 0)

    def home(self):
        self.set_position(0, 0);

    def get_position(self):
        return self.position

    def set_position(self, mm_x: int, mm_y: int):
        delta_x = mm_x - self.position[0]
        delta_y = mm_y - self.position[1]
        self.move(delta_x, delta_y)

    def move(self, mm_x: int, mm_y: int, first_axis=0):
        if first_axis == 0:
            self.move_x(mm_x)
            self.move_y(mm_y)
        if first_axis == 1:
            self.move_y(mm_y)
            self.move_x(mm_x)

    def move_x(self, mm: int):
        self.query(f'movex {mm}')
        self.position = (self.position[0] + mm, self.position[1])

    def move_y(self, mm: int):
        self.query(f'movey {mm}')
        self.position = (self.position[0], self.position[1] + mm)

    def write(self, command: str):
        self.arduino.write(bytes(command, 'utf-8'))

    def query(self, command: str):
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
