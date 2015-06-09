import socket
from time import sleep

SOCKET_ADDRESS = 'cube'
SOCKET_PORT = 2323

SLEEPTIME = 1

#@asyncio.coroutine
#def echo_client(msg):
    #try:
        #reader, writer = yield from asyncio.open_connection(
            #SOCKET_ADDRESS,
            #SOCKET_PORT,
            #loop=loop,
        #)

        #print('Send: {}'.format(msg))
        #writer.write(msg.encode())

        #data = yield from reader.read(100)
        #print("Received: {}".format(data.decode()))

        #writer.close()
    #except:
        #print("Failed to connect to daemon.")
        #sys.exit(1)

def echo_client(msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)

    try:
        s.connect((SOCKET_ADDRESS, SOCKET_PORT))

        print('Send: {}'.format(msg))
        s.send((msg + '\r\n').encode())

    except:
        raise

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
        try:
            msg = self.handler(*args)
            echo_client(msg)
            sleep(SLEEPTIME)
        except Exception:
            raise

    @classmethod
    def __call__(cls, handler):
        return cls(handler)

@Command
def set_color(r, g, b):
    """Set color. Args: r g b"""
    return "light.setColor({r}, {g}, {b})".format(r=r, g=g, b=b)

@Command
def turn_off():
    """Turn off LED. Args: None"""
    return "light.turnOff()"

@Command
def morph(r, g, b, t):
    """Morph to color. Args: r g b t"""
    return "light.morph({r}, {g}, {b}, {t})".format(r=r, g=g, b=b, t=t)

@Command
def pulse(r, g, b, t, n):
    """Pulse selected color, then return to base color."""
    return "light.pulse({r}, {g}, {b}, {t}, {n})".format(r=r, g=g, b=b, t=t, n=n)

if __name__ == '__main__':
    turn_off.run()
    pulse.run(.5, .5, .5, 2, 2)
