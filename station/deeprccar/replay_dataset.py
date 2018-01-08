#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import cv2

import dataset as ds
from utils import get_mapped_steering_command
from utils import get_mapped_speed_command
from collections import deque

parser = argparse.ArgumentParser()
parser.add_argument("dataset_dir")
args = parser.parse_args()

dataset_file = args.dataset_dir + "/" + ds.DATASET_FILE
image_dir = args.dataset_dir + "/" + ds.IMAGE_FOLDER + "/"
with open(dataset_file, 'r') as csv:
    for line in csv.readlines():
        line = line.strip()
        (_, _, imagefile, steering_cmd, speed_cmd, steering_angle, speed) = line.split(";")
        steering_cmd = int(steering_cmd)
        speed_cmd = int(speed_cmd)

        steering_angle = int(float(steering_angle))
        speed = int(float(speed)*10)

        image = cv2.imread(image_dir + imagefile, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.resize(image, (480, 320), interpolation=cv2.INTER_CUBIC)
        # Count images
        cv2.putText(image, imagefile, (5, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

        cv2.putText(image, "Steering Command: {}".format(steering_cmd), (5, 315), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

        steering_cmd = get_mapped_steering_command(steering_cmd)

        #cv2.line(image, (240, 300), (240 - steering_cmd, 200), (0, 255, 0), 3)


        speed_cmd = get_mapped_speed_command(speed_cmd)
        print(steering_angle, speed)

        cv2.line(image, (50, 160), (50, 160 - speed_cmd), (0, 255, 0), 2)

        speed = 4
        if steering_angle < 0:
            cv2.ellipse(image, (240 - 3 * steering_angle, 300 + speed), (-3 * steering_angle, 100 + speed), 180, 0, 90 + speed, (0, 255, 0), 2)
        else:
            cv2.ellipse(image, (240 - 3 * steering_angle, 300 + speed), (3 * steering_angle, 100 + speed), 0, -90, 0 + speed, (0, 255, 0), 2)

        cv2.imshow('replay dataset', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        if (cv2.waitKey(0) & 0xFF) == ord('q'):  # Hit `q` to exit
            break
