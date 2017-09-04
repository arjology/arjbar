import sys,time

class UnknownLength: pass

class arjBar(object):
    """Starts measuring time, and prints the bar at 0%.
    It returns self so you can use it like this:
    >>> N = 100
    >>> width = 20
    >>> bar = arjbar(N,width)
    >>> bar.arjbarstart()
    >>> for i in range(N):
    ...    # do something
    ...    bar.update(i+1)
    ...
    >>> bar.finish()
    """

    def __init__(self,size=None, width=None, widget="#", s=sys.stdout):
        self.size = size

        self.__iterable = None
        self.val = 0
        self.finished = False
        self.last_update_time = None
        self.seconds_elapsed = 0
        self.runtime = 0.0
        self.size = size
        self.start_time = None
        self.width=width
        self.widget = widget
        self.s = s
        self.rate = [0,0,0]

        if width is not None:
            self.term_width = width
        else:
            raise SystemExit('Width not specified')

    def __call__(self, iterable):
        try:
            self.size = len(iterable)
        except:
            if self.size is None:
                self.size = UnknownLength

        self.__iterable = iter(iterable)
        return self


    def __iter__(self):
        return self


    def __next__(self):
        try:
            value = next(self.__iterable)
            if self.start_time is None:
                self.start()
            else:
                self.update(self.val + 1)
            return value
        except StopIteration:
            if self.start_time is None:
                self.start()
            self.finish()
            raise

    # Create an alias so that Python 2.x won't complain about not being
    # an iterator.
    next = __next__

    def percentage(self):
        if self.val >= self.size:
            return 100.0
        return (self.val * 100.0 / self.size) if self.size else 100.00
    percent = property(percentage)

    def rate_completed(self):
        if self.val==0: return 0.0
        self.rate = self.rate[1:] + [self.val]
        return round(sum(self.rate)/3.0/self.runtime,4)
    current_rate = property(rate_completed)

    def _format_line(self):
        percent = self.percentage()
        current_rate = self.rate_completed()
        hashes = self.widget * int(round(percent/100.0 * self.size))
        spaces = ' ' * (self.size - len(hashes))
        return "\rPercent: [{0}] {1}% completed in {2} seconds ({3}/s))".format(hashes + spaces, 
            int(round(percent)), 
            self.seconds_elapsed,
            current_rate)

    def update(self, value=None):
        """Updates the ProgressBar to a new value."""

        if value is not None and value is not UnknownLength:
            if (self.size is not UnknownLength
                and not 0 <= value <= self.size):

                raise ValueError('Value out of range')

            self.val = value

        if self.start_time is None:
            raise RuntimeError('You must call "start" before calling "update"')

        now = time.time()
        self.seconds_elapsed = round(now - self.start_time, 2)
        self.runtime = now - self.start_time
        self.s.write('\r' + self._format_line())
        self.s.flush()
        self.last_update_time = now

    def start(self):
        if self.size is None:
            raise ValueError('Value out of range')

        if self.size is not UnknownLength:
            if self.size < 0: raise ValueError('Value out of range')

        self.start_time = self.last_update_time = time.time()
        self.update(0)

        return self

    def finish(self):
        if self.finished:
            return
        self.finished = True
        self.update(self.size)
        self.s.write('\n')
