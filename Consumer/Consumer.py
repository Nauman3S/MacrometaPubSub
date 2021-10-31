from c8 import C8Client
import time
import base64
import six
import json
import warnings
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

subscriber = client.subscribe(
       stream=stream, local=False, subscription_name="test-subscription-1")
for i in range(10):

    print("In ", i)
    # Listen on stream for any receiving msg's
    m1 = json.loads(subscriber.recv())
    msg1 = base64.b64decode(m1["payload"])
    # Print the received msg over   stream
    print("Received message '{}' id='{}'".format(msg1, m1["messageId"]))
    # Acknowledge the received msg.
    subscriber.send(json.dumps({'messageId': m1['messageId']}))

print(client.get_stream_subscriptions(stream=stream, local=False))

print(client.get_stream_backlog(stream=stream, local=False))
