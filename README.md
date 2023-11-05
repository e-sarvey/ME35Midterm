# ME35Midterm

Welcome to my GitHub repository for my ME-35: Intro to Robotics midterm assignment. For a detailed overview of the project's requirements and my approach, please visit my [Notion page](https://www.notion.so/Midterm-Reading-the-Temperature-plus-some-8a9a66b3cea440bfb427b6d7f3f0bd2e?pvs=4).

The image processing part of the assignment was implemented using a PyScript page, which can be found [here](https://esarvey.pyscriptapps.com/me35-midterm-copy/latest/). My professor provided the HTML framework and some underlying Python functions, while I contributed my code to the REPL and saved it within the HTML. When you access the page, you can view the code I added. This program identifies the most prominent RGB channel of the largest object within the frame and updates an Airtable database with the detected color. The code I added to the REPL is also available as "cv2_pyscript.py" in this repository.

## Contents

- **MidtermPC**: 
  Python3 program that runs on a local PC to update the Adafruit Dashboard when the color cell changes in Airtable.

- **MidtermPico**: 
  MicroPython program designed to run on the Raspberry Pi Pico, which connects to Airtable, Adafruit IO, reads data from a thermistor and accelerometer, and controls a servo motor.

- **MidtermPyscript**: 
  Code input for the Pyscript REPL for processing the captured image to detect the color of the largest object in the frame, which can be red, green, or blue. The Airtable is updated accordingly using RestAPI.

- **ThermistorMath**: 
  Python3 program that I used to verify the mathematical calculations for determining the temperature from the thermistor resistance. It generates a plot illustrating the resistance-temperature curve for the thermistor and the ADC voltage-temperature curve when used in a voltage divider with a specific load resistor. The values within the program are based on measurements of the resistor used in the project.

- **accel**: 
  A simple module I created, based on code provided earlier in the semester. It facilitates reading data from the accelerometer. It defines an Accelerometer class, initialized with the corresponding I2C pins, and includes functions, `read_a()` and `read_g()`, which return tuples containing acceleration and gyroscope values, respectively.

- **connect2wifi**: 
  Another simple module I developed, based on code from earlier in the semester. It is responsible for connecting to the specified Wi-Fi network. It takes input in the form of a dictionary with the format `wifi={'ssid':'network_name','pass':'network_password'}`.

## Links to packages used that are not mine

- [GPIO LCD Control](https://www.circuitschools.com/interfacing-16x2-lcd-module-with-raspberry-pi-pico-with-and-without-i2c/#google_vignette)

- [micropython-servo](https://pypi.org/project/micropython-servo/)

Additionally, I referred to the following package to figure out how to connect to the Adafruit MQTT broker using paho-mqtt, although I did not integrate it directly into the final program:

- [Adafruit IO MQTT Package](https://github.com/adafruit/Adafruit_IO_Python/blob/master/Adafruit_IO/mqtt_client.py)
