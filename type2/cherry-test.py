#!/usr/bin/env python3

CONFIG_VRANGE = 0.5 # 50 mV
CONFIG_SAMPLERATE = 249999999 # 125 MSPS
CONFIG_SAMPLECOUNT = 1000000

from picoscope import ps2000a
import uuid
import numpy as np
import sys

if __name__ == "__main__":
  ps = ps2000a.PS2000a()
  ps.setChannel('A','DC',VRange=CONFIG_VRANGE,VOffset=0.0,enabled=True,BWLimited=False,probeAttenuation=10.0)
  (freq,maxSamples) = ps.setSamplingFrequency(CONFIG_SAMPLERATE,CONFIG_SAMPLECOUNT)
  print(" > Asked for %d Hz, got %d Hz" % (CONFIG_SAMPLERATE, freq))
  for i in range(0,5):
    ps.runBlock()
    ps.waitReady()
    dataA = ps.getDataV('A',CONFIG_SAMPLECOUNT,returnOverflow=False)
    print("Saving to /tmp/blink-%s%d.npy" % (sys.argv[1],i))
    np.save("/tmp/blink-%s%d.npy" % (sys.argv[1],i),dataA)
