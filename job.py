class Job:
    """
    A basic display job -- a thing that shows stuff on the display. Jobs have
    the notion of a duration -- either finite or infinite. They run
    synchronously.
    """

    def __init__(self, disp):
        self.disp = disp
        self.disp_width, self.disp_height = disp.im.size
        self.exit_asap = False

    def do(self):
        raise Exception("Why doesn't this job have an implementation?")
        return

    def set_exit_asap():
        self.exit_asap = True
