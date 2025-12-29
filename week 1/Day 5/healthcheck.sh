#!/bin/bash


mkdir -p logs

while true
do
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    status=$(curl -s -o /dev/null -w "%{http_code}" https://www.google.com)

    if [ "$status" != "200" ]; then
        echo "[$timestamp] FAILED with status $status" >> logs/health.log
    else
        echo "[$timestamp] OK" >> logs/health.log
    fi

    sleep 10
done
healthlog.sh