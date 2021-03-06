from collections import defaultdict
from concurrent.futures.thread import ThreadPoolExecutor
from itertools import repeat
from queue import Queue
from threading import Thread

import cv2
import matplotlib.pyplot as plt

from buffers import Buffer
from chopper import chop
from classifier import classify
from executor import process_and_upload
from Database import DataBase

plt.rcParams["figure.figsize"] = [10, 6]

plt.ion()

fig, ax = plt.subplots()



def show_images(imgs):
    for i, img in enumerate(imgs):
        cv2.imshow('img{}'.format(i), img)


buffer = Buffer()
frame = None
cap = cv2.VideoCapture("../Speaking_Shreyan.mp4")

retvals = Queue()


def process_frame():
    imgs = chop(frame)
    buffer.reset_people()
    with ThreadPoolExecutor() as master:
        master.map(process_and_upload, imgs, repeat(buffer))
    classes, attentions = classify(buffer)
    # RITIK IDHAR SE UTHA
    dbt = Thread(target=db.insert_data,args=(classes, attentions))
    dbt.start()
    retvals.put((classes, attentions))
    buffer.set_pressences()


processingThread = Thread(target=process_frame)
NAMES = ["Ritesh Sethi", "Ayush Apoorva", "Nitin GL", "Vivek Chopra", "Shallen@GL", "Shreyan Datta Chakrabort"]
db = DataBase()
attentions = defaultdict(lambda: [])
while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    if not processingThread.is_alive():
        ax.cla()
        while not retvals.empty():
            classes, scores = retvals.get()
            for key in scores:
                attentions[key].append(scores[key])
        
        processingThread = Thread(target=process_frame)
        processingThread.start()
