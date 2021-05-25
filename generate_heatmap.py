import numpy as np
from PIL import Image
from scipy.stats import multivariate_normal


# HEIGHT and WIDTH refer to the size of the output image
HEIGHT = 256
WIDTH = 256

# Number of elements per divisions, must be positive integer
# If the elements should be squares, one parameter can be set to None
# Height and Width have to be dividable by num
NUM_HEIGHT = 64
NUM_WIDTH = None

# Heat distributions: (x, y, x_variance, y_variance)
# All values must be chosen between 0 and 1 as fractions of length and width
DISTS = [
    (0.5, 0.5, 1.0, 1.0),
    (0.6, 0.6, 2.5, 2.5)
]


def generate():
    valid = True
    num_height = NUM_HEIGHT
    num_width = NUM_WIDTH
    if num_height and num_width:
        if (HEIGHT % num_height != 0) or (WIDTH % num_width != 0):
            print("HEIGHT or WIDTH is not dividable by NUM")
            valid = False
        else:
            h = HEIGHT / num_height
            w = WIDTH / num_width
    elif num_height:
        if HEIGHT % num_height != 0:
            print("HEIGHT is not dividable by NUM")
            valid = False
        else:
            h = HEIGHT / num_height
            if WIDTH % h == 0:
                w = h
                num_width = WIDTH / w
            else:
                i = 1
                while True:
                    if i > 10:
                        print("No square value can be found")
                        valid = False
                        break
                    else:
                        if WIDTH % (h + i) == 0:
                            w = h + i
                            num_width = WIDTH / w
                            break
                        elif WIDTH % (h - i) == 0:
                            w = h - i
                            num_width = WIDTH / w
                            break
                        i += 1
    else:
        if WIDTH % num_width != 0:
            print("WIDTH is not dividable by NUM")
            valid = False
        else:
            w = WIDTH / num_width
            if HEIGHT % w == 0:
                h = w
                num_height = HEIGHT / h
            else:
                i = 1
                while True:
                    if i > 10:
                        print("No square value can be found")
                        valid = False
                        break
                    else:
                        if HEIGHT % (w + i) == 0:
                            h = w + i
                            num_height = HEIGHT / h
                            break
                        elif HEIGHT % (w - i) == 0:
                            h = w - i
                            num_height = HEIGHT / h
                            break
                        i += 1
    if valid:
        num_width = int(num_width)
        num_height = int(num_height)
        center_points = [(x * h + (h / 2), y * w + (w / 2)) for y in range(num_width) for x in range(num_height)]
        arr = np.zeros((HEIGHT, WIDTH))
        values = [0] * (num_width * num_height)
        for dist in DISTS:
            distribution = multivariate_normal([dist[0] * HEIGHT, dist[1] * WIDTH],
                                               [[dist[2] * HEIGHT, 0], [0, dist[3] * WIDTH]])
            results = distribution.pdf(center_points)
            max_val = max(results)
            results = [i / max_val for i in results]
            new_values = [n if n > o else o for n, o in zip(results, values)]
            values = new_values
        for val, point in zip(values, center_points):
            arr[int(point[0] - (h / 2)): int(point[0] + (h / 2)),
                int(point[1] - (w / 2)): int(point[1] + (w / 2))] = val * 255
        img = Image.fromarray(np.uint8(arr), 'L')
        img.show()
        img.save("heatmap.png")


if __name__ == "__main__":
    generate()
