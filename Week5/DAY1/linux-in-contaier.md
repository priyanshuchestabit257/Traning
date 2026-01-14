# Day 1: Docker Fundamentals & Linux Internals

## 1. Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 4000

CMD ["node", "index.js"]

## 2. Exploration Results
I entered the container using `docker exec -it mycontainer /bin/sh`.

### A. Processes (`ps`)
* **Observation:** The Node application is running as PID 1.
* **Output:**
  # ps
    PID TTY          TIME CMD
     20 pts/0    00:00:00 sh
     26 pts/0    00:00:00 ps

### B. File System (`ls -F`)
* **Observation:** The code is correctly located in the `/app` directory.
* **Output:**
  # ls -F
    dockerfile  index.js  node_modules/  package-lock.json  package.json

### C. Resource Usage (`top`)
* **Observation:** 
     top
    top - 14:01:43 up  8:29,  0 user,  load average: 0.67, 0.73, 0.71
    Tasks:   3 total,   1 running,   2 sleeping,   0 stopped,   0 zombie
    %Cpu(s):  4.6 us,  1.5 sy,  0.0 ni, 93.7 id,  0.0 wa,  0.0 hi,  0.1 si,  0.0 st 
    MiB Mem :  23717.8 total,   5942.8 free,   6273.3 used,  12495.1 buff/cache     
    MiB Swap:   8192.0 total,   8192.0 free,      0.0 used.  17444.5 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND                                           
      1 root      20   0 1407664  63212  46744 S   0.0   0.3   0:00.25 MainThread                                        
     20 root      20   0    2584   1788   1676 S   0.0   0.0   0:00.04 sh                                                
     28 root      20   0    8632   4936   2852 R   0.0   0.0   0:00.00 top                                               




### D. Disk Usage (`df -h`)
* **Observation:** Checked the overlay filesystem size.
* **Output:**
  
# df -h
    Filesystem      Size  Used Avail Use% Mounted on
    overlay         468G   47G  398G  11% /
    tmpfs            64M     0   64M   0% /dev
    shm              64M     0   64M   0% /dev/shm
    /dev/nvme0n1p2  468G   47G  398G  11% /etc/hosts
    tmpfs            12G     0   12G   0% /proc/acpi
    tmpfs            12G     0   12G   0% /proc/asound
    tmpfs            12G     0   12G   0% /proc/scsi
    tmpfs            12G     0   12G   0% /sys/devices/virtual/powercap
    tmpfs            12G     0   12G   0% /sys/firmware
    tmpfs            12G     0   12G   0% /sys/devices/system/cpu/cpu0/thermal_throttle
    tmpfs            12G     0   12G   0% /sys/devices/system/cpu/cpu1/thermal_throttle
    tmpfs            12G     0   12G   0% /sys/devices/system/cpu/cpu2/thermal_throttle
    tmpfs            12G     0   12G   0% /sys/devices/system/cpu/cpu3/thermal_throttle
    tmpfs            12G     0   12G   0% /sys/devices/system/cpu/cpu4/thermal_throttle
    tmpfs            12G     0   12G   0% /sys/devices/system/cpu/cpu5/thermal_throttle
    tmpfs            12G     0   12G   0% /sys/devices/system/cpu/cpu6/thermal_throttle
    tmpfs            12G     0   12G   0% /sys/devices/system/cpu/cpu7/thermal_throttle
    tmpfs            12G     0   12G   0% /sys/devices/system/cpu/cpu8/thermal_throttle
    tmpfs            12G     0   12G   0% /sys/devices/system/cpu/cpu9/thermal_throttle
    tmpfs            12G     0   12G   0% /sys/devices/system/cpu/cpu10/thermal_throttle
    tmpfs            12G     0   12G   0% /sys/devices/system/cpu/cpu11/thermal_throttle