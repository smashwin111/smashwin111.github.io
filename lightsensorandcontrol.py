# adapted from https://github.com/gallaugher/CPXBluefruitHalloweenHead/blob/master/code.py

import time

# Import the board-specific input/output library.
from adafruit_circuitplayground import cp

# Import the Adafruit Bluetooth library.  Technical reference:
# https://circuitpython.readthedocs.io/projects/ble/en/latest/api.html
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

#added for Day 3
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket

# ----------------------------------------------------------------
# Initialize global variables for the main loop.

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

print("Radio:", ble)
ble.name = 'CPB-36'
print("Radio name:", ble.name)

print("Advertisement:", advertisement)
print("UART:", uart)

# Flags for detecting state changes.
advertised = False
connected  = False


# The sensor sampling rate is precisely regulated using the following timer variables.
sampling_timer    = 0.0
last_time         = time.monotonic()
sampling_interval = 0.10

# ----------------------------------------------------------------
# Begin the main processing loop.

button4 = False

while True:

    # Read the accelerometer at regular intervals.  Measure elapsed time and
    # wait until the update timer has elapsed.
    now = time.monotonic()
    interval = now - last_time
    last_time = now
    sampling_timer -= interval
    if sampling_timer < 0.0:
        sampling_timer += sampling_interval
        x, y, z = cp.acceleration
        #added sound level later on
        sound_level = cp.sound_level
        #added outside light level later on
        light_level = cp.light
    else:
        x = None

    if not advertised:
        try:
            ble.start_advertising(advertisement)
        except:
            pass
        print("Waiting for connection.")
        advertised = True

    if not connected and ble.connected:
        print("Connection received.")
        connected = True
        cp.red_led = True

    if connected:
        if not ble.connected:
            print("Connection lost.")
            connected = False
            advertised = False
            cp.red_led = False
        else:
            if x is not None:
                if light_level < 1:
                    uart.write("Turn on lights\n")
                    time.sleep(1.0)

            if uart.in_waiting:
                try:
                    packet = Packet.from_stream(uart)
                except ValueError:
                    continue # or pass. This will start the next

                if isinstance(packet, ColorPacket): # check if a color was sent from color picker
                    cp.pixels.fill(packet.color)
                if isinstance(packet, ButtonPacket): # check if a button was pressed from control pad
                    if packet.pressed:
                        if packet.button == ButtonPacket.RIGHT:
                            for i in [0, 1, 2, 3, 4]:
                                cp.pixels[i] = (255,0,0)
                            for i in [5, 6, 7, 8, 9]:
                                cp.pixels[i] = (0,0,0)
                        if packet.button == ButtonPacket.LEFT:
                            for i in [5, 6, 7, 8, 9]:
                                cp.pixels[i] = (255,0,0)
                            for i in [0, 1, 2, 3, 4]:
                                cp.pixels[i] = (0,0,0)
                        if packet.button == ButtonPacket.UP:
                            for i in [2, 3, 4, 5, 6, 7]:
                                cp.pixels[i] = (255,0,0)
                            for i in [0, 1, 8, 9]:
                                cp.pixels[i] = (0,0,0)
                        if packet.button == ButtonPacket.DOWN:
                            for i in [0, 1, 2, 7, 8, 9]:
                                cp.pixels[i] = (255,0,0)
                            for i in [3, 4, 5, 6]:
                                cp.pixels[i] = (0,0,0)

                        #reset all neopixels
                        if packet.button == ButtonPacket.BUTTON_1:
                            for i in range(0, 10):
                                cp.pixels[i] = (0,0,0)
