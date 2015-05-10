from blinkstick import blinkstick
from time import sleep

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
        self.__doc__ = handler.__doc__

    def run(self, *args):
        r, g, b = STICK.get_color()
        try:
            return self.handler(*args)
        except Exception:
            STICK.morph(red=r, green=g, blue=b, duration=500, steps=16)
            raise

    @classmethod
    def __call__(cls, handler):
        return cls(handler)

@Command
def turn_off():
    """Turn off LED. Args: None"""
    STICK.turn_off()

@Command
def set_random():
    """Set LED to a random color. Args: None"""
    STICK.set_random_color()

@Command
def set_color(r, g, b):
    """Set LED to color. Args: r g b"""
    STICK.set_color(red=int(r), green=int(g), blue=int(b))

@Command
def pulse(r, g, b, repeats, duration, steps):
    """Pulse LED. Args: r g b repeats duration steps"""
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
    """Morph LED. Args: r g b duration steps"""
    STICK.morph(
        red=int(r),
        green=int(g),
        blue=int(b),
        duration=int(duration),
        steps=int(steps),
    )

@Command
def get_color():
    """Get current color. Args: None"""
    col = STICK.get_color()
    return col

@Command
def help():
    """Print general usage."""
    txt = "Commands:\n"
    for cmd in COMMANDS.keys():
        txt += "  " + cmd + "\n"

    txt += "\nColors are ints [0-16]"

    return txt

@Command
def help_for(cmd):
    """Print help for a command. Args: cmd"""
    try:
        return COMMANDS[cmd].__doc__
    except KeyError:
        return "Command {} not found".format(cmd)

@Command
def test_fail():
    """Always fail. Args: None"""
    STICK.set_color(red=16, green=0, blue=0)
    raise Exception('Test Failure')

@Command
def set_total_brightness(pct):
    """Set current brightness to portion of max while maintaining color and
    set maximum for any single color to be under this limit. Because of the way
    the maximum brightness is enforced, it is possible to subsequently set to a
    higher total power by setting 2 or more colors to the max. Args: pct"""
    pct = int(pct)
    if pct > 100 or pct < 0:
        raise ValueError("Invalid percentage {}".format(pct))

    r, g, b = map(int, STICK.get_color())
    target_level = round(pct * 255 / 100)
    total = r + g + b

    r, g, b = [round(255 * i / total) for i in (r, g, b)]

    STICK.set_max_rgb_value(target_level)
    STICK.set_color(red=r, green=g, blue=b)

@Command
def get_total_brightness():
    """Get current total brightness as percentage of maximum. Args: None"""
    r, g, b = map(int, STICK.get_color())

    cb = 100 * (r + g + b) / (3. * 255)
    return cb

if __name__ == '__main__':
    set_random.run()
    print(COMMANDS)
