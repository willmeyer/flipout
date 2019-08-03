import utils
import time
from PIL import ImageFont, ImageDraw


FONT_BIG = ImageFont.truetype(utils.rsrc("fonts/VeraBd.ttf"), 15)
FONT_SMALL = ImageFont.truetype(utils.rsrc("fonts/VeraBd.ttf"), 10)


def scroll_text(d, text, large=True):
    """
    Displays a line of text, scrolling it from left to right and off the screen,
    then finishes.
    """
    draw = ImageDraw.Draw(d.im)
    font = FONT_BIG if large else FONT_SMALL
    text_w, text_h = draw.textsize(text, font=font)
    shift = 0 if large else -2
    for x in range(d.im.size[0], 0-text_w, -1):
        d.reset()
        draw.text((x, 14-text_h+shift), text, font=font)
        d.send()
        time.sleep(0.08)
    del draw


def static_text(d, text, large=True):
    """
    Displays a line of text statically on the screen. It will be centered,
    whether or not it actually fits.
    """
    draw = ImageDraw.Draw(d.im)
    font = FONT_BIG if large else FONT_SMALL
    tw, th = draw.textsize(text, font=font)
    shift = -1 if large else -3
    d.reset()
    center_x=d.im.size[0]/2
    draw.text((center_x-(tw/2), 14-th+shift), text, font=font)
    d.send()
    del draw
