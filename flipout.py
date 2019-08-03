#! /usr/bin/env python

import sys
import time
import threading
import math
import datetime
import random
import draw
import curses
from PIL import Image, ImageDraw, ImageFont, ImageOps
import text
import transitions
import utils
import serial.tools.list_ports
import os
sys.path.append("..") # Adds higher directory to python modules path.
sys.path.append("../dcreemer/flipdot") # Adds higher directory to python modules path.
from dcreemer.flipdot import client, display
from dcreemer.demo import animations
from dcreemer.flipdot.sim import DisplaySim

import poetry
import clock
import animation
import rain

d = display.Display(84, 14,
                    panels={
                         0: ((0, 0), (28, 7)),
                         1: ((0, 7), (28, 7)),
                         2: ((28, 0), (28, 7)),
                         3: ((28, 7), (28, 7)),
                         4: ((56, 0), (28, 7)),
                         5: ((56, 7), (28, 7)),
                    })

def run_job(job):
    print("Running job",job,"...")
    job.do()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "sim-client":
        d.connect(client.UDPClient("localhost", 9999))
    elif len(sys.argv) > 1 and sys.argv[1] == "sim-server":
        exec(open("simulator.py").read());
    elif len(sys.argv) > 1:
        d.connect(client.SerialClient(sys.argv[1]))
    else:
        print("Not connecting...listing available ports:")
        print(list(serial.tools.list_ports.comports()))
        os._exit(1)
    try:
        d.reset()
        noise = animation.Noise()
        rain = rain.Rain()
        invader = animation.HorizontalImageAnimation(["renderables/animationframes/invader1-1.png", "renderables/animationframes/invader1-2.png"], True, 10, 5)
        ninja = animation.HorizontalImageAnimation(["renderables/animationframes/ninja-1.png",
                                                   "renderables/animationframes/ninja-2.png",
                                                   "renderables/animationframes/ninja-3.png",
                                                   "renderables/animationframes/ninja-4.png",
                                                   "renderables/animationframes/ninja-5.png"],
                                                   True, 10, 10)
        #job = animation.AnimatorJob(d, ninja)
        #job = animation.AnimatorJob(d, invader)
        #job = animation.AnimatorJob(d, noise)
        job = animation.AnimatorJob(d, rain)
        #job = clock.ClockJob(d)
        #job = poetry.PoemsJob(d)
        while True:
            run_job(job)
    finally:
        d.disconnect()
