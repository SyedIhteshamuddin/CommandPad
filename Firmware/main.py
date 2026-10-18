
# CommandPad - CircuitPython firmware
# Board: Seeed XIAO RP2040

import time
import board
import busio
import digitalio
import usb_hid
import neopixel

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# ---------- PIN CONFIGURATION ----------
COL_PINS = (board.D0, board.D1, board.D2)
ROW_PINS = (board.D3, board.D6)

SDA_PIN = board.D4
SCL_PIN = board.D5

ENC_A_PIN = board.D9
ENC_B_PIN = board.D10
ENC_SW_PIN = board.D7

LED_PIN = board.D8
LED_COUNT = 5

OLED_ADDRESS = 0x3C
DEBOUNCE = 0.025

# Matrix layout:
# SW1 = row 0, col 0
# SW2 = row 0, col 1
# SW3 = row 0, col 2
# SW4 = row 1, col 0
# SW5 = row 1, col 1
#
# ASSUMPTION: diode anodes face columns and cathodes face rows.

# ---------- USB KEYBOARD ----------
keyboard = Keyboard(usb_hid.devices)
consumer = ConsumerControl(usb_hid.devices)

SHORTCUTS = {
    (0, 0): (Keycode.CONTROL, Keycode.C),
    (0, 1): (Keycode.CONTROL, Keycode.V),
    (0, 2): (Keycode.CONTROL, Keycode.Z),
    (1, 0): (Keycode.ALT, Keycode.TAB),
    (1, 1): (Keycode.GUI, Keycode.SHIFT, Keycode.S),
}

# ---------- SWITCH MATRIX ----------
columns = []
for pin in COL_PINS:
    obj = digitalio.DigitalInOut(pin)
    obj.direction = digitalio.Direction.INPUT
    obj.pull = digitalio.Pull.UP
    columns.append(obj)

rows = []
for pin in ROW_PINS:
    obj = digitalio.DigitalInOut(pin)
    obj.direction = digitalio.Direction.OUTPUT
    obj.value = True
    rows.append(obj)

raw_key = {key: False for key in SHORTCUTS}
stable_key = {key: False for key in SHORTCUTS}
key_changed_at = {key: time.monotonic() for key in SHORTCUTS}


def scan_matrix():
    pressed = set()

    for r, row in enumerate(rows):
        for other_row in rows:
            other_row.value = True

        row.value = False
        time.sleep(0.001)

        for c, column in enumerate(columns):
            key = (r, c)
            if key in SHORTCUTS and not column.value:
                pressed.add(key)

    for row in rows:
        row.value = True

    return pressed


def send_shortcut(keys):
    keyboard.release_all()
    keyboard.press(*keys)
    time.sleep(0.03)
    keyboard.release_all()


# ---------- ADDRESSABLE LEDS ----------
pixels = None
LED_COLORS = (
    (0, 80, 255),
    (0, 255, 30),
    (180, 0, 255),
    (255, 80, 0),
    (255, 0, 30),
)

try:
    pixels = neopixel.NeoPixel(
        LED_PIN,
        LED_COUNT,
        brightness=0.15,
        auto_write=True,
        pixel_order=neopixel.GRB,
    )
    pixels.fill((0, 0, 0))
except Exception as error:
    print("LED initialization failed:", error)


def set_key_led(key_position, enabled):
    if pixels is None:
        return

    r, c = key_position
    index = r * 3 + c

    if index >= LED_COUNT:
        return

    pixels[index] = LED_COLORS[index] if enabled else (0, 0, 0)


# ---------- OLED DISPLAY ----------
display = None
status_label = None


def show_status(message):
    print(message)

    if status_label is not None:
        try:
            status_label.text = message[:21]
        except Exception as error:
            print("OLED update failed:", error)


try:
    import displayio
    import terminalio
    import i2cdisplaybus
    import adafruit_displayio_ssd1306
    from adafruit_display_text import label

    displayio.release_displays()

    i2c = busio.I2C(SCL_PIN, SDA_PIN)
    display_bus = i2cdisplaybus.I2CDisplayBus(
        i2c, device_address=OLED_ADDRESS
    )

    display = adafruit_displayio_ssd1306.SSD1306(
        display_bus, width=128, height=32
    )

    screen = displayio.Group()
    status_label = label.Label(
        terminalio.FONT,
        text="CommandPad ready",
        color=0xFFFFFF,
        x=0,
        y=10,
    )
    screen.append(status_label)
    display.root_group = screen

except Exception as error:
    print("OLED unavailable; other features will continue:", error)


# ---------- ROTARY ENCODER ----------
enc_a = digitalio.DigitalInOut(ENC_A_PIN)
enc_a.direction = digitalio.Direction.INPUT
enc_a.pull = digitalio.Pull.UP

enc_b = digitalio.DigitalInOut(ENC_B_PIN)
enc_b.direction = digitalio.Direction.INPUT
enc_b.pull = digitalio.Pull.UP

enc_sw = digitalio.DigitalInOut(ENC_SW_PIN)
enc_sw.direction = digitalio.Direction.INPUT
enc_sw.pull = digitalio.Pull.UP

last_ab = (enc_a.value, enc_b.value)
encoder_accumulator = 0

last_sw_raw = enc_sw.value
stable_sw = enc_sw.value
sw_changed_at = time.monotonic()

# Quadrature transition table. Direction may need reversing.
TRANSITIONS = {
    (0, 1): 1, (1, 3): 1, (3, 2): 1, (2, 0): 1,
    (1, 0): -1, (3, 1): -1, (2, 3): -1, (0, 2): -1,
}


def handle_encoder():
    global last_ab, encoder_accumulator
    global last_sw_raw, stable_sw, sw_changed_at

    ab = (enc_a.value, enc_b.value)
    old_code = (int(last_ab[0]) << 1) | int(last_ab[1])
    new_code = (int(ab[0]) << 1) | int(ab[1])

    if new_code != old_code:
        encoder_accumulator += TRANSITIONS.get(
            (old_code, new_code), 0
        )
        last_ab = ab

        # One volume action after four valid quadrature transitions.
        if encoder_accumulator >= 4:
            consumer.send(ConsumerControlCode.VOLUME_INCREMENT)
            encoder_accumulator = 0
            show_status("Volume up")

        elif encoder_accumulator <= -4:
            consumer.send(ConsumerControlCode.VOLUME_DECREMENT)
            encoder_accumulator = 0
            show_status("Volume down")

    raw = enc_sw.value
    now = time.monotonic()

    if raw != last_sw_raw:
        last_sw_raw = raw
        sw_changed_at = now

    elif raw != stable_sw and now - sw_changed_at >= DEBOUNCE:
        stable_sw = raw

        if not stable_sw:
            consumer.send(ConsumerControlCode.MUTE)
            show_status("Mute toggled")


# ---------- MAIN LOOP ----------
print("CommandPad firmware starting")
show_status("CommandPad ready")

while True:
    now = time.monotonic()
    currently_pressed = scan_matrix()

    for key in SHORTCUTS:
        raw = key in currently_pressed

        if raw != raw_key[key]:
            raw_key[key] = raw
            key_changed_at[key] = now

        elif (
            raw != stable_key[key]
            and now - key_changed_at[key] >= DEBOUNCE
        ):
            stable_key[key] = raw

            if raw:
                send_shortcut(SHORTCUTS[key])
                set_key_led(key, True)
                show_status("Key {} pressed".format(
                    key[0] * 3 + key[1] + 1
                ))
            else:
                set_key_led(key, False)

    handle_encoder()
    time.sleep(0.003)
