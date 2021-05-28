def matrix_init():
    led_id = 0
    matrix = dict()
    for i in range(5):
        matrix[(0,i)] = led_id
        led_id += 1
    for i in range(4,-1,-1):
        matrix[(1,i)] = led_id
        led_id += 1
    for i in range(5):
        matrix[(2,i)] = led_id
        led_id += 1
    for i in range(4,-1,-1):
        matrix[(3,i)] = led_id
        led_id += 1

    led_id = 19
    invers = dict()
    for i in range(5):
        invers[(0,i)] = led_id
        led_id -= 1
    for i in range(4,-1,-1):
        invers[(1,i)] = led_id
        led_id -= 1
    for i in range(5):
        invers[(2,i)] = led_id
        led_id -= 1
    for i in range(4,-1,-1):
        invers[(3,i)] = led_id
        led_id -= 1

    return (matrix, invers)

def full_layout(x_boxes, y_boxes):
    """ x_boxes: Number of Beer Crates horizontal
        y_boxes: Number of Beer Crates vertical"""
    matrix = matrix_init()
    layout = dict()
    box_count = 0
    for y in range(y_boxes):
        if y & 1:
            #'odd --> use invers
            for x in range(x_boxes-1, -1, -1):
                for k,v in matrix[1].items():
                    coordinate = (k[0] + (4*x), k[1] + (5*y))
                    layout[coordinate] = v + (20*box_count)
                box_count += 1
        else:
            #'even --> use matrix
            for x in range(x_boxes):
                for k,v in matrix[0].items():
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
    layout = full_layout(5,4)
    for y in range(19,-1,-1):
        for x in range(20):
            print(f'{layout[(x,y)]} ', end='')
        print(' ')
