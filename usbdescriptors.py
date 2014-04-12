#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Script to upload USB descriptors to http://usbdescriptors.com/.
# Author: takeshix@adversec.com
import requests,argparse,sys
from os import getuid
from sh import lsusb

parser = argparse.ArgumentParser(description='Upload USB descriptors to http://usbdescriptors.com/.')
parser.add_argument('-dev', help='Device, in format: vendor:device (optional)')
parser.add_argument('-c', default='', help='Comment (optional)')
parser.add_argument('-d', action='store_true', default=False, help='Enable debugging output')
args = parser.parse_args()

def info(msg):
    print '[+] {}'.format(msg)

def error(msg):
    print '[-] {}'.format(msg)

def debug(msg):
    if args.d: print '[*] {}'.format(msg)

def device_info(vendor,device):
    return lsusb('-v','-d','{}:{}'.format(vendor,device))

def choose_device():
    all_devices = lsusb().split('\n')
    count = 0 
    for dev in all_devices:
        if not dev: continue
        print '[{}] {}'.format(count,dev)
        count += 1
    choice = raw_input('Please enter an ID between 0 and {}: '.format(count-1))
    choice = int(choice)
    if not choice >= 1 and not choice <= count:
        error('Invalid choice: {}'.format(choice))
        sys.exit(0)
    vendor,device = all_devices[choice].split(' ')[5].split(':')
    return vendor,device

def upload(vendor,device,lsusb,comment):
    info('Uploading...')
    payload = {'vendor_entry':unicode(vendor),'device_entry':unicode(device),'comment_entry':unicode(comment).encode('utf8'),'descriptor_entry':unicode(lsusb).encode('utf8')}
    try:
        r = requests.post('http://usbdescriptors.com/cgi-bin/add',data=payload)
        if not r.status_code == requests.codes.ok:
            raise Exception
        if 'text success' in r.text:
            return True
        elif 'device exists' in r.text:
            info('Device already exists')
            sys.exit(0)
        elif 'missing' in r.text:
            raise Exception('Something is missing: {}'.format(r.text))
        elif 'doesnt match' in r.text:
            raise Exception('Input format is wrong: {}'.format(r.text))
        elif 'cant write to database' in r.text:
            raise Exception('Encoding error: {}'.format(r.text))
        return True
    except Exception as e:
        debug(str(e))
        return False

if __name__ == '__main__':
    if not getuid() == 0:
        error('This script should be run as root for more comprehensive output!')
        sys.exit(0)
    if not args.dev:
        vendor,device = choose_device()
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

    lsusb_dump = device_info(vendor,device)
    if not upload(vendor,device,lsusb_dump,args.c):
        error('An error occured during upload. Please try again in a few minutes.')
        sys.exit(0)
    else:
        info('Successfully uploaded USB descriptor. Thanks for your contribution!')
