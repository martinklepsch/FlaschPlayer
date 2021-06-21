import time
import board
import neopixel
from PIL import Image, ImageSequence
import layout
from filelock import Timeout, FileLock
import os
import random
import glob
import ast
from systemd import journal


def display_gif(strip, matrix, path_to_gif, DISPLAY_RESOLUTION, lock, BRIGHTNESS=1, post = True):
    global active       #Are we displaying media atm?
    global start        #When did we start displaying media?
    global update       #When did we update the waiting line
    global waiting_line #What media is queued?

    def update_line(lock):
        with lock:
            with open("/home/pi/ws2812b/config/waiting_line", 'r') as f:
                line = f.read()
                if len(line) > 1:
                    journal.write(f'waiting line: {line}')
                waiting_line = ast.literal_eval('[' + line[:-1] + ']')
            with open("/home/pi/ws2812b/config/waiting_line", 'w') as f:
                f.write('')
        return waiting_line


    def draw_frame(frame, DISPLAY_RESOLUTION, BRIGHTNESS):
        rgb_frame = frame.convert('RGB')
        for y in range(DISPLAY_RESOLUTION[1]):
            for x in range(DISPLAY_RESOLUTION[0]):
                strip[matrix[(x,y)]] = tuple( int(x * BRIGHTNESS) for x in rgb_frame.getpixel((x,y)))
        strip.show()
        if 'duration' in frame.info:
            if type(frame.info['duration']) is int:
                time.sleep(frame.info['duration']/1000) 
            else:
                time.sleep(0.1)
        else:
            time.sleep(0.1)


    background_gif = Image.open(path_to_gif + '.gif')
    journal.write(f'Back: {path_to_gif}.gif')
    if (background_gif.size[0] < DISPLAY_RESOLUTION[0] or
            background_gif.size[1] < DISPLAY_RESOLUTION[1]):
        #fallback gif should be placed if the background is wrongly composed
        background_gif = Image.open('fallback.gif')

    for frame in ImageSequence.Iterator(background_gif):
        draw_frame(frame, DISPLAY_RESOLUTION, BRIGHTNESS)
        waiting_line = update_line(lock)
        while waiting_line:
            for media in waiting_line:
                BRIGHTNESS = set_brightness()
                journal.write(f'Fore: {media}.gif')
                forground_gif = Image.open('/home/pi/ws2812b/gifs/' + str(media) + '.gif')
                if forground_gif.format == 'GIF':
                    for frame in ImageSequence.Iterator(forground_gif):
                        draw_frame(frame, DISPLAY_RESOLUTION, BRIGHTNESS)
                else:
                    #photos in gif container get shown 5 seconds
                    for n in range(50):
                        draw_frame(frame, DISPLAY_RESOLUTION, BRIGHTNESS)
                os.rename('/home/pi/ws2812b/gifs/' + str(media) + '.gif', '/home/pi/ws2812b/graveyard/' + str(time.time()) + '.gif')
            waiting_line = update_line(lock)


def set_brightness():
    options = [f for f in files("/home/pi/ws2812b/config/")]
    brightness = float([i for i in options if 'BRIGHTNESS' in i][0][11:])
    journal.write(f'Set Brightness: {brightness}')
    return brightness



def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


def init():
    with open("/home/pi/ws2812b/config/waiting_line", 'w') as f:
        f.write('')


