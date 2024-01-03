import time
import usb_hid
import board
import digitalio
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import rotaryio

btn1 = digitalio.DigitalInOut(board.GP21)
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.DOWN

btn2 = digitalio.DigitalInOut(board.GP19)
btn2.direction = digitalio.Direction.INPUT
btn2.pull = digitalio.Pull.DOWN

btn3 = digitalio.DigitalInOut(board.GP17)
btn3.direction = digitalio.Direction.INPUT
btn3.pull = digitalio.Pull.DOWN

btn4 = digitalio.DigitalInOut(board.GP20)
btn4.direction = digitalio.Direction.INPUT
btn4.pull = digitalio.Pull.DOWN

btn5 = digitalio.DigitalInOut(board.GP18)
btn5.direction = digitalio.Direction.INPUT
btn5.pull = digitalio.Pull.DOWN

btn6 = digitalio.DigitalInOut(board.GP16)
btn6.direction = digitalio.Direction.INPUT
btn6.pull = digitalio.Pull.DOWN

button = digitalio.DigitalInOut(board.GP28)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

encoder = rotaryio.IncrementalEncoder(board.GP27, board.GP26)

cc = ConsumerControl(usb_hid.devices)

keyboard = Keyboard(usb_hid.devices)

button_state = None
last_position = encoder.position

while True:
    if btn1.value:
        keyboard.send(Keycode.CONTROL, Keycode.F7)
        time.sleep(0.1)
    if btn2.value:
        keyboard.send(Keycode.CONTROL, Keycode.F8)
        time.sleep(0.1)
    if btn3.value:
        keyboard.send(Keycode.CONTROL, Keycode.F9)
        time.sleep(0.1)
    if btn4.value:
        keyboard.send(Keycode.CONTROL, Keycode.F10)
        time.sleep(0.1)
    if btn5.value:
        keyboard.send(Keycode.CONTROL, Keycode.F11)
        time.sleep(0.1)
    if btn6.value:
        keyboard.send(Keycode.CONTROL, Keycode.F12)
        time.sleep(0.1)
    time.sleep(0.1)
    current_position = encoder.position
    position_change = current_position - last_position
    if position_change > 0:
        for _ in range(position_change):
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        print(current_position)
    elif position_change < 0:
        for _ in range(-position_change):
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        print(current_position)
    last_position = current_position
    if not button.value and button_state is None:
        button_state = "pressed"
    if button.value and button_state == "pressed":
        print("Button pressed.")
        cc.send(ConsumerControlCode.PLAY_PAUSE)
        button_state = None
