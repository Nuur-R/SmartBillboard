import cv2
from ultralytics import YOLO
import numpy as np
import matplotlib.pyplot as plt

# Load the YOLOv8 model
model = YOLO('models/yolov8s.pt')

# Open the video file
video_path = "Video/20240524_071138.mp4"
cap = cv2.VideoCapture(video_path)

# Define the polygon area (example polygon coordinates)
polygon_points = np.array([[100, 100], [500, 100], [500, 400], [100, 400]])

# Cek apakah video berhasil dibuka
if not cap.isOpened():
    print(f"Error: Tidak dapat membuka video {video_path}")
else:
    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame)

            # Filter results based on polygon area
            filtered_results = []
            for result in results:
                for detection in result.boxes:
                    bbox = detection.xyxy[0].cpu().numpy().astype(int)
                    center_x = int((bbox[0] + bbox[2]) // 2)
                    center_y = int((bbox[1] + bbox[3]) // 2)
                    if cv2.pointPolygonTest(polygon_points, (center_x, center_y), False) >= 0:
                        filtered_results.append(detection)

            # Draw the polygon area on the frame
            cv2.polylines(frame, [polygon_points], isClosed=True, color=(0, 255, 0), thickness=2)

            # Visualize the filtered results on the frame
            for detection in filtered_results:
                bbox = detection.xyxy[0].cpu().numpy().astype(int)
                label = result.names[detection.cls[0].cpu().item()]
                confidence = detection.conf[0].cpu().item()

                x1, y1, x2, y2 = bbox
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # Display the annotated frame using matplotlib
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            plt.imshow(frame_rgb)
            plt.axis('off')
            plt.show()

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # Break the loop if the end of the video is reached
            break

    # Release the video capture object and close the display window
    cap.release()