def main(X_BOXES, Y_BOXES, BRIGHTNES ):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true",
                    help="debug mode")
    parser.add_argument("-dl", "--delay", type=float,
                    help="delay between set")
    parser.add_argument("-bl", "--blink", action='store_true',
                    help="delay between set")

    LED_COUNT = X_BOXES * Y_BOXES * 20
    DISPLAY_RESOLUTION = (X_BOXES * 4, Y_BOXES * 5)

    #Setup LED stripe
    strip = neopixel.NeoPixel(board.D18, LED_COUNT,brightness=1,auto_write=False)

    #Setup Display Matrix
    matrix = layout.full_layout(X_BOXES, Y_BOXES)

    #Setup Media Wait list
    waiting_line = []
    active = False
    start = update = time.time()

    args = parser.parse_args()


    #TODO DEBUG
    path_to_file='blinky'
    if args.blink:
        strip = neopixel.NeoPixel(board.D18, LED_COUNT,brightness=1,auto_write=True)
        try:
            if args.delay:
                delay = args.delay
            else:
                delay = 0.1
            while True:
                t = random.randint(0, 80)
                for y in range(0,255):
                    strip[t] = (y,y,y)
                    time.sleep(delay)
                    print(y)
                u = random.randint(0, 80)
                for y in range(0,255):
                    strip[u] = (y,y,y)
                    time.sleep(delay)
                    print(y)
                i = random.randint(0, 80)
                for y in range(0,255):
                    strip[i] = (y,y,y)
                    time.sleep(delay)
                    print(y)
                for y in range(255,-1,-1):
                    strip[i] = (y,y,y)
                    time.sleep(delay)
                    print(y)
                for y in range(255,-1,-1):
                    strip[t] = (y,y,y)
                    time.sleep(delay)
                    print(y)
                for y in range(255,-1,-1):
                    strip[u] = (y,y,y)
                    time.sleep(delay)
                    print(y)
        except KeyboardInterrupt:
            for y in range(DISPLAY_RESOLUTION[1]):
                for x in range(DISPLAY_RESOLUTION[0]):
                    #It's not a bug it's a feature
                    strip[matrix[(x,y)]] = (0,0,0)
                    strip.show()


    elif args.debug:
        strip = neopixel.NeoPixel(board.D18, LED_COUNT,brightness=1,auto_write=True)
        try:
            if args.delay:
                delay = args.delay
            else:
                delay = 0.1
            while True:
                for i in range(LED_COUNT):
                    strip[i] = (255,255,255)
                    time.sleep(delay)
                for i in range(LED_COUNT):
                    strip[i] = (255,0,0)
                    time.sleep(delay)
                for i in range(LED_COUNT):
                    strip[i] = (0,255,0)
                    time.sleep(delay)
                for i in range(LED_COUNT):
                    strip[i] = (0,0,255)
                    time.sleep(delay)
        except KeyboardInterrupt:
            for y in range(DISPLAY_RESOLUTION[1]):
                for x in range(DISPLAY_RESOLUTION[0]):
                    #It's not a bug it's a feature
                    strip[matrix[(x,y)]] = (0,0,0)


    else:
        try:
            os.makedirs("/home/pi/ws2812b/graveyard", exist_ok=True)
            os.chown("/home/pi/ws2812b/graveyard", uid=1000, gid=1000)
            os.makedirs("/home/pi/ws2812b/gifs", exist_ok=True)
            os.chown("/home/pi/ws2812b/gifs", uid=1000, gid=1000)
            file_path = "/home/pi/ws2812b/config/waiting_line"
            lock_path = "/home/pi/ws2812b/config/waiting_line.lock"

            lock = FileLock(lock_path, timeout=5)
            mylist = [f[:-4] for f in glob.glob("/home/pi/ws2812b/backgrounds/*.gif")]
            while True:
                #TODO loop through backgrounds
                #Load background gif. Should be exactly the Screen resolution
                brightness = set_brightness()
                display_gif(strip, matrix, random.choice(mylist), DISPLAY_RESOLUTION, lock, BRIGHTNESS=brightness)

        except KeyboardInterrupt:
            for y in range(DISPLAY_RESOLUTION[1]):
                for x in range(DISPLAY_RESOLUTION[0]):
                    #It's not a bug it's a feature
                    strip[matrix[(x,y)]] = (0,0,0)
if __name__ == '__main__':
    init()
    main(4,1,1)
