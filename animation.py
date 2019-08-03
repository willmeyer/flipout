import text
import time
from job import Job
import transitions
from PIL import Image, ImageDraw, ImageOps
import random
import utils

class AnimatorJob(Job):

    def __init__(self, disp, anim):
        self.anim = anim
        super().__init__(disp)

    def do(self):
        last_animation_time = time.time()
        self.anim.config_for_display(self.disp.im.size[1], self.disp.im.size[0])
        while not self.exit_asap:
            if self.anim.reset_before_render:
                self.disp.reset()
            this_animation_time = time.time()
            ms_elapsed = (this_animation_time - last_animation_time) * 1000
            print("Updating animations after",ms_elapsed,"ms...")
            self.anim.update_positions(ms_elapsed)
            self.anim.render_into_image(self.disp.im)
            last_animation_time = this_animation_time
            time.sleep(0.05)
            self.disp.send()

class Animation:

    def __init__(self, reset_before_render):
        self.reset_before_render = reset_before_render
        print("animated object initialized")

    def config_for_display(self, disp_height, disp_width):
        self.disp_height = disp_height
        self.disp_width = disp_width

    def update_positions(self, ms_elapsed):
        return

    def render_into_image(self, img):
        return

class HorizontalImageAnimation(Animation):

    def __init__(self, frame_filenames, captive=False, x_speed_pps=1.0, framerate=2.0):
        self.frame_images = []
        for filename in frame_filenames:
            img = Image.open(utils.rsrc(filename))
            self.frame_images.append(img)
        self.current_frame=-1
        if captive:
            self.x_pos = 0
        else:
            self.x_pos = 0-self.frame_images[0].size[0]
        self.y_pos = 0
        self.framerate = framerate
        self.ms_since_last_frame = 0
        self.x_speed_pps = x_speed_pps
        self.captive = captive
        self.x_direction = True
        super().__init__(True)

    def update_positions(self, ms_elapsed):

        # first, advance the frame.
        # advance by 1, not more (as long as the framerate dictates it's time for the next frame)
        ideal_ms_between_frames = 1.0 / self.framerate * 1000.0
        if ((self.ms_since_last_frame + ms_elapsed) > ideal_ms_between_frames):
            if (self.current_frame == len(self.frame_images)-1):
                self.current_frame = 0
            else:
                self.current_frame = self.current_frame + 1
            self.ms_since_last_frame = 0
        else:
            self.ms_since_last_frame = self.ms_since_last_frame + ms_elapsed

        # update the object's position
        x_shift = (ms_elapsed / 1000.0) * self.x_speed_pps
        if self.captive:
            if self.x_direction:
                if (self.x_pos + self.frame_images[self.current_frame].size[0]) >= self.disp_width:
                    print("Switching direction...")
                    self.x_direction = False
                    x_shift = 0
            else:
                if (self.x_pos <= 0):
                    self.x_direction = True
                    x_shift = 0
                else:
                    x_shift = -1*x_shift
        self.x_pos = self.x_pos + x_shift
        print("animated object position is", self.x_pos, self.y_pos)

    def render_into_image(self, img):
        frame = self.frame_images[self.current_frame]
        if self.x_direction == False:
            frame = ImageOps.mirror(frame)
        img.paste(frame, (int(self.x_pos), int(self.y_pos)))

class Noise(Animation):

    def __init__(self):
        super().__init__(True)
        return

    def update_positions(self, ms_elapsed):
        return

    def render_into_image(self, img):
        draw = ImageDraw.Draw(img)
        disp_width, disp_height = img.size
        for col in range(0, disp_width):
            for row in range(0, disp_height):
                if (random.choice([True, False])):
                    draw.point((col,row), (255,255,255))
                else:
                    draw.point((col,row), (0,0,0))
