import RPi.GPIO as GPIO
import time
import subprocess
import os
import image

from picamera import PiCamera
from upload import toS3


# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variables
button_state = False
button_press_time = 0
long_press_duration = 3  # seconds
recording = False
current_video_file = ""
camera = None

def capture_image():
    with PiCamera() as camera:
        timestamp = time.strftime("%y%m%d-%H%M%S")
        image_name = f"image_{timestamp}.jpg"
        camera.capture(image_name)
        print(f"Captured image: {image_name}")
        toS3(image_name)
        delete_file(image_name)
        #image.main('noText.jpg')

def record_video():
    global recording, current_video_file, camera
    camera = PiCamera()
    recording = True
    timestamp = time.strftime("%y%m%d-%H%M%S")
    current_video_file = f"video_{timestamp}.h264"
    camera.start_recording(current_video_file, format='h264')
    print(f"Started recording: {current_video_file}")

def stop_video():
    global recording, current_video_file, camera
    if recording:
        recording = False
        camera.stop_recording()
        print("Stopped recording")
        camera.close()
        convert_to_mp4(current_video_file)
        toS3(os.path.splitext(current_video_file)[0] + '.mp4')
        delete_file(current_video_file)
        delete_file(os.path.splitext(current_video_file)[0] + '.mp4')

def convert_to_mp4(video_file):
    timestamp = time.strftime("%y%m%d-%H%M%S")
    output_file = f"{os.path.splitext(video_file)[0]}.mp4"
    command = f"MP4Box -add {video_file} {output_file}"
    subprocess.run(command, shell=True)
    print(f"Converted to MP4: {output_file}")

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted file: {file_path}")

# Button event callback
def button_callback(channel):
    global button_state, button_press_time
    if GPIO.input(channel) == GPIO.LOW:
        button_state = True
        button_press_time = time.time()
    else:
        button_state = False
        press_duration = time.time() - button_press_time

        if press_duration < long_press_duration:
            capture_image()
        else:
            stop_video()

# Register button event handler
GPIO.add_event_detect(4, GPIO.BOTH, callback=button_callback, bouncetime=200)

try:
    while True:
        if button_state and GPIO.input(4) == GPIO.LOW:
            press_duration = time.time() - button_press_time
            if press_duration > long_press_duration and not recording:
                record_video()
        time.sleep(0.1)  # Add a small delay to reduce CPU usage

except KeyboardInterrupt:
    if camera is not None:
        camera.close()
    GPIO.cleanup()
