def matrix_init():
    """Hardcoded Layout for a single crate
          (seen from front, up↥)
           ┏━━━━━━━━━━━━━━━━━┓
           ┃ ○ → ○   ○ → ○   ┃
           ┃ ↑   ↓   ↑   ↓   ┃
           ┃ ○   ○   ○   ○   ┃
           ┃ ↑   ↓   ↑   ↓   ┃
           ┃ ○   ○   ○   ○   ┃
           ┃ ↑   ↓   ↑   ↓   ┃
           ┃ ○   ○   ○   ○   ┃
           ┃ ↑   ↓   ↑   ↓   ┃
      {in}→┃ ○   ○ → ○   ○ → ┃→{out}
           ┗━━━━━━━━━━━━━━━━━┛
                  (down↧)

        We create the matrix and an inverse.
        For every second line of crates we can use the inverse 
        if we dont want to lay long cables .

        inverse=False
            ┏┓┏┓┏┓┏┓ ↑
          → ┗┛┗┛┗┛┗┛→↑
          <-----------
            ┏┓┏┓┏┓┏┓ ↑
          → ┗┛┗┛┗┛┗┛→↑
          <-----------
            ┏┓┏┓┏┓┏┓ ↑
          → ┗┛┗┛┗┛┗┛→↑

        inverse=True
            ┏┓┏┓┏┓┏┓
        ^ ->┗┛┗┛┗┛┗┛
        | <-┏┓┏┓┏┓┏┓<-
            ┗┛┗┛┗┛┗┛ ↑
            ┏┓┏┓┏┓┏┓ ↑
          → ┗┛┗┛┗┛┗┛→↑
"""

    #Din unten links
    led_id = 0
    unl = dict()
    for i in range(5):
        unl[(0,i)] = led_id
        led_id += 1
    for i in range(4,-1,-1):
        unl[(1,i)] = led_id
        led_id += 1
    for i in range(5):
        unl[(2,i)] = led_id
        led_id += 1
    for i in range(4,-1,-1):
        unl[(3,i)] = led_id
        led_id += 1

    #Din oben links
    led_id = 0
    obl = dict()
    for i in range(4,-1,-1):
        obl[(0,i)] = led_id
        led_id += 1
    for i in range(5):
        obl[(1,i)] = led_id
        led_id += 1
    for i in range(4,-1,-1):
        obl[(2,i)] = led_id
        led_id += 1
    for i in range(5):
        obl[(3,i)] = led_id
        led_id += 1

    #Din unten rechts
    led_id = 19
    unr = dict()
    for i in range(5):
        unr[(0,i)] = led_id
        led_id -= 1
    for i in range(4,-1,-1):
        unr[(1,i)] = led_id
        led_id -= 1
    for i in range(5):
        unr[(2,i)] = led_id
        led_id -= 1
    for i in range(4,-1,-1):
        unr[(3,i)] = led_id
        led_id -= 1

    #Din oben rechts
    led_id = 19
    obr = dict()
    for i in range(4,-1,-1):
        obr[(0,i)] = led_id
        led_id -= 1
    for i in range(5):
        obr[(1,i)] = led_id
        led_id -= 1
    for i in range(4,-1,-1):
        obr[(2,i)] = led_id
        led_id -= 1
    for i in range(5):
        obr[(3,i)] = led_id
        led_id -= 1

    return (obl,unl,obr,unr)

def full_layout(x_boxes, y_boxes, inverse=False, unten=False, rechts=False):
    """ x_boxes: Number of Beer Crates horizontal
        y_boxes: Number of Beer Crates vertical"""
    matrix = matrix_init()
    layout = dict()
    box_count = 0
    if not inverse:
        for y in range(y_boxes):
            for x in range(x_boxes):
                for k,v in matrix[1].items():
                    coordinate = (k[0] + (4*x), k[1] + (5*y))
                    layout[coordinate] = v + (20*box_count)
                box_count += 1
    else:
        for y in range(y_boxes):
            if y & 1:
                #'odd --> use invers
                for x in range(x_boxes-1, -1, -1):
                    for k,v in matrix[3].items():
                        coordinate = (k[0] + (4*x), k[1] + (5*y))
                        layout[coordinate] = v + (20*box_count)
                    box_count += 1
            else:
                #'even --> use matrix
                for x in range(x_boxes):
                    for k,v in matrix[1].items():
                        coordinate = (k[0] + (4*x), k[1] + (5*y))
                        layout[coordinate] = v + (20*box_count)
                    box_count += 1
    return layout


if __name__ == '__main__':
    matrix = matrix_init()
    print('Matrix')
    for k,v in matrix[0].items():
        print(f'{k}:{v}')
    print('++++++++')
    print('invers')
    for k,v in matrix[1].items():
        print(f'{k}:{v}')
    print('++++++++')
    print('full')
    layout = full_layout(5,4,inverse=True)
    for y in range(19,-1,-1):
        for x in range(20):
            print(f'{layout[(x,y)]} ', end='')
        print(' ')
    layout = full_layout(5,4)
    for y in range(19,-1,-1):
        for x in range(20):
            print(f'{layout[(x,y)]} ', end='')
        print(' ')
