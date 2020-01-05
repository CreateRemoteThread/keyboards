#!/usr/bin/env python3

import sys
import numpy as np

CONFIG_PEAKT = 0.075
CONFIG_SLICEWIDTH = 9
CONFIG_SLICETHRESH = 50000
CONFIG_SLICETEMPL = [False, True, False, False, False, False, False, False]

def getTruePeaks(locations,samples):
  out = []
  for x in locations:
    temp_array = samples[x-50:x+50]
    out.append( (max(temp_array),x + int(np.where(temp_array == max(temp_array))[0]) ) )
  print(out)
  return out

def matchSlice(lengths):
  e = [lengths[i+1] - lengths[i] for i in range(0,len(lengths) - 1)]
  ex = [i > CONFIG_SLICETHRESH for i in e]
  if ex == CONFIG_SLICETEMPL:
    return None
  else:
    print(ex)
    return ex

def findpeaks_slice(samples):
  n = []
  dists = []
  const_slen = len(samples)
  out = []
  i = 0
  while i < const_slen:
    if samples[i] > CONFIG_PEAKT:
      if len(n) != CONFIG_SLICEWIDTH:
        n.append(i)
      else:
        n.pop(0)
        n.append(i)
      if len(n) == CONFIG_SLICEWIDTH:
        x = matchSlice(n)
        if x is None:
          print("OK")
          return n
        else:
          print("Pushing")
          n.pop(0)
          x.pop(0)
          while x[1] is not True and len(x) >= 3:
            print("++Pushing")
            n.pop(0)
            x.pop(0)
      i += 10000
    i += 1
  print("End reached")
  return out

def findpeaks(samples):
  const_n = len(samples)
  i = 0
  out = []
  while i < const_n:
    if samples[i] > CONFIG_PEAKT:
      out.append(i)
      i += 1000
    i += 1
  return out
