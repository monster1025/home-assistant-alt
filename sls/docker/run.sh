#!/bin/bash

while [ 1 ]
do
  python3 backup.py -i=$SLS_IP
  sleep 1d
done
