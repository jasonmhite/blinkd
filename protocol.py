from blinkstick import blinkstick

STICK = blinkstick.find_first()

COMMANDS = {}

class CommandFactory(type):
    def __call__(cls, *args, **kwargs):
        C = type.__call__(cls, *args, **kwargs)

        global COMMANDS
        COMMANDS[C.handler.__name__] = C

        return C

class Command(object, metaclass=CommandFactory):
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
    STICK.set_color(red=int(r), green=int(g), blue=int(b))

@Command
def pulse(r, g, b, repeats, duration, steps):
    STICK.pulse(
        red=int(r),
        green=int(g),
        blue=int(b),
        repeats=int(repeats),
        duration=int(duration),
        steps=int(steps),
    )

@Command
def morph(r, g, b, duration, steps):
    STICK.morph(
        red=int(r),
        green=int(g),
        blue=int(b),
        duration=int(duration),
        steps=int(steps),
    )

@Command
def get_color():
    col = STICK.get_color()
    return col

if __name__ == '__main__':
    set_random.run()
    print(COMMANDS)
