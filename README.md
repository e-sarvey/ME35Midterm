# ME35Midterm
Welcome to my GitHub repository for my ME-35: Intro to Robotics midterm assignment.
To see all the details about what the project entailed and how I completed it check out my [Notion page](https://www.notion.so/Midterm-Reading-the-Temperature-plus-some-8a9a66b3cea440bfb427b6d7f3f0bd2e?pvs=4).

The image processing part of the assignment was done using a PyScript page which can be found [here](https://esarvey.pyscriptapps.com/me35-midterm-copy/latest/).
My professor created the HTML outline and some underlying python functions, and I added my code to the repl and saved it in the HTML so when the page loads you can see the code I added. This program detects the most prominent rgb channel of the largest item placed in the frame and updates an Airtable database with that color. I also added the code I added to the repl as the file "cv2_pyscript.py" in this repository.

Contents:
- MidtermPC: Python3 program that runs on local PC to update Adafruit Dashboard when the color cell changes in Airtable.
- MidtermPico: Micropython program that runs on the Raspberry Pi Pico and connects to Airtable, Adafruit IO, reads a thermistor and accelerometer, and controls a servo motor.
- MidtermPyscript: Code input to the Pyscript repl that processes the image captured to detect if the color of the largest object in the frame is red, green, or blue and updates the Airtable accordingly.
- ThermistorMath: Python3 program that I used to verify the math used to calculate the temperature from the thermistor resistance. It creates a plot that shows the resistance-temperature curve for the thermistor and ADC voltage-temperature curve if used in a voltage divider with a certain load resistor. The current values in the program are based on the measured values for the resistor used in the project.
- accel: A simple module I created based on code provided earlier in the semester which is used to read the accelerometer. It defines an Accelerometer class which is initialized with the corresponding i2c pins used and has functions, '''_.read_a()''' and '''_.read_g()''' which return a tuple with the acceleration and gyroscope values respectively.
- connect2wifi: A simple module I created based on code provided earlier in the semester which connects to the wifi network specified in the input. It takes a dictionary input with the format '''wifi={'ssid':'network_name','pass': 'network_password}'''

Links to packages used that are not mine:
- [GPIO LCD Control](https://www.circuitschools.com/interfacing-16x2-lcd-module-with-raspberry-pi-pico-with-and-without-i2c/#google_vignette)
- [micropython-servo](https://pypi.org/project/micropython-servo/)

And this package I used to figure out how to connect to the Adafruit MQTT broker using paho-mqtt although I did not use it in the final program:
- [Adafruit IO MQTT Package](https://github.com/adafruit/Adafruit_IO_Python/blob/master/Adafruit_IO/mqtt_client.py)

