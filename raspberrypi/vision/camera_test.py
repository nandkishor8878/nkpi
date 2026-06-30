from picamera2 import Picamera2

picam2 = Picamera2()

picam2.start()

metadata = picam2.capture_file("image.jpg")

print("Image captured successfully!")
