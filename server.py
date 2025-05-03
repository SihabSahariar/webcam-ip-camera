from flask import Flask, Response
import cv2
import numpy as np

app = Flask(__name__)

# Initialize webcam (single access point for all clients)
camera = cv2.VideoCapture(0)

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
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Webcam MJPEG Stream</title>
    </head>
    <body>
        <h1>Webcam MJPEG Stream</h1>
        <p>Access the MJPEG stream at: <code>/mjpeg</code></p>
        <p>Use in OpenCV with: <code>cv2.VideoCapture('http://&lt;server-ip&gt;:56000/mjpeg')</code></p>
        <img src="/mjpeg" style="width:640px; height:480px;">
    </body>
    </html>
    """

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    finally:
        # Release camera when app stops
        camera.release()