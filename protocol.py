from blinkstick import blinkstick

STICK = blinkstick.find_first()

class Command(object):
    def __init__(self, handler):
        self.handler = handler

    def run(self, *args):
        return self.handler(*args)

    @classmethod
    def __call__(cls, handler):
        return cls(handler)

@Command
def turn_off():
    STICK.turn_off()

@Command
def set_random():
    STICK.set_random_color()

@Command
def set_color(r, g, b):
    STICK.set_color(red=r, green=g, blue=b)

@Command
def pulse(r, g, b, repeats, duration, steps):
    STICK.pulse(
        red=r,
        green=g,
        blue=b,
        repeats=repeats,
        duration=duration,
        steps=steps,
    )

@Command
def morph(r, g, b, duration, steps):
    STICK.morph(red=r, green=g, blue=b, duration=duration, steps=steps)

@Command
def get_color():
    col = STICK.get_color()
    return col
