import asyncio
import os

# Simple client:
# echo "cmd ..args.." | nc 127.0.0.1 59993

from protocol import COMMANDS

SOCKET_ADDRESS = '127.0.0.1'
SOCKET_PORT = 59993

loop = asyncio.get_event_loop()
lock = asyncio.Lock(loop=loop)

@asyncio.coroutine
def handle_command(reader, writer):
    try:
        data = yield from reader.read(100)
        args = data.decode().strip().split(" ")
        cmd = args.pop(0)

        print("Command: {}".format(cmd))
        print("Args: {}".format(args))

        with (yield from lock):
            try:
                r = COMMANDS[cmd].run(*args)
            except KeyError:
                raise Exception('Command {} not found'.format(cmd))

        if r is None:
            writer.write("OK".encode())
        else:
            writer.write((str(r) + "\n").encode())

        yield from writer.drain()

    except Exception as e:
        r = "ERR: {}\n".format(e)
        writer.write(r.encode())

        yield from writer.drain()

    finally:
        writer.close()

coro = asyncio.start_server(
    handle_command,
    SOCKET_ADDRESS,
    SOCKET_PORT,
    loop=loop,
)
server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
