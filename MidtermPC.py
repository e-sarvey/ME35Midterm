import requests, json, time
from mysecrets import ATsecrets, DashSecrets
import paho.mqtt.client as mqtt

# Initialize Airtable Rest API access (this is a lot of the same code used on pyscript page)
api_key = ATsecrets['token']
base_id = 'appCUx68GT006rHir'
table_name = 'Color Detection History'
url = f'https://api.airtable.com/v0/{base_id}/{table_name}/recDBFD7dJnbrfVHM'

# set up MQTT communication with Adafruit
broker = 'io.adafruit.com' 
port = 1883
username = DashSecrets['username']
key = DashSecrets['key']
topic = "esarvey/feeds/COLOR/json"

# Function that returns the current color posted to the Airtable "Color Detection History"
def GetCurrentColor():
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        current_color = data.get('fields', {}).get('Color')
        print(current_color)
        return current_color
    else:
        print(f"Failed to get data. Status code: {response.status_code}")

def Post2AIO(data): # posts data to adafruit IO
    try:
        client = mqtt.Client()
        client.username_pw_set(username=username, password=key) # this was the tricky thing to figure out!
        # figured out this by reading through the AIO library MQTTClient class: https://github.com/adafruit/Adafruit_IO_Python/blob/master/Adafruit_IO/mqtt_client.py
        
        client.connect(broker, port)
        data = json.dumps({"value":data}) # needs to be in a json string format for adafruit to interpret
        (res, mid) = client.publish(topic, data, qos=1)
        time.sleep(1)
        print(f"Published message with result: {res}, mid: {mid}")
    except Exception as e:
        print(f"An error occurred in Post2AIO: {str(e)}")

## main code ##
def main():
    color_prev = []
    # main loops to check the current color, compares to prev color and updates AIO if it is different.
    while True:
        color = GetCurrentColor()
        if color != color_prev:
            Post2AIO(str(color))
            color_prev = color
        elif color == color_prev:
            print('color has not changed')
            pass
        time.sleep(2)

try:
    main()
except Exception as e:
    print(e)
finally:
    print('finished')
    print('------------------------------')



