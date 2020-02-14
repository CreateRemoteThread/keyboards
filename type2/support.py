#!/usr/bin/env python3

import sys
import numpy as np

CONFIG_PEAKT = 0.06
CONFIG_PEAK_ISOLATION = 5000
CONFIG_PEAK_SEARCHDIST = 2000
# slicing for block synchronisation
CONFIG_SLICEWIDTH = 9
CONFIG_SLICETHRESH = 50000
CONFIG_SLICETEMPL = [False, True, False, False, False, False, False, False]

CONFIG_SUPPRESSOR_SLICETHRESH = 20000
CONFIG_SUPPRESSOR_SLICEDIST = 3000

def getRegularPeaks(firstPeak,samples):
  out = []
  i = firstPeak
  while i < len(samples):
    if i + CONFIG_SUPPRESSOR_SLICETHRESH >  len(samples):
      break
    maxVal = max(samples[i - CONFIG_SUPPRESSOR_SLICEDIST:i + CONFIG_SUPPRESSOR_SLICEDIST])
    maxIndex = np.where(samples[i - CONFIG_SUPPRESSOR_SLICEDIST:i+CONFIG_SUPPRESSOR_SLICEDIST] == maxVal)[0][0] + i - CONFIG_SUPPRESSOR_SLICEDIST
    if type(maxIndex) != np.int64:
      print(maxIndex)
    out.append( (maxIndex,maxVal) )
    i = maxIndex + CONFIG_SUPPRESSOR_SLICETHRESH
    print("Advancing read head: %d" % i)
  print("Done")
  locs = [loc for (loc,val) in out]
  dists = [locs[i+1] - locs[i] for i in range(0,len(locs) - 1)]
  # print(dists)
  vals = [val for (loc,val) in out]
  f2 = np.average(dists)
  f1 = np.mean(vals)
  # print("Average Distance: %f" % f2)
  # print("Maximum Horizontal Variance: %f" % max([abs(dist - f2) for dist in dists]))
  # print("Maximum Vertical Variance: %f" % max([abs(val - f1) for val in vals]))
  # print("Minimum Value: %f" % min(vals))
  # print("Minimum Value: %f" % max(vals))
  return (max([abs(val - f1) for val in vals]),max([abs(dist - f2) for dist in dists]),out)

# maximum vertical delta and maximum horizontal delta must flal within thresholds, otherwise, we've detected a false peak
CONFIG_SUPPRESSOR_VERTSANITY = 0.02
CONFIG_SUPPRESSOR_HORSANITY = 2000
CONFIG_PEAK_SUPPRESS = 500

def autoSuppress(peaks,samples):
  if len(peaks) < 5:
    print("Not enough peaks detected for automatic suppress")
    sys.exit(0)
  TRIPWIRE_SANITY = False
  dists = [peaks[i+1] - peaks[i] for i in range(0,len(peaks)-1)]
  for i in peaks[0:5]:
    (maxVertical,maxHorizontal,rp) = getRegularPeaks(i,samples)
    print("Marker %d, Max Vertical %f, Max Horizontal %f" % (i,maxVertical,maxHorizontal))
    if maxVertical < CONFIG_SUPPRESSOR_VERTSANITY and maxHorizontal < CONFIG_SUPPRESSOR_HORSANITY:
      print("Pulse synchronisation successful, setting TRIPWIRE_SANITY")
      TRIPWIRE_SANITY = True
      break
    # print(rp[0])
    for x in range(rp[0][0] - CONFIG_PEAK_SUPPRESS,rp[0][0] + CONFIG_PEAK_SUPPRESS):
      samples[x] = 0
  if TRIPWIRE_SANITY is False:
    print("autoSuppress(): Loop unbroken, could not detect true peaks")
    sys.exit(0)
  lastPeak = 0
  for (peak,peakval) in rp:
    lastPeak = peak
    for x in range(peak - CONFIG_PEAK_SUPPRESS,peak + CONFIG_PEAK_SUPPRESS):
      samples[x] = 0
  print("Cutting tail, taking lazy way out")
  for x in range(lastPeak,len(samples)):
    samples[x] = 0

def getTruePeaks(locations,samples):
  out = []
  newPeakOffset = 0
  for x in locations:
    if x - CONFIG_PEAK_SEARCHDIST <= 0:
      temp_array = samples[:x+CONFIG_PEAK_SEARCHDIST]
      newPeakOffset = 0
    elif x + CONFIG_PEAK_SEARCHDIST >= len(samples):
      temp_array = samples[x-CONFIG_PEAK_SEARCHDIST:]
      newPeakOffset = x - CONFIG_PEAK_SEARCHDIST
    else:
      temp_array = samples[x-CONFIG_PEAK_SEARCHDIST:x + CONFIG_PEAK_SEARCHDIST]
      newPeakOffset = x - CONFIG_PEAK_SEARCHDIST
    f = np.where(temp_array == max(temp_array))[0][0]
    out.append( (max(temp_array),newPeakOffset + f ) )
  return out


def suppressPeaks(locations,samples):
  for x in locations:
    if x - CONFIG_PEAK_SUPPRESS <= 0:
      for i in range(0,x + CONFIG_PEAK_SUPPRESS):
        samples[i] = 0
    elif x + CONFIG_PEAK_SUPPRESS >= len(samples):
      for i in range(x - CONFIG_PEAK_SUPPRESS,len(samples)):
        samples[i] = 0
    else:
      for i in range(x - CONFIG_PEAK_SUPPRESS,x+CONFIG_PEAK_SUPPRESS):
        samples[i] = 0

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
      i += CONFIG_PEAK_ISOLATION
    i += 1
  print(out)
  return out
