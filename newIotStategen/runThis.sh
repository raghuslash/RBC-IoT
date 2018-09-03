#!/bin/bash

sh /home/richard/Desktop/newIoT/tools/streaming/get.sh 10

python3 /home/richard/Desktop/newIoT/streaming/RF/stateGen.py /home/richard/Desktop/newIoT/tools/streaming/data/out.csv

echo "Completed RF state generation.."


