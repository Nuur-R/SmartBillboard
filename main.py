import cv2
import supervision as sv  # Assuming supervision library is available
from ultralytics import YOLO
import numpy as np

# Define the polygon coordinates
polygon = np.array([
    [84, 1064],
    [1090, 418],
    [1247, 419],
    [989, 1059],
])

# Define text properties
FONT_SCALE = 1  # Font size for text
TEXT_COLOR = (0, 255, 0)  # Text color (BGR)
TEXT_THICKNESS = 2  # Text thickness

def initialize_model(model_path):
    """
    Initialize the YOLO model.
    
    Args:
        model_path (str): Path to the YOLO model weights.
    
    Returns:
        model: Loaded YOLO model.
    """
    return YOLO(model_path)

def process_frame(frame, model, zone):
    """
    Process a single frame for object detection and annotation.
    
    Args:
        frame (ndarray): Input frame from the video.
        model (model): YOLO model for object detection.
        zone (PolygonZone): PolygonZone object for defining detection area.
    
    Returns:
        annotated_frame (ndarray): Annotated frame with bounding boxes and labels.
        class_counts (dict): Dictionary with counts of detected classes.
    """
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    mask = zone.trigger(detections=detections)
    detections = detections[np.isin(detections.class_id, [2, 3]) & mask]

    class_counts = {}
    for class_name in detections['class_name']:
        if class_name in class_counts:
            class_counts[class_name] += 1
        else:
            class_counts[class_name] = 1

    labels = [
        f"{class_name} {confidence:.2f}"
        for class_name, confidence
        in zip(detections['class_name'], detections.confidence)
    ]

    bounding_box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    annotated_frame = bounding_box_annotator.annotate(scene=frame, detections=detections)
    annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
    annotated_frame = sv.draw_polygon(scene=frame, polygon=polygon, color=sv.Color.red(), thickness=6)

    return annotated_frame, class_counts

def display_frame(frame, class_counts, text_position=(20, 20)):
    """
    Display the frame with text annotations.
    
    Args:
        frame (ndarray): Frame to be displayed.
        class_counts (dict): Dictionary with counts of detected classes.
        text_position (tuple, optional): Position for displaying text. Defaults to (20, 20).
    """
    for class_name, count in class_counts.items():
        line = f"{class_name}: {count}"
        cv2.putText(frame, line, text_position, cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, TEXT_COLOR, TEXT_THICKNESS)
        text_position = (text_position[0], text_position[1] + 30)  # Adjust y-coordinate for each line

    window_name = "Frame"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, frame)

def write_state_to_file(class_counts, filename='state.txt'):
    """
    Write the class name with the highest count to a file.
    
    Args:
        class_counts (dict): Dictionary with counts of detected classes.
        filename (str, optional): Name of the file to write the state to. Defaults to 'state.txt'.
    """
    if not class_counts:
        return
    
    most_common_class = max(class_counts, key=class_counts.get)
    with open(filename, 'w') as file:
        file.write(most_common_class)

def read_video_and_annotate(video_path, model_path='models/yolov8s.pt'):
    """
    Reads a video file, performs object detection using YOLO, and displays the results with bounding boxes and labels.
    
    Args:
        video_path (str): Path to the video file.
        model_path (str, optional): Path to the YOLO model weights. Defaults to 'models/yolov8n.pt'.
    """
    video_info = sv.VideoInfo.from_video_path(video_path)
    zone = sv.PolygonZone(polygon=polygon, frame_resolution_wh=video_info.resolution_wh)
    model = initialize_model(model_path)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video stream or file")
        return

    while True:
        ret, frame = cap.read()
        if not ret or cv2.waitKey(1) & 0xFF == ord('q'):
            break

        annotated_frame, class_counts = process_frame(frame, model, zone)
        display_frame(annotated_frame, class_counts)
        write_state_to_file(class_counts)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    video_path = 'video/3s.mp4'  # Replace with your video path
    read_video_and_annotate(video_path)
