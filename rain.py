from animation import Animation
import random, time
import datetime
from PIL import ImageDraw

SNOWFLAKE_MIN_COUNT=100
SNOWFLAKE_YSPEED_MIN=2.0
SNOWFLAKE_YSPEED_MAX=15.0
SNOWFLAKE_XSPEED_MIN=0.0
SNOWFLAKE_XSPEED_MAX=0.5

class Drop:

    def __init__(self, x_max):
        self.x = random.randrange(0, int(x_max))
        self.y = random.randrange(-5,0)
        self.y_speed = random.randrange(int(10*SNOWFLAKE_YSPEED_MIN),int(10*SNOWFLAKE_YSPEED_MAX))/10.0 # pixels per s
        self.x_speed = random.randrange(int(10*SNOWFLAKE_XSPEED_MIN),int(10*SNOWFLAKE_XSPEED_MAX))/10.0 # pixels per s
        self.last_position_time = 0
        print ("Created drop at pixel", self.x, "moving at", self.y_speed,"pps vertical, ",self.x_speed,"pps horizontal")


class Rain(Animation):

    def __init__(self):
        super().__init__(True)
        self.drops = list()
        return

    def advance_drop(self, drop):
        #print ("Inspecting drop at", drop.x, drop.y,"moving at", drop.y_speed,"pixels per s")
        if (drop.y > 14):
            return False
        this_position_time = datetime.datetime.now()
        if (drop.last_position_time == 0):
            # first render, start at the start point
            drop.y = drop.y
        else:
            ms_since_last_render = (this_position_time - drop.last_position_time).total_seconds() * 1000
            #print("It has been",ms_since_last_render,"ms since last rendering")
            drop.y += (ms_since_last_render * drop.y_speed / 1000.0)
            drop.x += (ms_since_last_render * drop.x_speed / 1000.0)
        drop.last_position_time = this_position_time
        #print ("Setting drop to", drop.x, drop.y)
        return True

    def update_positions(self, ms_elapsed):

        # need some drops?
        while len(self.drops) < SNOWFLAKE_MIN_COUNT:
            self.drops.append(Drop(self.disp_width))

        # advance all the existing drops
        self.drops[:] = [drop for drop in self.drops if self.advance_drop(drop)]

    def render_into_image(self, img):
        draw = ImageDraw.Draw(img)
        disp_width, disp_height = img.size
        for col in range(0, self.disp_width):
            for row in range(0, self.disp_height):
                for drop in self.drops:
                    #print("For row",row,"col",col,", inspecting drop at",drop.x,drop.y)
                    if (drop.x >= col) and (drop.x < col+1):
                        if (drop.y >= row) and (drop.y < row+1):
                            draw.point((col,row), (255,255,255))
