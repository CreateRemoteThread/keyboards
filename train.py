#!/usr/bin/env python3

import sys
import glob
import support
import numpy as np

def createLabel(filename,offset):
  label = filename.split("/")[1]
  label = label.split("-")[0]
  return "%s-%d" % (label,offset)

traintracks = []
for fn in glob.glob("toothpicks/*"):
  print("Training on %s" % fn)
  data = np.load(fn)
  lm = support.findLocalMaxima(data)
  for nom in lm:
    rlm_channelA = support.findReallyLocalMaxima(support.block_preprocess_function(data[nom+1000:nom+support.CONFIG_MAX_PULSEWIDTH]))
    traintracks.append( (createLabel(fn,nom),rlm_channelA) )

print("Toothpicks sorted, saving to trainset.npy")
np.save("trainset.npy",np.array(traintracks,dtype=np.object))

