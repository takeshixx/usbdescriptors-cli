usbdescriptors-cli
==================

A command line utility for uploading USB descriptors to usbdescriptors.com. Feel free to contribute! This script needs lsusb and the following Python packages (install them via pip):
* requests
* sh

### Usage
Run the script without any paramters to choose from a list of all attached USB devices:
```
$ ./usbdescriptors.py 
[0] Bus 004 Device 004: ID 08e6:34ec Gemalto (was Gemplus) Compact Smart Card Reader Writer
[1] Bus 004 Device 011: ID 046d:c069 Logitech, Inc. M500 Laser Mouse
[2] Bus 004 Device 002: ID 8087:0024 Intel Corp. Integrated Rate Matching Hub
[3] Bus 004 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
[4] Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
[5] Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
[6] Bus 003 Device 002: ID 8087:0024 Intel Corp. Integrated Rate Matching Hub
[7] Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Please enter an ID between 0 and 7: 
```
Try to submit each connected USB device:
```
$ ./usbdescriptors.py -all
```
Upload a device via it's vendor and device ID:
```
$ ./usbdescriptors.py -dev 148f:3070
```

### Help
```
$  ./usbdescriptors.py -h
usage: usbdescriptors.py [-h] [-dev DEV] [-all] [-c C] [-d]

Upload USB descriptors to http://usbdescriptors.com/.

optional arguments:
  -h, --help  show this help message and exit
  -dev DEV    Device, in format: vendor:device (optional)
  -all        Try submitting all connected devices (optional)
  -c C        Comment (optional)
  -d          Enable debugging output

```
