import asyncio

SOCKET_ADDRESS = '127.0.0.1'
SOCKET_PORT = 59993

@asyncio.coroutine
def echo_client(msg, loop):
    reader, writer = yield from asyncio.open_connection(
        SOCKET_ADDRESS,
        SOCKET_PORT,
        loop=loop,
    )

    print('Send: {}'.format(msg))
    writer.write(msg.encode())

    data = yield from reader.read(100)
    print("Received: {}".format(data.decode()))

    writer.close()

#@asyncio.coroutine
#def blink_client(msg, loop):
    #reader, writer = yield from asyncio.open_unix_connection('/var/run/blinkd', loop=loop)

message = "pulse 10 10 10 2 1000 60"
loop = asyncio.get_event_loop()
loop.run_until_complete(echo_client(message, loop))

loop.close()
