import sys
import liblo, pyautogui

# create server, listening on port 1234
try:
    target = liblo.Address("osc.udp://hawat:3819")
    server = liblo.Server(8000)
except liblo.ServerError as err:
    print(err)
    sys.exit()


def transport_stop_callback(path, args):
    if (args[0] == 1):
        pyautogui.keyDown('v')
        pyautogui.keyUp('v')
        print('stop')


def transport_play_callback(path, args):
    if (args[0] == 1):
        pyautogui.keyDown('v')
        pyautogui.keyUp('v')
        print('play')


def fallback(path, args, types, src):
    fallback_list = ['/strip/meter/1', '/strip/signal/1', '/strip/meter/2', '/strip/signal/2', '/select/meter', '/select/signal']
    if path not in fallback_list:
        # print("got unknown message '%s' from '%s'" % (path, src.url))
        for a, t in zip(args, types):
            # print("argument of type '%s': %s" % (t, a))
            pass

# register method taking an int and a float
server.add_method("/transport_stop", 'i', transport_stop_callback)
server.add_method("/transport_play", 'i', transport_play_callback)

# register a fallback for unhandled messages
server.add_method(None, None, fallback)

# loop and dispatch messages every 100ms
liblo.send(target, "/set_surface", 0, 32, 16, 0)
while True:
    server.recv(1000)
    liblo.send(target, "/transport_stop", 0)
