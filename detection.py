import cv2 as cv
import time
import requests
import os


def send_file(path):
    # Retrieve access token and group ID from environment variables
    access_token = os.environ["TelegramTok"]
    group_id = os.environ["GroupID"]

    # Prepare file for upload
    files = {'video': open(path, 'rb')}

    # Send video file to Telegram using Bot API
    resp = requests.post(f'https://api.telegram.org/bot{access_token}/sendVideo?chat_id=-{group_id}', files=files)

    # Check if the response status code is 200 (OK)
    return str(resp.status_code) == "200"


def make_recording(duration=10):
    # Initialize video capture and recording parameters
    fp = "recording.mp4"
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)  # Open default camera
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)  # Set frame width
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)  # Set frame height
    fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')  # Define codec
    out = cv.VideoWriter(fp, fourcc, 30.0, (640, 480))  # VideoWriter object

    # Start recording for specified duration
    start_time = time.time()
    while int(time.time() - start_time) < duration:
        ret, frame = cap.read()  # Read frame from camera
        if ret:
            out.write(frame)  # Write frame to video file
        else:
            break

    # Release video capture and recording objects
    cap.release()
    out.release()

    # Return filepath of the recorded video
    return fp


if __name__ == '__main__':
    # Initialize object detection parameters
    consecutive_frames = 75  # Number of consecutive frames with a bird required
    bird_frame_counter = 0  # Counter for frames containing a bird

    Conf_threshold = 0.4  # Confidence threshold for object detection
    NMS_threshold = 0.4  # Non-maximum suppression threshold
    COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0),
              (255, 255, 0), (255, 0, 255), (0, 255, 255)]

    class_name = []
    with open('classes.txt', 'r') as f:
        class_name = [cname.strip() for cname in f.readlines()]

    # Load YOLOv4-tiny model for object detection
    net = cv.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

    model = cv.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1 / 255, swapRB=True)

    # Initialize video capture from default camera
    cap = cv.VideoCapture(0)
    starting_time = time.time()
    frame_counter = 0

    # Main loop for real-time object detection
    while True:
        bird_in_frame = False
        ret, frame = cap.read()  # Read frame from camera
        frame_counter += 1

        if not ret:
            break

        # Perform object detection on the frame
        classes, scores, boxes = model.detect(frame, Conf_threshold, NMS_threshold)

        for (classid, score, box) in zip(classes, scores, boxes):
            cls_name = class_name[classid[0]]

            # Check if the detected object is a bird
            if cls_name == 'bird':
                bird_in_frame = True
                color = COLORS[int(classid) % len(COLORS)]
                label = f"{cls_name} : {score}"

                # Draw bounding box and label around the detected bird
                cv.rectangle(frame, box, color, 1)
                cv.putText(frame, label, (box[0], box[1] - 10),
                           cv.FONT_HERSHEY_COMPLEX, 0.3, color, 1)

        # Calculate frames per second (FPS) and display on the frame
        endingTime = time.time() - starting_time
        fps = frame_counter / endingTime
        cv.putText(frame, f'FPS: {fps:.2f}', (20, 50),
                   cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

        # Update bird frame counter if a bird is detected in the frame
        bird_frame_counter += 1 if bird_in_frame else 0

        # Check if enough consecutive frames contain a bird
        if bird_frame_counter >= consecutive_frames:
            bird_frame_counter = 0
            cap.release()  # Release camera to prepare for recording
            recording = make_recording(duration=10)  # Record a 10-second video

            # Send recorded video to Telegram
            if not send_file(recording):
                exit("Error - Video could not be sent on Telegram.")

            # Reinitialize camera for object detection
            cap = cv.VideoCapture(0)

        # Display the processed frame with overlays
        cv.imshow('frame', frame)

        # Check for user input to exit the program
        key = cv.waitKey(1)
        if key == ord('q'):
            break

    # Release camera and close all OpenCV windows
    cap.release()
    cv.destroyAllWindows()
