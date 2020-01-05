#!/usr/bin/env python3

import support
import numpy as np
import sys
import uuid
import random

CONFIG_BITESIZE = 350000

if __name__ == "__main__":
  data1 = np.load(sys.argv[1])
  if len(sys.argv) == 3:
    print("Slicing...")
    data1 = data1[len(data1) // 2:]
  t = support.findpeaks_slice(data1)
  print(t)
  x = support.getTruePeaks(t,data1)
  print(x)
  (val,start) = x[0]
  data2 = data1[start-50:start+CONFIG_BITESIZE]
  np.save("blonk-%d" % random.randint(0,100),data2)
