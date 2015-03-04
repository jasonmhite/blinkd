import asyncio

@asyncio.coroutine
def echo_client(msg, loop):
    reader, writer = yield from asyncio.open_unix_connection('/var/run/blinkd', loop=loop)

    print('Send: {}'.format(msg))
    writer.write(msg.encode())

    data = yield from reader.read(100)
    print("Received: {}".format(data.decode()))

    writer.close()

message = "Hello"
loop = asyncio.get_event_loop()
loop.run_until_complete(echo_client(message, loop))

loop.close()
