#!/usr/bin/env python3

import support
import numpy as np
import sys

if __name__ == "__main__":
  data1 = np.load(sys.argv[1])
  # print(support.findpeaks(data1))
  t = support.findpeaks_slice(data1)
  print(t)
  print(support.getTruePeaks(t,data1))
