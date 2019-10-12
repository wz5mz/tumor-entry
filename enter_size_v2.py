#! /data/data/com.termux/files/usr/bin/env python3

from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import sys
import re

filename = sys.argv[1]
sheetname = sys.argv[2]
mouseno = re.search('\d+', sys.argv[3]).group(0)
width = float(re.search('(\d*\.\d+|\d+)', sys.argv[4]).group(0))
length = float(re.search('(\d*\.\d+|\d+)', sys.argv[5]).group(0))
date = re.search('\d\d\d\d-[0-1]\d-[0-3]\d', sys.argv[6]).group(0)

print(filename, sheetname, mouseno, width, length, date)
