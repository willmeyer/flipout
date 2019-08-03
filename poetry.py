import text
import time
from job import Job
import transitions

POEMS = {
         "dew": ["A world of dew", "In every dewdrop", "A world of struggle"],
         "thoreau": ["My life has been the poem I would have writ", "But I could not both live and utter it."]
         }

class PoemsJob(Job):

    def __init__(self, disp):
        super().__init__(disp)

    def show_poem(self, name="dew"):
        fnt = False
        for line in POEMS[name]:
            text.scroll_text(self.disp, line, fnt)
            time.sleep(1.0)
        transitions.HorizontalWipeTransition(self.disp, False).do()

    def do(self):
        for name in POEMS:
            if self.exit_asap:
                break
            self.show_poem(name)
