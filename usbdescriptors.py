#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Script to upload USB descriptors to http://usbdescriptors.com/.
# Author: takeshix@adversec.com
import requests,argparse,sys
from os import getuid
from sh import lsusb

def info(msg):
    print '[+] {}'.format(msg)

def error(msg):
    print '[-] {}'.format(msg)

def debug(msg):
    if args.d: print '[*] {}'.format(msg)

def parse_cl():
    global args
    parser = argparse.ArgumentParser(description='Upload USB descriptors to http://usbdescriptors.com/.')
    parser.add_argument('-dev', help='Device, in format: vendor:device (optional)')
    parser.add_argument('-all', action='store_true', default=False, help='Try submitting all connected devices (optional)')
    parser.add_argument('-c', default='', help='Comment (optional)')
    parser.add_argument('-d', action='store_true', default=False, help='Enable debugging output')
    args = parser.parse_args()

def device_info(vendor,device):
    return lsusb('-v','-d','{}:{}'.format(vendor,device))

def choose_device():
    all_devices = lsusb().split('\n')
    count = 0 
    for dev in all_devices:
        if not dev: continue
        print '[{}] {}'.format(count,dev)
        count += 1
    try:
        choice = raw_input('Please enter an ID between 0 and {}: '.format(count-1))
        choice = int(choice)
    except:
        sys.exit(0)
    if not choice >= 1 and not choice <= count:
        error('Invalid choice: {}'.format(choice))
        sys.exit(0)
    vendor,device = all_devices[choice].split(' ')[5].split(':')
    return vendor,device

def upload(vendor,device,lsusb,comment):
    info('Uploading...')
    payload = {'vendor_entry':unicode(vendor),'device_entry':unicode(device),
            'comment_entry':unicode(comment).encode('utf8'),'descriptor_entry':unicode(lsusb).encode('utf8')}
    try:
        r = requests.post('http://usbdescriptors.com/cgi-bin/add',data=payload)
        if not r.status_code == requests.codes.ok:
            raise Exception
        if 'success' in r.text:
            return 1 
        elif 'device exists' in r.text:
            return 2
            sys.exit(0)
        else:
            raise Exception('Error: {}'.format(r.text))
    except Exception as e:
        debug(str(e))
        return False

if __name__ == '__main__':
    if not getuid() is 0:
        error('This script should be run as root for more comprehensive output!')
        sys.exit(0)
    parse_cl()
    usb_devices = []
    if args.all:
        for entry in lsusb().split('\n'):
            if not entry: continue
            usb_devices.append(entry.split(' ')[5].split(':'))
    elif not args.dev:
        usb_devices.append(choose_device())
    else:
        vendor,device = args.dev.split(':')
        try:
            int(vendor,16)
            int(device,16)
            if len(vendor) != 4 or len(device) != 4:
                raise ValueError
        except ValueError:
            error('Invalid vendor or device ID')
            sys.exit(0)
        usb_devices.append([vendor,device])

    success = 0
    for dev in usb_devices:
        if not dev: continue
        vendor,device = dev
        lsusb_dump = device_info(vendor,device)
        debug('Trying to submit vendor: {}, device: {}'.format(vendor,device))
        ret = upload(vendor,device,lsusb_dump,args.c)
        if not ret:
            error('Uploading vendor: {}, device: {} failed!'.format(vendor,device))
        elif ret is 1: 
            info('Successfully uploaded vendor: {}, device: {}'.format(vendor,device))
            success += 1
        elif ret is 2:
            error('Device already exists')
        
    info('Successfully submitted {} of {} descriptors'.format(success,len(usb_devices)))
