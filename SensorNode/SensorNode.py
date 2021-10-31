import Adafruit_DHT
from c8 import C8Client
import time
import base64
import six
import json
import warnings


def getMACAddress():

    # gives mac address without ':'
    mac = ''.join(re.findall('..', '%012x' % uuid.getnode()))
    return mac


DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

warnings.filterwarnings("ignore")

region = "gdn1.macrometa.io"
demo_tenant = "mytenant@example.com"
demo_fabric = "_system"
stream = "demostream"
# --------------------------------------------------------------
print("publish messages to stream...")
client = C8Client(protocol='https', host=region, port=443,
                  email=demo_tenant, password='hidden',
                  geofabric=demo_fabric)

producer = client.create_stream_producer(stream)


def getTempHumid():
    global DHT_SENSOR, DHT_PIN
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
        return [temperature,humidity]
    else:
        print("Failed to retrieve data from humidity sensor")

while 1:
    
    
    data='{"MacAddress": '+getMACAddress() + ',"Temperature_Humidity": ' +getTempHumid()+'}'
    producer.send(json.dumps(data))
    time.sleep(10)  # 10 sec
