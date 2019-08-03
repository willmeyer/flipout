from job import Job
from PIL import ImageDraw
import datetime, time

class ClockJob(Job):

    def __init__(self, disp):
        super().__init__(disp)

    def draw_clock_tickline(self, draw, top_y, num_graduations, val_percent, width, height):
        for x in range(0, width):

            # baseline
            #if x % 3 == 0:
            draw.point((x,top_y), (255,255,255))

            # major tick marks
            tick_every = int(width / num_graduations)
            if x % tick_every == 0:
                print("printing tick at x=", x)
                #draw.rectangle([(x,top_y), (x, top_y+1)], (255, 255, 255))

        # value
        x = val_percent * 0.01 * width
        #draw.rectangle([(x,top_y), (x+1, top_y+height-1)], (255, 255, 255))
        draw.polygon([(x-3,top_y+height-1), (x+3, top_y+height-1), (x,top_y)], (255, 255, 255))
        #draw.ellipse([(x-2,top_y-1), (x+2, top_y+height-1)], (255, 255, 255))

    def clock_tick(self, now, previous):
        draw = ImageDraw.Draw(self.disp.im)
        self.disp.reset()
        disp_width, disp_height = self.disp.im.size

        # If this is the first animation in a new minute, do an effect and reset.
        # otherwise just start the update
        now = datetime.datetime.now()
        if (now.minute != previous.minute):
            for i in range(0,2):
                draw.rectangle([(0,0),(disp_width, disp_height)], (255,255,255))
                self.disp.send()
                time.sleep(0.5)
                draw.rectangle([(0,0),(disp_width, disp_height)], (0,0,0))
                self.disp.send()
        now = datetime.datetime.now()

        row_height = int(disp_height / 3)
        top = disp_height % row_height / 2
        print("row height, display height", row_height, disp_height)

        self.draw_clock_tickline(draw, top, 24, now.hour / 24 * 100, disp_width, row_height)
        self.draw_clock_tickline(draw, top+row_height, 4, now.minute / 60 * 100, disp_width, row_height)
        self.draw_clock_tickline(draw, top+(row_height * 2), 12, now.second / 60 * 100, disp_width, row_height)

        del draw
        self.disp.send()

        # Continue
        previous=now

    def do(self):
        previous = datetime.datetime.now()
        while not self.exit_asap:
            current = datetime.datetime.now()
            self.clock_tick(current, previous)
            previous=current
            time.sleep(0.5)
