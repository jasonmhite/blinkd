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
        self.__doc__ = handler.__doc__

    def run(self, *args):
        return self.handler(*args)

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
    return COMMANDS[cmd].__doc__

if __name__ == '__main__':
    set_random.run()
    print(COMMANDS)
