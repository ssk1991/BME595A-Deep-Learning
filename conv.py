import numpy as np
import matplotlib.image as img
from PIL import Image


class Conv2D:

    def __init__(self, in_channel, o_channel, kernel_size, stride, mode='known'):

        # Represent the kernel as a 1D tensor, and then reshape it to a rectangle
        self.in_channel = in_channel
        self.o_channel = o_channel
        self.kernel_size = kernel_size
        self.stride = stride
        self.mode = mode

    def forward(self, input_image):
        # Number of operations
        ops = 0

        self.input_image = input_image

        # Add the RGB channels to create one single channel
        # This saves time with convolution. Basically instead of multiplying 3 times and then adding 3 times
        # We can first add 3 and then multiply once
        input_image_condensed = self.input_image[:, :, 0] + self.input_image[:, :, 1] + self.input_image[:, :, 2]

        # input_image number of rows, columns, and number of channels
        input_image_r, input_image_c = input_image_condensed.shape
        ops = ops + 3 * (input_image_r + 1) * (input_image_c + 1)
        # The output image dimensions will be different from the input image due to the convolution. Source CS231 Stanford. Remember to round down in case of an integer
        output_image_r = int((input_image_r - self.kernel_size) / self.stride + 1)
        output_image_c = int((input_image_c - self.kernel_size) / self.stride + 1)

        # Initialize the output image with zeros
        output_image = np.zeros((output_image_r, output_image_c, self.o_channel))

        # Initialize the kernel
        #kernel = np.zeros((self.kernel_size,self.kernel_size,self.o_channel))

        if self.mode == 'rand':

            # Note how the order is changed. Numpy fucks this up somehow, or maybe I am missing something
            kernel = np.random.rand(self.o_channel, self.kernel_size, self.kernel_size)

        else:
            # Kernel stuff. If else statements allow for proper selection of kernels according to question prompt
            if self.kernel_size == 3:

                K1 = np.matrix('-1, -1, -1;  0, 0, 0;  1, 1, 1')
                K2 = np.matrix('-1,  0,  1; -1, 0, 1; -1, 0, 1')
                K3 = np.matrix('1,  1,  1;  1, 1, 1;  1, 1, 1')
                kernel = np.array((K1, K2, K3))

            elif self.kernel_size == 5:

                K1 = np.matrix('-1, -1, -1, -1, -1; -1, -1, -1, -1, -1; 0, 0, 0, 0, 0; 1, 1, 1, 1, 1; 1, 1, 1, 1, 1')
                K2 = np.matrix('-1, -1, 0, 1, 1; -1, -1, 0, 1, 1; -1, -1, 0, 1, 1; -1, -1, 0, 1, 1; -1, -1, 0, 1, 1')
                kernel = np.array((K1, K2))

            else:
                # default convolution
                K1 = np.matrix('-1, -1, -1;  0, 0, 0;  1, 1, 1')
                kernel = np.array((K1))

        # Following loops perform the convolution
        # for each channel of output you will have one kernel
        # Channel refers to output channel
        for channel in range(self.o_channel):

            # Perform the convolution using for loops. Move kernel by stride length every iteration
            for i in range(0, output_image_r, self.stride):

                for j in range(0, output_image_c, self.stride):

                    # Tricky bit
                    # output_image [i,j] <=> input_image [i*stride, j*stride]
                    output_image[i][j][channel] = np.sum([input_image_condensed[i * self.stride: i * self.stride + self.kernel_size, j * self.stride: j * self.stride + self.kernel_size] * kernel[channel]])
                    ops = ops + 2 * self.kernel_size * self.kernel_size

        return ops, output_image


# if __name__ == "__main__":
#     input_image_name = "cb.jpg"
#     input_image = img.imread(input_image_name)

#     # # Part A
#     # conv2d = Conv2D(3, 1, 3, 1)
#     # number_of_ops, output_image = conv2d.forward(input_image)
#     # output_image_rows, output_image_columns, output_image_channels = output_image.shape

#     # for i in range(output_image_channels):
#     #     # Normalize image to 0 1, and then multiply by 255 to get back the image
#     #     I8 = (((output_image[:, :, i] - output_image[:, :, i].min()) / (output_image[:, :, i].max() - output_image[:, :, i].min())) * 255.0).astype(np.uint8)
#     #     grayscale_image = Image.fromarray(I8)
#     #     output_image_name = str(i + 1) + ".jpg"
#     #     grayscale_image.save(output_image_name)

#     # print (number_of_ops)

#     # Part B
#     # for i in range(10):
#     #     import math
#     #     conv2d = Conv2D(3, int(math.pow(2, i)), 3, 1, 'rand')
#     #     import timeit
#     #     start_time = timeit.default_timer()
#     #     # code you want to evaluate
#     #     x, output_image = conv2d.forward(input_image)
#     #     elapsed = timeit.default_timer() - start_time
#     #     print (i, elapsed)

#     # Part C
#     for x in range(3, 13, 2):
#         conv2d = Conv2D(3, 2, x, 1, 'rand')
#         number_of_ops, output_image = conv2d.forward(input_image)
#         print (x, number_of_ops)
