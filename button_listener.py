import RPi.GPIO as GPIO
import subprocess
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up GPIO pin
button_pin = 4
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to execute when button is pressed
def button_pressed(channel):
    # Execute the Python program or shell command here
    subprocess.call(["python", "/home/meska/BeMyReader/camera.py"])

# Add event listener for button press
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_pressed, bouncetime=300)

try:
    # Main program loop
    while True:
        #include delays to avoid excessive CPU usage
        time.sleep(0.1)  # Add a small delay (e.g., 0.1 seconds) between iterations

except KeyboardInterrupt:
    # Clean up GPIO on keyboard interrupt
    GPIO.cleanup()
