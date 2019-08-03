from PIL import ImageDraw
import time
from job import Job

class Transition(Job):

    def __init__(self, disp, reset_first):
        self.reset_first = reset_first
        super().__init__(disp)


class HorizontalWipeTransition(Transition):

    def __init__(self, disp, reset_first, left_to_right=True):
        self.left_to_right = left_to_right
        super().__init__(disp, reset_first)

    def do(self):
        if self.reset_first:
            self.disp.reset(white=False)
            self.disp.send()
            time.sleep(0.5)
        for x in range(1, self.disp_width+1):
            draw = ImageDraw.Draw(self.disp.im)
            xy = (0, 0)
            sz = (x, self.disp_height)
            draw.rectangle([xy, sz], fill=(255, 255, 255))
            del draw
            self.disp.send()
            time.sleep(0.01)

class VerticalWipeTransition(Transition):

    def __init__(self, disp, reset_first, top_to_bottom=True):
        self.top_to_bottom = top_to_bottom
        super().__init__(disp, reset_first)

    def do(self):
        if self.reset_first:
            self.disp.reset(white=False)
            self.disp.send()
            time.sleep(0.5)
        for y in range(1, self.disp_height+1):
            draw = ImageDraw.Draw(self.disp.im)
            xy = (0, 0)
            sz = (28, y)
            draw.rectangle([xy, sz], fill=(255, 255, 255))
            del draw
            self.disp.send()
            time.sleep(0.1)


class CurtainTransition(Transition):

    def do(self):
        for x in range(1, w+1):
            draw = ImageDraw.Draw(self.disp.im)
            xy = (w-x, 0)
            sz = (x, h)
            draw.rectangle([(0, 0), (w, h)], fill=(255, 255, 255))
            draw.rectangle([xy, sz], fill=(0, 0, 0))
            del draw
            self.disp.send()
            time.sleep(0.1)
