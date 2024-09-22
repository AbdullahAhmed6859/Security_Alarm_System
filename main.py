from gpiozero import RGBLED, LED, Button, DistanceSensor, Buzzer
from time import sleep

class SecuritySystem:
    KEYPAD = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
        ["*", "0", "#"],
    ]

    def __init__(self):
        self.rows = [LED(19), LED(13), LED(6), LED(5)]
        self.cols = [Button(22), Button(27), Button(17)]
        self.sensor = DistanceSensor(echo=4, trigger=3)
        self.buzzer = Buzzer(26)
        self.led = RGBLED(red=25, blue=23, green=24)
        self.state = "off"
        self.password = "1234"
        self.code = ""
        self.threshold_distance = 0.5

    def check_button_press(self, row, col):
        if self.cols[col].is_pressed:
            digit = self.KEYPAD[row][col]
            print(digit)
            self.code += digit
            while self.cols[col].is_pressed:
                pass
            return True
        return False

    def scan_keypad(self):
        for i, row in enumerate(self.rows):
            row.on()
            self.rows[i].off()
            for j in range(3):
                if self.check_button_press(i, j):
                    return
            self.rows[i].on()

    def get_code(self):
        self.code = ""
        print("Enter Code")
        while len(self.code) < 4:
            self.scan_keypad()

    def star_check(self):
        self.rows[3].off()
        if self.cols[0].is_pressed:
            while self.cols[0].is_pressed:
                pass
            return True
        self.rows[3].on()
        return False

    def detect_intruder(self):
        return self.sensor.distance < self.threshold_distance

    def run(self):
        while True:
            if self.state == "off":
                self.led.color = (0, 0, 0)
                print("System is off")
                if self.star_check():
                    self.get_code()
                    if self.code == self.password:
                        self.state = "on"
                    else:
                        print("Wrong password")

            elif self.state == "on":
                self.led.color = (1, 0.5, 0)
                if self.detect_intruder():
                    self.state = "buzz"
                elif self.star_check():
                    self.get_code()
                    if self.code == self.password:
                        self.state = "off"
                    else:
                        print("Wrong password")

            elif self.state == "buzz":
                self.led.color = (1, 0, 0)
                self.buzzer.on()
                if self.star_check():
                    self.get_code()
                    if self.code == self.password:
                        self.state = "on"
                        self.buzzer.off()

if __name__ == "__main__":
    security_system = SecuritySystem()
    security_system.run()