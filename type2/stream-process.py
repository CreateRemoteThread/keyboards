#!/usr/bin/env python3

import support2
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl

for f in sys.argv[1:]:
  try:
    samples = np.load(f)
  except:
    print("Bye!")
    sys.exit(0)
  s = samples[300000:]
  loc = support2.detectFirstPeak(s)
  sl = s[loc - 500:loc + 275000]
  support2.suppressLowNoise(sl)
  # support2.compressPeakInformation(sl)
  plt.plot(sl,"-D",label=f)

plt.legend()
plt.show()
