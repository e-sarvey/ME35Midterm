import time, math, json, network
from accel import Accelerometer
from machine import Pin, ADC
import connect2wifi as c2w
from stepper import Stepper
from servo import Servo
from gpio_lcd import GpioLcd
from mysecrets import *
import umqtt as mqtt
import uasyncio as asyncio
import urequests as requests
# woah thats a lot of imports (⊙﹏⊙)

# Initialize the accelerometer using my accelerometer library
AC = Accelerometer(1, 19, 18)

# Initialize servo using simple servo library
servo = Servo(16,500,2500,0.0,180.0,50)

# Initialize LCD pins using LCD library
lcd = GpioLcd(rs_pin=Pin(13),
              enable_pin=Pin(12),
              d4_pin=Pin(11),
              d5_pin=Pin(10),
              d6_pin=Pin(9),
              d7_pin=Pin(8),
              num_lines=2, num_columns=16)

# init thermistor
thermistor = machine.ADC(1)

client_name = 'Elijah_Client'
broker = 'io.adafruit.com' 
port = 1883 # 8883 if using SSL but would need more info for this
username = DashSecrets['username']
key = DashSecrets['key']
topic = "esarvey/feeds/temp/json"

client = mqtt.MQTTClient(client_name, broker, port, 'esarvey', DashSecrets['key'], keepalive=60)


# Initialize Airtable Rest API access (this is a lot of the same code used on pyscript page)
api_key = ATsecrets['token']
base_id = 'appCUx68GT006rHir'
table_name = 'tblETnsnuu3toJ1ok' # used table id here since parsing the table name to a url is handled differently in urequests...
url = f'https://api.airtable.com/v0/{base_id}/{table_name}/recDBFD7dJnbrfVHM'
#print(url)

# -------------------------------------------------------------------------- #
def GetCurrentColor():
    # Function that returns the current color posted to the Airtable "Color Detection History"
    # This is the same function that is used in the VScode program and pyscript page to get the current color from airtable
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
        print("Failed to get data. Status code:", response.status_code)

def moveServo():
    a = AC.read_a() # read accelerometer
    ax = a[0]
    az = a[2]
    angle = (90 - (math.atan2(ax, az) * (180 / math.pi)))  # Calculate angle from the x-axis (ax could be 0 so subtract to prevent NaN error)
    #print(angle)

    # set servo angle with limits to prevent damage to hardware.
    if 135.0 >= angle >= 50.0:
        servo.write(angle)
    elif angle > 135.0:
        servo.write(135)
    elif angle < 50.0:
        servo.write(50.0)
    else:
        pass
    
def readTherm():
    R = 9300 # resistance of resistor in voltage divider, measured using multimeter
    R1 = 10_500 # resistance of calibration resistor
    T1 = 24.1 + 273.15 # Calibration temp of thermistor
    B = 3381.6 # Beta value of thermistor, calculated experimentally
    
    u16_adc = thermistor.read_u16() # read ADC as u16
    V_adc= 3.3*(u16_adc/65535) # convert u16 ADC reading to voltage
    
    R_th = ((3.3*R)/V_adc)-R # calculate resistance of thermistor
    
    Temp_C = B * (math.log(R_th/ R1) + (B / T1))**-1 - 273.15 
    #print(Temp_C, V_adc)
    return Temp_C


def readTemp(color):
    color2unit = {'Blue':'K','Green':'C','Red':'F'}
    unit = color2unit[color]
    # function takes unit input based on open CV program/REST
    temp_c = readTherm() #read thermistor value
    
    if unit == 'K':
        temp = temp_c+273.15
    elif unit == 'C':
        temp = temp_c
    elif unit == 'F':
        temp = temp_c*(9/5) + 32
    # display result on LCD
    lcd.clear()
    lcd.move_to(1,0) # move cursor to first position
    lcd.putstr(str(round(temp,2)) + unit)
    return temp, unit

def AIO_MQTT_Publish(temp,unit):
    # publishes temp (or really any value) to the "temp" feed on Adafruit IO dashboard using their MQTT Broker
    try:
        client.connect()
        msg = json.dumps({"value":str(round(temp,2)) + unit})
        client.publish(topic,msg, qos=1)
        client.disconnect()
    except Exception as e:
             print(f'Failed to connect to MQTT server @ {broker}: {e}')

# ------------------ ASYNC COROUTINES--------------------------- #

async def ServoCoroutine():
    while True:
        moveServo()
        #('moving servo')
        await asyncio.sleep(0.1)

async def LCDCoroutine():
    while True:
        global color
        temp, unit = readTemp(color)
        lcd.clear()
        lcd.move_to(1, 0)
        lcd.putstr(f"{round(temp, 2)} {unit}")
        print('LCD')
        await asyncio.sleep(2)

async def ColorCoroutine():
    while True:
        global color
        color = GetCurrentColor()
        print('getting color')
        await asyncio.sleep(5)

async def AdaPubCoroutine():
    while True:
        global color
        temp, unit = readTemp(color)
        AIO_MQTT_Publish(temp, unit)
        print('publishing')
        await asyncio.sleep(45)
        
async def main():
        await asyncio.gather(
            ServoCoroutine(),
            LCDCoroutine(),
            ColorCoroutine(),
            AdaPubCoroutine()
        )

# ------------------ MAIN STATES --------------------------- #

def initState():
    global color, temp, unit
    # setup wifi on board
    lcd.putstr('...BOOTING UP...')
    station = network.WLAN(network.STA_IF) # check if already connected to wifi
    if not station.isconnected(): # connect to wifi if not already
        c2w.connect_wifi(Tufts_Wireless) # Tufts_Wireless referenced via secrets
    
    # synchronous to establish intial values
    color = GetCurrentColor() # need an initial color to define the first unit used
    temp, unit = readTemp(color)
    print('Initialization complete')

def endState():
    # code to run with finally statement. Resets machine outputs.
    servo.write(90)
    lcd.clear()
    machine.soft_reset()

# --------------------------------------------- #
    
## RUN PROGRAM HERE ##
try:
    initState()
    asyncio.run(main())
    
except Exception as e:
    print(f'uh oh... an error has occured in the main loop: {e}')
finally:
    endState()
    print('El Fin!')
    
    
    




