import array
import wasp
import time
import watch
import har

class HarApp():
    NAME = "Har"

    def __init__(self):
        self.x = array.array('i', [1, 2, 3, 4, 5])
        self.y = array.array('i', [6, 7, 8, 9, 10])
        self.z = array.array('i', [11, 12, 13, 14, 15])
        self.even = None
        self.odd = self.even
        self.now_sec = 0

    def foreground(self):
        self._draw()
        wasp.system.request_tick(1000)

    def tick(self, ticks):
        self._draw()

    def _draw(self):
        draw = wasp.watch.drawable
        draw.fill()
        self.now_sec = wasp.watch.rtc.get_time()[2]
        if self.now_sec % 2 == 0:
            self.even = har.add_ints_array(list(self.x), list(self.y), list(self.z))
            draw.string('{} Even '.format(self.even), 0, 108, width=240)
        else:
            self.odd = har.add_ints_array(list(self.z), list(self.y), list(self.x))
            draw.string('{} Odd '.format(self.odd), 0, 108, width=240)
