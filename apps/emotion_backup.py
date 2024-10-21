# App to read the accelerometer, heart sensor data and predict emotion.
# Development in progress

import wasp
import watch
import fonts


class EmotionApp():
    NAME = 'Emotion'

    def __init__(self):
        watch.accel.reset()

        self.xyz_data = None
        self.steps_data = None
        self.heart_rate_data = None

        self._count = 0

        self.draw = wasp.watch.drawable

    def foreground(self):
        self.draw.fill()
        self._draw()
        wasp.system.request_tick(1000 // 8)

    def background(self):
        wasp.watch.hrs.disable()

    def tick(self, ticks):
        self._count += 686;
        self._update()
        wasp.system.keep_awake()

    def _draw(self):
        self._update()
        self.draw.fill()

    def _update(self):
        # Update the step count
        self.steps_data = str(watch.accel.steps)
        w = fonts.width(fonts.sans24, self.steps_data)
        self._render(self.steps_data, 50 - 18, w)

        # Update the xyz axis
        self.xyz_data = str(self._accel_xyz())
        w = fonts.width(fonts.sans24, self.xyz_data)
        self._render(self.xyz_data, 125 - 18, w)

        # Update the heart rate
        self.heart_rate_data = str(self._heart_rate())
        w = fonts.width(fonts.sans24, self.heart_rate_data)
        self._render(self.heart_rate_data, 200 - 18, w)

    def _render(self, data, y_position, width):
        draw = wasp.watch.drawable
        draw.set_font(fonts.sans24)
        draw.set_color(draw.lighten(wasp.system.theme('spot1'), wasp.system.theme('contrast')))
        draw.string(data, 240 - width, y_position)

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
        hrdata = wasp.watch.hrs.read_hrs()
        # hrdata is the raw dataclasses implement you code below
        return hrdata