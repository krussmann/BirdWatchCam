import cv2 as cv
import time
import requests
import os

def send_file(path):
    acces_token = os.environ["TelegramTok"]
    group_id = os.environ["GroupID"]
    files ={'video':open(path, 'rb')}
    resp = requests.post(f'https://api.telegram.org/bot{acces_token}/sendVideo?chat_id=-{group_id}', files=files)
    if str(resp.status_code) == "200":
        return True
    else:
        return False

def make_recording(duration=10):
    fp = "recording.mp4"
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
    fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv.VideoWriter(fp, fourcc, 20.0,(640,480))
    start_time = time.time()
    while (int(time.time() - start_time) < duration):
        ret, frame = cap.read()
        if ret == True:
            # frame = cv2.flip(frame, 0)
            out.write(frame)
            # cv2.imshow('frame', frame)
        else:
            break
    cap.release()
    out.release()
    return fp


consecutive_frames = 75 # bird needs to be around for ~4 (75 frames) secs
bird_frame_counter = 0

Conf_threshold = 0.4
NMS_threshold = 0.4
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0),
          (255, 255, 0), (255, 0, 255), (0, 255, 255)]

class_name = []
with open('classes.txt', 'r') as f:
    class_name = [cname.strip() for cname in f.readlines()]
# print(class_name)
net = cv.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')
net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

model = cv.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

cap = cv.VideoCapture(0)
starting_time = time.time()
frame_counter = 0
while True:
    bird_in_frame = False
    ret, frame = cap.read()
    frame_counter += 1
    if ret == False:
        break
    classes, scores, boxes = model.detect(frame, Conf_threshold, NMS_threshold)
    for (classid, score, box) in zip(classes, scores, boxes):
        cls_name = class_name[classid[0]]
        if cls_name == 'bird':
            bird_in_frame = True
            color = COLORS[int(classid) % len(COLORS)]
            label = "%s : %f" % (cls_name, score)
            cv.rectangle(frame, box, color, 1)
            cv.putText(frame, label, (box[0], box[1]-10),
                       cv.FONT_HERSHEY_COMPLEX, 0.3, color, 1)
    endingTime = time.time() - starting_time
    fps = frame_counter/endingTime
    cv.putText(frame, f'FPS: {fps}', (20, 50),
               cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
    bird_frame_counter += 1 if bird_in_frame else 0
    if bird_frame_counter >= consecutive_frames:
        bird_frame_counter = 0
        cap.release()
        recording = make_recording(duration=10)
        if not send_file(recording):
            exit("Error - Video could not be send on telegram.")
        cap = cv.VideoCapture(0)
    cv.imshow('frame', frame)
    key = cv.waitKey(1)
    if key == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
