#!/usr/bin/env python3
import logging
import paho.mqtt.client as mqtt
import sys

try:
  logging.basicConfig(level=logging.DEBUG)
  server_ip = "127.0.0.1"

  topic = sys.argv[1]
  msg = " ".join(sys.argv[2:])

  client = mqtt.Client("monit")
  client.connect(server_ip)
  client.publish(topic, msg, qos=1, retain=True)
except:
  logging.exception("something failed miserably")
