#!/usr/bin/env python3

import numpy as np
import sys

CONFIG_PEAK_THRESHOLD = 0.05
CONFIG_NOISE_THRESHOLD = 0.03

def detectFirstPeak(samples):
  for x in range(0,len(samples)):
    if abs(samples[x]) > CONFIG_PEAK_THRESHOLD:
      return x
  return 0 

def suppressLowNoise(samples):
  for x in range(0,len(samples)):
    if abs(samples[x]) < CONFIG_NOISE_THRESHOLD:
      samples[x] = 0
  return

def compressPeakInformation(samples):
  for x in range(0,len(samples)):
    if abs(samples[x]) > CONFIG_PEAK_THRESHOLD:
      samples[x] = max(abs(samples[x-250:x+250]))
      for y in range(-250,250):
        if y == 0:
          continue
        else:
          samples[x + y] = 0
