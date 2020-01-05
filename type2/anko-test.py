#!/usr/bin/env python3

CONFIG_VRANGE = 0.5
CONFIG_SAMPLERATE = 24999999
CONFIG_SAMPLECOUNT = 5000000

from picoscope import ps2000a
import uuid
import numpy as np

if __name__ == "__main__":
  ps = ps2000a.PS2000a()
  ps.setChannel('A','DC',VRange=CONFIG_VRANGE,VOffset=0.0,enabled=True,BWLimited=False,probeAttenuation=10.0)
  (freq,maxSamples) = ps.setSamplingFrequency(CONFIG_SAMPLERATE,CONFIG_SAMPLECOUNT)
  print(" > Asked for %d Hz, got %d Hz" % (CONFIG_SAMPLERATE, freq))
  ps.runBlock()
  ps.waitReady()
  dataA = ps.getDataV('A',CONFIG_SAMPLECOUNT,returnOverflow=False)
  np.save("/tmp/blink-%s.npy" % uuid.uuid4(),dataA)
