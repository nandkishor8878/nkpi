from flask import Flask, Response
from camera import Camera

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
    return """
    <html>
    <head>
        <title>Smart Reception Assistant</title>
    </head>
    <body>
        <h1>🤖 Smart Reception Assistant</h1>
        <img src="/video" width="640">
    </body>
    </html>
    """

@app.route("/video")
def video():
    return Response(
        generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
