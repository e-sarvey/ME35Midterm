# ME35Midterm
Welcome to my GitHub repository for my ME-35: Intro to Robotics midterm assignment.
To see all the details about what the project entailed and how I completed it check out my [notion page](https://www.notion.so/Midterm-Reading-the-Temperature-plus-some-8a9a66b3cea440bfb427b6d7f3f0bd2e?pvs=4).

The image processing part of the assignment was done using a PyScript page which can be found [here](https://esarvey.pyscriptapps.com/me35-midterm-copy/latest/).
My professor created the HTML outline and some underlying python functions, and I added my code to the repl and saved it in the HTML so when the page loads you can see the code I added. This program detects the most prominent rgb channel of the largest item placed in the frame and updates an Airtable database with that color. I also added the code I added to the repl as the file "cv2_pyscript.py" in this repository.

Links to packages used that are not mine:
- [GPIO LCD Control](https://www.circuitschools.com/interfacing-16x2-lcd-module-with-raspberry-pi-pico-with-and-without-i2c/#google_vignette)
- [micropython-servo](https://pypi.org/project/micropython-servo/)

And this package I used to figure out how to connect to the Adafruit MQTT broker using paho-mqtt although I did not use it in the final program:
- [Adafruit IO MQTT Package](https://github.com/adafruit/Adafruit_IO_Python/blob/master/Adafruit_IO/mqtt_client.py)

