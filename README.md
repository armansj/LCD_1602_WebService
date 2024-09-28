Pico W Web Server with LCD Display

This project demonstrates how to use a Raspberry Pi Pico W as a web server to control and display messages on an I2C LCD. By accessing the web interface, users can input text, which is then displayed on the LCD connected to the Pico W. The project also uses a background subtraction method to ensure continuous WiFi connection monitoring.

Features

Web Server: Hosts a web interface that allows users to input custom text.
LCD Display: Displays user-inputted text on a 16x2 LCD using I2C communication.
Counter: Includes a counter that updates on the second row of the LCD.
WiFi Connectivity: Connects to a WiFi network for remote control.
Socket Communication: Manages HTTP requests using a socket connection.
Requirements

Raspberry Pi Pico W
I2C 16x2 LCD Display
Breadboard and Jumper Wires
Micro USB cable
WiFi connection


How to Use

Power On the Raspberry Pi Pico W.
Connect to the web server via the Pico's IP address, which will be printed in the serial monitor once it connects to the WiFi.
Open the Web Interface:
Open a browser and type the Pico’s IP address. You'll see a text input field and a submit button.
Enter Text: Input your desired text in the text box and click "Save". The text will be displayed on the LCD.
