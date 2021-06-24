import numpy as np

def full_layout(x_boxes, y_boxes, vert=False, horz=False):
    """ x_boxes: Number of Beer Crates horizontal
        y_boxes: Number of Beer Crates vertical"""
    layout = matrix = np.array([[0, 9, 10, 19],
                                [1, 8, 11, 18],
                                [2, 7, 12, 17],
                                [3, 6, 13, 16],
                                [4, 5, 14, 15]])
    for x in range(1, x_boxes):
        layout = np.concatenate((layout, matrix+x*20), axis=1)
    for y in range(1, y_boxes):
        layout = np.concatenate((layout, layout+x_boxes*y*20), axis=0)

    if vert:
        layout = np.fliplr(layout)
    if horz:
        layout = np.flipud(layout)
    return layout
