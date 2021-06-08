import time
import board
import neopixel
from PIL import Image, ImageSequence
import layout
from filelock import Timeout, FileLock
import pickle

file_path = "waiting_line"
lock_path = "waiting_line.lock"

lock = FileLock(lock_path, timeout=1)

def post_media():
    """This method should connect to to the Media Input
    In our case blinky_bot
    Then it'll overwrite the background before beeing shown 
    on the strip
    Input should be given as coordinate with RGB value
    """

    global active       #Are we displaying media atm?
    global start        #When did we start displaying media?
    global waiting_line #What media is queued?

    def update_line():
        done_media = []
        with lock.acquire():
            pfile = open(file_path, 'rb')
            waiting_line_bot = pickle.load(pfile)
            for media in waiting_line_bot:
                if media not in waiting_line:
                    done_media.append(media)
                else:
                    break
            waiting_line = [ x for x in waiting_line_bot if x not in done_media ]
            pickle.dump( waiting_line, pfile )


    def draw_media(media):
        # pixel = [(x,y) , (int,int,int)]
        for pixel in media:
            strip[matrix[pixel[0]]] = pixel[1]

    if active:
        # pixel = [(x,y) , (int,int,int)]
        draw_media(waiting_line[0])
        if (time.time() - start) > 13:
            waiting_line.pop(0)
            active = False
    elif waiting_line:
        active = True
        start = time.time()
        draw_media(waiting_line[0])



if __name__ == '__main__':
    X_BOXES = 5
    Y_BOXES = 3
    LED_COUNT = X_BOXES * Y_BOXES * 20
    DISPLAY_RESOLUTION = (X_BOXES * 4, Y_BOXES * 5)

    #Setup LED stripe
    strip = neopixel.NeoPixel(board.D18, LED_COUNT,brightness=1,auto_write=False)

    #Setup Display Matrix
    matrix = layout.full_layout(X_BOXES, Y_BOXES)

    #Setup Media Wait list
    waiting_line = []
    active = False
    start = time.time()
    try:
        while True:
            #Load background gif. Should be exactly the Screen resolution
            im = Image.open('blinky_test.gif')
            if (im.size[0] < DISPLAY_RESOLUTION[0] or
                    im.size[1] < DISPLAY_RESOLUTION[1]):
                #fallback gif should be placed if the background is wrongly composed
                im = Image.open('fallback.gif')

            for frame in ImageSequence.Iterator(im):
                rgb_frame = frame.convert('RGB')
                for y in range(DISPLAY_RESOLUTION[1]):
                    for x in range(DISPLAY_RESOLUTION[0]):
                        strip[matrix[(x,y)]] = rgb_frame.getpixel((x,y))
                post_media()
                strip.show()
                #TODO Do gifs always have a duration?
                if 'duration' in frame.info:
                    if type(frame.info['duration']) is int:
                        time.sleep(frame.info['duration']/1000)
                    else:
                        time.sleep(0.1)
                else:
                    time.sleep(0.1)

    except KeyboardInterrupt:
        for y in range(DISPLAY_RESOLUTION[1]):
            for x in range(DISPLAY_RESOLUTION[0]):
                #It's not a bug it's a feature
                strip[matrix[(x,y)]] = (0,0,0)
                strip.show()
