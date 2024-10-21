import wasp
import machine
import watch
import ppg


class EmotionApp():
    NAME = 'Emotion'

    def __init__(self):
        watch.accel.reset()
        self.xyz_data = None
        self.steps_data = None
        self.heart_rate_data = None
        self._count = 0
        self.draw = wasp.watch.drawable
        self._hrdata = ppg.PPG(wasp.watch.hrs.read_hrs())

    def foreground(self):
        wasp.system.request_tick(1000 // 8)
        self.draw.fill()
        self._draw()
        self._heart_rate()

    def background(self):
        wasp.watch.hrs.disable()

    def tick(self, ticks):
        self._count += 686
        self._update()
        t = machine.Timer(id=1, period=8000000)
        t.start()
        self._subtick(1)
        wasp.system.keep_awake()
        while t.time() < 41666:
            pass
        self._subtick(1)
        while t.time() < 83332:
            pass
        self._subtick(1)
        t.stop()
        del t

    def _subtick(self, ticks):
        spl = self._hrdata.preprocess(wasp.watch.hrs.read_hrs())
        if len(self._hrdata.data) >= 240:
            self.heart_rate_data = str(self._hrdata.get_heart_rate())
            self._render(self.heart_rate_data, 200 - 18)

    def _draw(self):
        self._update()

    def _update(self):
        self.steps_data = str(watch.accel.steps)
        self._render(self.steps_data, 50 - 18)
        self.xyz_data = str(self._accel_xyz())
        self._render(self.xyz_data, 125 - 18)
        # self.heart_rate_data = str(self._heart_rate())
        # self._render(self.heart_rate_data, 200 - 18)
        self._log_data()

    def _render(self, data, y_position):
        draw = wasp.watch.drawable
        draw.string(data, 0, y_position, width=240)

    def _accel_xyz(self):
        orientation = const(0b010010101)
        watch.accel._orientation = orientation
        raw = watch.accel._dev.read_accel_xyz()
        x = raw[watch.accel._orientation >> 7 & 0b11] * ((watch.accel._orientation >> 1 & 0b10) - 1)
        y = raw[watch.accel._orientation >> 5 & 0b11] * ((watch.accel._orientation      & 0b10) - 1)
        z = raw[watch.accel._orientation >> 3 & 0b11] * ((watch.accel._orientation << 1 & 0b10) - 1)
        return [x, y, z]

    def _heart_rate(self):
        wasp.watch.hrs.enable()
        # self._hrdata = ppg.PPG(wasp.watch.hrs.read_hrs())
        # hrdata = wasp.watch.hrs.read_hrs()
        # return hrdata

    def _log_data(self):
        with open('log_file.log', 'a') as log_file:
            log_file.write('{},{},{},{}\n'.format(wasp.watch.rtc.get_time(), self.steps_data, self.xyz_data, self.heart_rate_data))
        return None
