#!/usr/bin/env python3

from picoscope import ps2000a
import matplotlib as mpl
mpl.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import numpy as np
import sys
import support
import getopt
import time

mpl.use("Agg")
import matplotlib.pyplot as plt
CONFIG_SAMPLECOUNT = 400000
CONFIG_SAMPLERATE = 124999999
CONFIG_CAPTURES = 5

CONFIG_THRESHOLD = support.CONFIG_THRESHOLD
CONFIG_BACKOFF = 0.2
CONFIG_VRANGE = 0.5

CONFIG_FPREFIX = None

def confirmSettings():
  print("Number of captures: %d" % CONFIG_CAPTURES)
  print("Sample rate: %d" % CONFIG_SAMPLERATE)
  print("Sample count: %d" % CONFIG_SAMPLECOUNT)
  print("Trigger level: %f" % CONFIG_THRESHOLD)
  print("Analog range: %f" % CONFIG_VRANGE)
  if CONFIG_THRESHOLD > CONFIG_VRANGE:
    print("Trigger cannot exceed analog range. Bye!")
    sys.exit(0)
  if CONFIG_FPREFIX:
    print("Capturing data for: %s" % CONFIG_FPREFIX)
  x = input("Are these settings correct? [y/n] ")
  if x.rstrip() not in ("y","Y"):
    print("Capture action cancelled. Bye!")
    sys.exit(0)

class Application(tk.Frame):
  def __init__(self,master=None):
    super().__init__(master)
    self.master=master
    self.f = Figure(figsize=(8,6),dpi=100)
    self.mainPlot = self.f.add_subplot(111)
    self.canvas=FigureCanvasTkAgg(self.f,self.master)
    self.cid = self.canvas.mpl_connect("button_press_event",self.canvasClick)
    self.canvas.draw()
    self.canvas_tk = self.canvas.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)

  def canvasClick(self,event):
    global CONFIG_VRANGE,CONFIG_SAMPLERATE,CONFIG_SAMPLECOUNT,CONFIG_FPREFIX,CONFIG_THRESHOLD,CONFIG_CAPTURES,CONFIG_BACKOFF
    try:
      ps = ps2000a.PS2000a()
      self.canvas.mpl_disconnect(self.cid)
      print("Committing capture...")
    except:
      print("Failed to commit scope")
      return
    ps.setChannel('A','DC',VRange=CONFIG_VRANGE,VOffset=0.0,enabled=True,BWLimited=False,probeAttenuation=10.0)
    (freq,maxSamples) = ps.setSamplingFrequency(CONFIG_SAMPLERATE,CONFIG_SAMPLECOUNT)
    print(" > Asked for %d Hz, got %d Hz" % (CONFIG_SAMPLERATE, freq))
    if CONFIG_FPREFIX is not None:
      print(" > Configured in training mode with prefix %s" % CONFIG_FPREFIX)
    ps.setSimpleTrigger('A',CONFIG_THRESHOLD,'Rising',enabled=True)
    i = 0
    nCount = 0
    nMax = CONFIG_CAPTURES
    print("Capture is committed...")
    while (nMax is None) or (nCount < nMax):
      ps.runBlock()
      ps.waitReady()
      dataA = ps.getDataV("A",CONFIG_SAMPLECOUNT,returnOverflow=False)
      if float(max(dataA[0:100])) < float(CONFIG_THRESHOLD):
        # print("failed capture")
        continue
      if CONFIG_FPREFIX is None:
        print("Saving training capture...")
        np.save("floss/%d.npy" % nCount,dataA)
      else:
        print("Saving real capture...")
        np.save("toothpicks/%s-%d.npy" % (CONFIG_FPREFIX,nCount),dataA)
      self.mainPlot.clear()
      self.mainPlot.plot(dataA[:75000])
      self.canvas.draw()
      self.canvas.flush_events()
      time.sleep(CONFIG_BACKOFF)
      nCount += 1
    print("Captured %d slices" % nCount)

if __name__ == "__main__":
  if len(sys.argv) > 1:
    args,opts = getopt.getopt(sys.argv[1:],"t:",["train="])
    for arg,opt in args:
      if arg in ("-t","--train"):
        CONFIG_FPREFIX = opt
  root = tk.Tk()
  root.title("sycamore.py")
  root.geometry("800x600")
  app = Application(master=root)
  app.mainloop()

