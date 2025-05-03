import cv2
ip_address = "127.0.0.1"  # Replace with the server's IP address
cap = cv2.VideoCapture(f'http://{ip_address}:5000/mjpeg')
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('MJPEG Stream', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()