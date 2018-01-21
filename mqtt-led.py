import logging
from rpi_ws281x import rpi_ws281x
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.basicConfig(level=logging.DEBUG)



    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("status_led/+", 1)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        led = msg.topic.split("/")[-1]
        logging.debug("Trying to convert {} to integer".format(led))
        led = int(led)
        text = msg.payload.decode("utf-8")
        logging.info("Message '{}' is meant for LED {}".format(text, led))
        if text[0:4] == "rgb:":
            red, green, blue = text[4:].split(",")
            client.strip.setPixelColor(led-1, rpi_ws281x.Color(int(red), int(green), int(blue)))
            client.strip.show()
            logging.info("LED {} set to red {}, green {}, blue {}".format(led, red, green, blue))
        elif text[0:4] == "hex:":
            hex = text[4:].lstrip("#")
            red, green, blue = tuple(int(hex[i:i+2], 16) for i in (0, 2 ,4))
            client.strip.setPixelColor(led-1, rpi_ws281x.Color(int(red), int(green), int(blue)))
            client.strip.show()
            logging.info("LED {} set to red {}, green {}, blue {}".format(led, red, green, blue))
    except:
        logging.exception("Converting to int failed")

LED_COUNT      = 8      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 127     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = rpi_ws281x.ws.WS2811_STRIP_GRB   # Strip type and colour ordering

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.strip = rpi_ws281x.Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
client.strip = rpi_ws281x.PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
client.strip.begin()
for i in range(0, LED_COUNT):
    client.strip.setPixelColor(i, rpi_ws281x.Color(0, 255, 0))
client.strip.show()
client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
