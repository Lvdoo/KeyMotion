import serial

class HardwareControls:
    def __init__(self, port="COM4", baudrate=115200):
        self.serial = serial.Serial(port, baudrate, timeout=0)

    def read_messages(self):
        messages = []

        while self.serial.in_waiting:
            line = self.serial.readline().decode("utf-8", errors="ignore").strip()

            if line:
                messages.append(line)

        return messages

    def close(self):
        self.serial.close()