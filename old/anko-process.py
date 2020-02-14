#!/usr/bin/env python3

import support
import numpy as np
import sys
import uuid
import random
import getopt

CONFIG_BITESIZE = 350000

def usage():
  print("todo: usage")

CONFIG_WRITEFILE = None
CONFIG_INFILE = None
CONFIG_MODE = None

MODE_SLICE = 1
MODE_CONVERT = 2

def selectMode(ar):
  if ar == "slice":
    return MODE_SLICE
  elif ar == "convert":
    return MODE_CONVERT

if __name__ == "__main__":
  opts,remainder = getopt.getopt(sys.argv[1:],"hm:i:w:",["help","mode=","infile=","writefile="])
  for (opt, arg) in opts:
    if opt in ("-h","--help"):
      usage()
      sys.exit(0)
    elif opt in ("-w","--writefile"):
      CONFIG_WRITEFILE = arg
    elif opt in ("-i","--infile"):
      CONFIG_INFILE = arg
    elif opt in ("-m","--mode"):
      CONFIG_MODE = selectMode(arg)
  if CONFIG_MODE is None:
    print("You must select a mode with -m")
    sys.exit(0)
  elif CONFIG_MODE == MODE_SLICE:
    if CONFIG_INFILE is None or CONFIG_WRITEFILE is None:
      print("Slice requires both in and out files")
      sys.exit(0)
    data1 = np.load(CONFIG_INFILE)
    t = support.findpeaks_slice(data1)
    print(t)
    x = support.getTruePeaks(t,data1)
    print(x)
    (val,start) = x[0]
    data2 = data1[start-50:start+CONFIG_BITESIZE]
    print("Saving to %s" % CONFIG_WRITEFILE)
    np.save(CONFIG_WRITEFILE,data2)
  elif CONFIG_MODE == MODE_CONVERT:
    if CONFIG_INFILE is None or CONFIG_OUTFILE is None:
      print("Convert requires both in and out files")
      sys.exit(0)
    print("WIP")
    sys.exit(0)
