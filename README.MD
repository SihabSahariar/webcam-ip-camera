# Webcam to IP Camera Flask App

This project is a Flask application that transforms a local webcam into an IP camera by streaming its video feed as an MJPEG stream. The stream is accessible via HTTP, allowing multiple clients to consume it simultaneously using tools like OpenCV (`cv2.VideoCapture`) or a web browser. It addresses the challenge of accessing a single webcam from multiple scripts, enabling concurrent use for tasks such as parallel model inference in computer vision applications.

## Necessity of the Project

Webcams typically allow only one process to access them at a time, creating conflicts when multiple scripts or models need to process the same camera feed simultaneously (e.g., for machine learning tasks like object detection, pose estimation, or facial recognition). This project solves this by:
- **Centralized Webcam Access**: The Flask app captures the webcam feed once and streams it as MJPEG, allowing multiple clients to access the feed without competing for webcam access.
- **Concurrent Model Inference**: Enables multiple scripts to process the same feed concurrently, ideal for running different machine learning models in parallel.
- **Cost-Effective Solution**: Utilizes existing webcams for networked video streaming without requiring dedicated IP cameras.
- **Flexibility**: Integrates seamlessly with computer vision pipelines using OpenCV or other libraries.
- **Prototyping and Development**: Facilitates rapid prototyping for IoT, surveillance, or multi-model inference applications.
- **Educational Value**: Demonstrates video streaming, Flask, and OpenCV integration for concurrent access scenarios.

## Requirements

### Software
- **Python 3.6+**
- **pip** (Python package manager)
- **Operating System**: Windows, macOS, or Linux (with a working webcam)

### Python Packages
- `flask` (for the web server)
- `opencv-python` (for webcam access and frame processing)
- `numpy` (for array operations with OpenCV)

### Hardware
- A webcam connected to the machine running the Flask app (usually accessible as device 0 in OpenCV).
- A network connection to allow clients to access the stream.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SihabSahariar/webcam-ip-camera.git
   cd webcam-ip-camera
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install flask opencv-python numpy
   ```

4. **Ensure Webcam Access**:
   - Verify that your webcam is connected and accessible (usually device 0 in OpenCV).
   - Test webcam access with a simple OpenCV script if needed.

## Usage

1. **Run the Flask App**:
   ```bash
   python app.py
   ```
   The app starts a server on `http://0.0.0.0:5000`, streaming the webcam feed as MJPEG.

2. **Access the Stream**:
   - **In a Browser**: Open `http://<server-ip>:5000/` to view the stream and access instructions.
   - **Programmatically with OpenCV** (e.g., for model inference):
     Save the following as `client.py`:
     ```python
     import cv2

     # Connect to the MJPEG stream
     ip_address = "<server-ip>"  # Replace with the server's IP address
     cap = cv2.VideoCapture(f'http://{ip_address}:5000/mjpeg')

     while True:
         ret, frame = cap.read()
         if not ret:
             print("Failed to retrieve frame")
             break
         
         # Example: Process frame (e.g., model inference)
         # Replace this with your model inference code
         cv2.imshow('Model Inference Client', frame)
         
         # Press 'q' to quit
         if cv2.waitKey(1) & 0xFF == ord('q'):
             break

     # Cleanup
     cap.release()
     cv2.destroyAllWindows()
     ```
     Run multiple instances of the client for different tasks (e.g., different models):
     ```bash
     python client.py
     ```
     Each client can process the stream independently.

3. **Stop the Server**:
   - Press `Ctrl+C` in the terminal to stop the Flask app. The webcam will be automatically released.

## Project Structure

```
webcam-ip-camera/
│
├── app.py          # Flask app to stream webcam as MJPEG
├── client.py       # Sample client script for accessing the MJPEG stream
├── README.md       # Project documentation
└── requirements.txt # List of Python dependencies
```

## Notes
- **Multiple Clients**: Run multiple `client.py` scripts (or custom scripts) to access the stream concurrently. Each client connects to `http://<server-ip>:5000/mjpeg`.
- **Model Inference**: Replace the placeholder in `client.py` with your model inference code (e.g., using TensorFlow, PyTorch, or OpenCV-based models).
- **Network Configuration**: Ensure port 5000 is open in your firewall to allow external access.
- **Performance**: For heavy processing, adjust frame size or JPEG quality in `app.py` (e.g., add `frame = cv2.resize(frame, (320, 240))` before encoding) to reduce bandwidth and processing load.
- **Security**: This is a basic implementation without authentication. For production, consider adding security measures like authentication or HTTPS.
- **Compatibility**: The MJPEG stream is compatible with OpenCV and most modern browsers.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for bug fixes, improvements, or new features.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.