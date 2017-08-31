from conv import Conv2D
# import numpy as np
import matplotlib.image as img
# import matplotlib.pyplot as plt
from PIL import Image

if __name__ == "__main__":
    input_image_name = "cb.jpg"
    input_image = img.imread(input_image_name)

    # ==================Part A===================
    conv2d = Conv2D(3, 2, 3, 1)
    number_of_ops, output_image = conv2d.forward(input_image)
    output_image_rows, output_image_columns, output_image_channels = output_image.shape

    # for i in range(output_image_channels):
    #     # Normalize image to 0 1, and then multiply by 255 to get back the image
    #     I8 = (((output_image[:, :, i] - output_image[:, :, i].min()) / (output_image[:, :, i].max() - output_image[:, :, i].min())) * 255.0).astype(np.uint8)
    #     grayscale_image = Image.fromarray(I8)
    #     output_image_name = str(i + 1) + ".jpg"
    #     grayscale_image.save(output_image_name)

    print (number_of_ops)

    # # ==================Part B==================
    # for i in range(10):
    #     import math
    #     conv2d = Conv2D(3, int(math.pow(2, i)), 3, 1, 'rand')
    #     import timeit
    #     start_time = timeit.default_timer()
    #     # code you want to evaluate
    #     x, output_image = conv2d.forward(input_image)
    #     elapsed = timeit.default_timer() - start_time
    #     print (i, elapsed)

    # # ==================Part C==================
    # for x in range(3, 13, 2):
    #     conv2d = Conv2D(3, 2, x, 1, 'rand')
    #     number_of_ops, output_image = conv2d.forward(input_image)
    #     print (x, number_of_ops)
