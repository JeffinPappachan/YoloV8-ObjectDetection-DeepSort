import os
import random
from ultralytics import YOLO
import cv2
from tracker import Tracker

video_path = os.path.join('.', 'data', 'people.mp4')
video_out_path = os.path.join('.', 'out.mp4')

cap = cv2.VideoCapture(video_path)  # Initialize cap with the input video path
ret, frame = cap.read()  # Read the first frame to get the frame dimensions

if not ret:
    print("Failed to read the video")
    cap.release()
    exit()

# Initialize the VideoWriter with the correct parameters
cap_out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS),
                          (frame.shape[1], frame.shape[0]))

model = YOLO('yolov8n.pt')
tracker = Tracker()

colors =[(random.randint(0,255),random.randint(0,255),random.randint(0,255)) for j in range(10)]

detection_threshold = 0.5



while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    for result in results:
        detections = []
        for r in result.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = r
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)
            class_id= int(class_id)
            if score > detection_threshold:
                detections.append([x1, y1, x2, y2, score])  # Append coordinates and score

        tracker.update(frame, detections)

        for track in tracker.tracks:
            bbox = track.bbox
            x1, y1, x2, y2 = bbox
            track_id = track.track_id

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), colors[track_id % len(colors)], 3)

    cap_out.write(frame)

    ret,frame =cap.read()

cap.release()
cap_out.release()
cv2.destroyAllWindows()