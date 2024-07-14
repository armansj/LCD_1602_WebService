import machine
import time
import socket
import network
from machine import I2C, Pin
from I2C_LCD import I2CLcd


# URL decode function
def url_decode(s):
    import ubinascii
    s = s.replace('+', ' ')
    s = s.split('%')
    s[0] = s[0].encode()
    for i in range(1, len(s)):
        s[i] = bytes([int(s[i][:2], 16)]) + s[i][2:].encode()
    return b''.join(s).decode()


# Set up I2C for the LCD
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
devices = i2c.scan()

# WiFi credentials
ssid = 'Vodafone-820C'  # Enter the router name
password = 'xc5dadQYrqpo2J2sd2q2'  # Enter the router password

# Initialize WiFi
wifi_status = network.WLAN(network.STA_IF)
wifi_status.disconnect()
wifi_status.active(True)
wifi_status.connect(ssid, password)


# HTML Page
def WebPage(gpio_text):
    html = """
    <html>
        <head>
            <title>Pico W Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" href="data:,">
            <style>
                html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
                h1{color: #0F3376; padding: 2vh;}
                p{font-size: 1.5rem;}
                button{display: inline-block; background-color: #4286f4; border: none; border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
                .button2{background-color: #4286f4;}
                input[type="text"]{width: 80%; padding: 12px; margin: 8px 0; box-sizing: border-box;}
                input[type="submit"]{width: 80%; padding: 14px 20px; margin: 8px 0; cursor: pointer;}
            </style>
        </head>
        <body> 
            <h1>Pico W Web Server</h1> 
            <p>GPIO state: <strong>""" + gpio_text + """</strong></p>
            <form action="/" method="GET">
                <input type="text" id="lname" name="text" value="""" + gpio_text + """"><br><br>
                <input type="submit" value="Save" class="button">
            </form>
        </body>
    </html>
    """
    return html


# Check WiFi connection
while not wifi_status.isconnected():
    time.sleep(1)
    print('Connecting to a wireless network...')

# If connected
print('WiFi connected successfully')
print(wifi_status.ifconfig())

# Set up the socket server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Add this line
s.bind(('', 80))
s.listen(5)

try:
    while True:
        conn, addr = s.accept()
        print('Connection from: %s' % str(addr))
        req = conn.recv(1024)
        req = str(req)
        print('Request: %s' % req)

        # Extract the text from the request
        text_start = req.find('/?text=') + 7
        text_end = req.find(' ', text_start)
        if text_start > 6 and text_end > text_start:
            gpio_text = url_decode(req[text_start:text_end])
        else:
            gpio_text = "Hello, World!"  # Default text

        # Display the text on the LCD
        if devices:
            lcd = I2CLcd(i2c, devices[0], 2, 16)
            lcd.move_to(0, 0)
            lcd.putstr(gpio_text)
            count = 0
            while count < 10:  # Example to avoid infinite loop, remove or adjust as needed
                lcd.move_to(0, 1)
                lcd.putstr("Counter:%d" % count)
                time.sleep(1)
                count += 1
        else:
            print("No I2C device found")

        # Send the HTML response
        response = WebPage(gpio_text)
        conn.send('HTTP/1.1 200 OK\r\n')
        conn.send('Content-Type: text/html\r\n')
        conn.send('Connection: close\r\n\r\n')
        conn.sendall(response.encode('utf-8'))
        conn.close()
except Exception as e:
    print('Error:', e)
finally:
    s.close()  # Ensure the socket is closed properly

