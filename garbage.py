#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 12:18:43 2022

@author: omega
"""
# imports
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime, timedelta, time
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from collections import namedtuple
import os
import pytz
import time
import re
import requests
import yaml
 
# init the calendar
cal = Calendar()

Display_Size_x=296
Display_Size_y=128
config = yaml.safe_load(open("config.yml"))
destination_file = config['output']['filename']

def generate_abhol_image(summary, datum):
    muster=Image.new("RGB",(296,128),color=(255,255,255))
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%d.%m.%Y, %H:%M:%S", named_tuple)
    im = ImageDraw.Draw(muster)
    font = ImageFont.load('fonts/VeraMono30.pil')
    font_klein = ImageFont.load('fonts/VeraMono8.pil')
    

    _, _, w, h = im.textbbox((0, 0), summary, font=font)
    im.text((((Display_Size_x/2)-w/2),Display_Size_y/2-h/2-30), summary ,fill=(0, 0, 0),font=font)
    
    _, _, w, h = im.textbbox((0, 0), datum, font=font_klein)
    im.text((((Display_Size_x/2)-w/2),80), datum ,fill=(0, 0, 0),font=font_klein)
    
    _, _, w, h = im.textbbox((0, 0), time_string, font=font_klein)
    im.text((((Display_Size_x/2)-w/2),100), time_string ,fill=(0, 0, 0),font=font_klein)
    
    # muster=muster.rotate(angle=90,expand="true")
    if (destination_file.upper().endswith('.JPG')):
        muster.save(destination_file, 'JPEG', quality="maximum")
    else:
        muster.save(destination_file)


def generate_empty_image():
    muster=Image.new("RGB",(296,128),color=(255,255,255))
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%d.%m.%Y, %H:%M:%S", named_tuple)
    im = ImageDraw.Draw(muster)
    font_klein = ImageFont.load('fonts/VeraMono8.pil')
    
    _, _, w, h = im.textbbox((0, 0), time_string, font=font_klein)
    im.text((((Display_Size_x/2)-w/2),100), time_string ,fill=(0, 0, 0),font=font_klein)
    
    # muster=muster.rotate(angle=90,expand="true")
    if (destination_file.upper().endswith('.JPG')):
        muster.save(destination_file, 'JPEG', quality="maximum")
    else:
        muster.save(destination_file)

#
# push image to OpenEPaperLink AP
#
def pushImage(image_path, cfg_oepl):
  # Prepare the HTTP POST request
  url = "http://" + cfg_oepl['apip'] + "/imgupload"
  payload = {"dither": 0, "mac": cfg_oepl['mac']}  # Additional POST parameter
  files = {"file": open(image_path, "rb")}  # File to be uploaded

  # Send the HTTP POST request
  response = requests.post(url, data=payload, files=files)

  # Check the response status
  if response.status_code == 200:
    print("Image uploaded successfully!")
  else:
    print("Failed to upload the image.")



generate_empty_image()
today = datetime.today().date()
e = open('abfuhrtermine.ics', 'rb')
ecal = cal.from_ical(e.read())
for component in ecal.walk():
    #print(component.name)
    if component.name == "VEVENT":
        summary = component.get('summary')
        shortsummary = re.search(r'^[a-zA-Z]+|$', summary).group()
        #print ('VEVENT: ', shortsummary)
        #print ('VEVENT: ', component.get('dtstart').dt)
        abfuhrtag = component.get('dtstart').dt
        nachrichttag = abfuhrtag - timedelta(days=1)
        nachrichttag = abfuhrtag - timedelta(days=1)
        #print(today, nachrichttag)
        if(today==nachrichttag or today==abfuhrtag):
            summary = component.get('summary')
            shortsummary = re.search(r'^[a-zA-Z]+|$', summary).group()
            #print ('TODAY: ', component.get('summary'))
            #print ('TODAY: ', component.get('dtstart').dt)
            datetext = "HEUTE" if today==abfuhrtag else component.get('dtstart').dt
            generate_abhol_image(str(shortsummary), str(datetext))
        
        
e.close()
if ('openepaperlink' in config):
    pushImage(destination_file, config['openepaperlink'])
