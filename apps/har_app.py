import array
import wasp
import watch
import har

class HarApp():
    NAME = "HAR"

    def __init__(self):
        self.draw = wasp.watch.drawable

        watch.accel.reset()
        self.xyz_data = None

        self.x_arr = array.array('i', [0, 0, 0, 0, 0])
        self.y_arr = array.array('i', [0, 0, 0, 0, 0])
        self.z_arr = array.array('i', [0, 0, 0, 0, 0])

        self.even = None
        self.odd = self.even

        self.now_sec = 0

    def foreground(self):
        wasp.system.request_tick(125)
        self.draw.fill()
        self._draw()

    def tick(self, ticks):
        self._draw()
        wasp.system.keep_awake()

    def _draw(self):
        draw = wasp.watch.drawable
        draw.fill()
        self.now_sec = wasp.watch.rtc.get_time()[2]
        if self.now_sec % 2 == 0:
            self.even = har.add_ints_array(list(self.x_arr), list(self.y_arr), list(self.z_arr))
            draw.string('{} Even '.format(self.even), 0, 108, width=240)
        else:
            self.odd = har.add_ints_array(list(self.z_arr), list(self.y_arr), list(self.x_arr))
            draw.string('{} Odd '.format(self.odd), 0, 108, width=240)

    def _accel_xyz(self):
        orientation = const(0b010010101)
        watch.accel._orientation = orientation
        raw = watch.accel._dev.read_accel_xyz()
        x = raw[watch.accel._orientation >> 7 & 0b11] * ((watch.accel._orientation >> 1 & 0b10) - 1)
        y = raw[watch.accel._orientation >> 5 & 0b11] * ((watch.accel._orientation      & 0b10) - 1)
        z = raw[watch.accel._orientation >> 3 & 0b11] * ((watch.accel._orientation << 1 & 0b10) - 1)
        return [x, y, z]


