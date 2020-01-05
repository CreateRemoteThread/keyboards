#!/usr/bin/env python3

import matplotlib as mpl
# mpl.use("Agg")
import matplotlib.pyplot as plt
import scipy.io
from scipy.signal import butter,lfilter, freqz
import numpy as np
import sys
# import support

def butter_lowpass(cutoff, fs, order=5):
  nyq = 0.5 * fs
  normal_cutoff = cutoff / nyq
  b, a = butter(order, normal_cutoff, btype='low', analog=False)
  return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
  b, a = butter_lowpass(cutoff, fs, order=order)
  y = lfilter(b, a, data)
  return y

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("usage: ./plotlite.py <savegame>")
    sys.exit(0)
  plt.title("ANKO Plotlite")
  for f in sys.argv[1:]:
    plt.plot(np.load(f),label=f)
  plt.legend()
  plt.show()
  
