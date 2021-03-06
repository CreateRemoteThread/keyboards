#!/usr/bin/env python3

import matplotlib as mpl
# mpl.use("Agg")
import matplotlib.pyplot as plt
import scipy.io
from scipy.signal import butter,lfilter, freqz
import numpy as np
import sys
import support

def butter_lowpass(cutoff, fs, order=5):
  nyq = 0.5 * fs
  normal_cutoff = cutoff / nyq
  b, a = butter(order, normal_cutoff, btype='low', analog=False)
  return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
  b, a = butter_lowpass(cutoff, fs, order=order)
  y = lfilter(b, a, data)
  return y

def distBetweenPeaks(peakLocations):
  lastPeak = 0
  out = []
  for p in peakLocations:
    out.append(p - lastPeak)
    lastPeak = p
  print(out)
  return out

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("usage: ./plotlite.py <savegame>")
    sys.exit(0)
  plt.title("Plotlite")
  for f in sys.argv[1:]:
    samples = abs(np.load(f))
    approxPeaks = support.findpeaks(samples)
    realPeaks = support.getTruePeaks(approxPeaks,samples)
    rl = [y for (x,y) in realPeaks]
    # print("Starting suppressor engine")
    # support.autoSuppress(rl,samples)
    plt.plot(samples,'-gD',label=f,markevery=rl)
  plt.ylim(0,0.2)
  plt.legend()
  plt.show()

