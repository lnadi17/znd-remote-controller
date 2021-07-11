import serial


class Steppers:
    def __init__(self, port='COM3', baudrate=9600, timeout=60):
        self.home = (0, 0)
        self.position = (0, 0)
        self.max = (1000, 1000)
        self.x_reversed = False
        self.y_reversed = False
        self.ignore_bounds = False
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        print("Serial connection: ", self.arduino)
        print("Note: Any read command will stop reading if the line contains '~' symbol.")
        print("Note: All occurrences of '~' symbol will be erased.")
        print(self.read())

    # If set to true, steppers can go anywhere without a problem
    # If set to false, steppers only move in (0, max) range for both axes
    def set_ignore_bounds(self, should_ignore: bool = False):
        self.ignore_bounds = should_ignore

    def attach(self):
        self.query("attach")

    def release(self):
        self.query("detach")

    def reverse_x(self):
        self.x_reversed = not self.x_reversed

    def reverse_y(self):
        self.y_reversed = not self.y_reversed

    def set_home(self):
        self.home = self.position
        self.position = (0, 0)

    def set_max(self):
        self.max = self.position

    def set_max(self, x=500, y=800):
        self.max = (x, y)

    def go_home(self):
        self.set_position(0, 0)

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
        mm = mm if not self.x_reversed else -mm
        future_position = (self.position[0] + mm, self.position[1])
        # Don't move if current command gets us out of bounds
        if not self.ignore_bounds and not (0 <= future_position[0] <= self.max[0]):
            return
        self.query(f'movex {mm}')
        self.position = future_position

    def move_y(self, mm: int):
        mm = mm if not self.y_reversed else -mm
        future_position = (self.position[0], self.position[1] + mm)
        # Don't move if current command gets us out of bounds
        if not self.ignore_bounds and not (0 <= future_position[1] <= self.max[1]):
            return
        self.query(f'movey {mm}')
        self.position = future_position

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
