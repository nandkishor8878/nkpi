from flask import Flask, Response
from camera import Camera
from flask import render_template
from services.communication.serial_service import serial_service

app = Flask(__name__)

camera = Camera()

def generate():
    while True:
        frame = camera.get_frame()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + frame +
            b'\r\n'
        )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/video")
def video():
    return Response(
        generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/led/on")
def led_on():

    response = serial_service.send("LED_ON")

    return {
        "status": "success",
        "response": response
    }


@app.route("/led/off")
def led_off():

    response = serial_service.send("LED_OFF")

    return {
        "status": "success",
        "response": response
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
