from flask import Flask, Response
import cv2
import numpy as np
import socket

app = Flask(__name__)

# Initialize webcam
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Error: Could not open webcam. Ensure it is connected and not in use.")
    exit(1)

def generate_mjpeg():
    while True:
        # Read frame from webcam
        success, frame = camera.read()
        if not success:
            break
            
        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        # Yield frame in MJPEG format for multiple clients
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n'
               b'Content-Length: ' + str(len(frame)).encode() + b'\r\n\r\n'
               + frame + b'\r\n')

@app.route('/mjpeg')
def mjpeg_feed():
    # Serve MJPEG stream to multiple clients
    return Response(generate_mjpeg(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    # Get server IP address for mobile access
    hostname = socket.gethostname()
    server_ip = socket.gethostbyname(hostname)
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Webcam MJPEG Stream</title>
    </head>
    <body>
        <h1>Webcam MJPEG Stream</h1>
        <p>Access the MJPEG stream at: <code>/mjpeg</code></p>
        <p>Use in OpenCV with: <code>cv2.VideoCapture('http://{server_ip}:5000/mjpeg')</code></p>
        <p>From your mobile device (on the same Wi-Fi), visit: <a href="http://{server_ip}:5000/mjpeg">http://{server_ip}:5000/mjpeg</a></p>
        <img src="/mjpeg" style="width:100%; max-width:640px; height:auto;">
    </body>
    </html>
    """

if __name__ == '__main__':
    try:
        print("Starting server on http://0.0.0.0:5000")
        app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    finally:
        # Release camera when app stops
        camera.release()