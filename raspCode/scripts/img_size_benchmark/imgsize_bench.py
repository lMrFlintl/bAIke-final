import cv2
import json
from statistics import mean
import time
import os

from tqdm import tqdm
import numpy as np
from yolov4.tf import YOLOv4

base_path = "../"

def impactDetection(frame, yolo):


        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame = cv2.resize(frame,  yolo.input_size, interpolation = cv2.INTER_AREA)
        boxes = yolo.predict(frame)
        
        return boxes

def get_yolo(img_size):
    
    yolo = YOLOv4()
    yolo.classes = base_path + "coco.names"
    yolo.input_size = img_size
    yolo.make_model()
    yolo.load_weights(base_path + "yolov4.weights", weights_type="yolo")

    return yolo

def updateDict(pred_dict, results):
    for _, _, _, _, label, pct in results:
        label = int(label)
        pred_dict[label]["count"] =  pred_dict[label]["count"] + 1
        tmp_list = pred_dict[label]["pct_list"]
        tmp_list.append(round(pct, 4))
        pred_dict[label]["pct_list"] = tmp_list
        pred_dict[label]["mean"] = mean(tmp_list)
        del tmp_list  
    return  pred_dict  


def main():
    b_dict = dict()

    for pct in tqdm(range(100, 0, -20)):
        x = int(640*pct/100)
        y = int(480*pct/100)

        if x % 32 != 0 or y % 32 != 0:
            continue

        yolo = get_yolo((x, y))
        coco_dict = {x:{"name":yolo.classes.get(x),"count":0, "mean":0, "pct_list":[]} for x in range(0,80)}
        predict_times=[]
        boxes_found=0
        cap = cv2.VideoCapture(base_path + "joinedVideo.mp4")

        while True:
            ret, frame = cap.read()


            if ret:
                time_init = time.time()
                result = impactDetection(frame, yolo)
                predict_times.append(round(time.time() - time_init, 4))

                if sum([sum(x) for x in result]):
                    boxes_found += len(result)
                    coco_dict=updateDict(coco_dict, result)

            else:
                break

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


            b_dict.update({pct:{
                    "coco.names": coco_dict, "boxes_found": boxes_found, \
                    "mean_predict_times": mean(predict_times), \
                    "predict_times": predict_times
                    }
                })
        
       
        cap.release()

    with open(base_path + "yolo_data.json", "w") as f:
        json.dump(b_dict, f)


if __name__ == "__main__":
    main()
