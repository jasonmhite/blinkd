import asyncio
import protocol

@asyncio.coroutine
def handle_echo(reader, writer):
    data = yield from reader.read(100)
    msg = data.decode()

    print("Received: {}".format(msg))

    writer.write("OK".encode())
    yield from writer.drain()

    writer.close()

loop = asyncio.get_event_loop()
#coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
coro = asyncio.start_unix_server(handle_echo, '/var/run/blinkd', loop=loop)
server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
