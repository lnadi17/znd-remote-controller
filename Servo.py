import serial
import io


class Servo:
    def __init__(self):
        self.ser = Serial(9600, 'COM1')
        print("Serial connection: ", self.ser)

    def write_angle(self, angle):
        self.ser.write("turn around idk whatever the command is")

    def read_status(self):
        self.ser.write("read status")
        return self.ser.readline()


class Serial:
    def __init__(self, baudrate, port):
        self.ser = serial.Serial()
        self.ser.baudrate = baudrate
        self.ser.port = port
        self.ser.open()
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))

    def open(self):
        if not self.ser.isOpen():
            self.ser.open()
            return True
        return False

    def close(self):
        if self.ser.isOpen():
            self.ser.close()
            return True
        return False

    def is_open(self):
        return self.ser.isOpen()

    def readline(self):
        return self.sio.readline()

    def write(self, command):
        self.sio.write(serial.unicode(command))
        self.sio.flush()
