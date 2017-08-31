#include <stdio.h>
#include <stdlib.h>
#include <time.h>

FILE *pFile;


// Kernel Stuff
int kernel_size_exponent = 10;
int kernel_base = 3;
int no_of_kernel = 1;
int *kernel;
int stride = 1;

// Image Stuff
int Image_Row = 1280;
int Image_Columns = 720;
int Image_Depth = 3;
int *input_image;
int *input_image_flattened;
int *output_image;

int main()
{
    char output_file[100];

    sprintf(output_file, "Image_size_%dx%d_data.txt", Image_Row, Image_Columns);
    pFile = fopen(output_file, "w");

    srand(time(NULL));

    int i;

    kernel = (int *)malloc(kernel_base*kernel_base*no_of_kernel*sizeof(int));


    input_image = (int *)malloc(Image_Columns*Image_Row*Image_Depth*sizeof(int));

    input_image_flattened = (int *)malloc(Image_Columns*Image_Row* sizeof(int));

    output_image = (int *)malloc((Image_Columns-kernel_base+1)*(Image_Row-kernel_base+1)*no_of_kernel*sizeof(int));


    generate_random_image();

    for(i=0; i<=kernel_size_exponent; i=i+1)
    {

        double output_generation_time_1 = clock();
        c_conv(Image_Depth, no_of_kernel, kernel_base, stride);
        double output_generation_time_2 = clock();
        double output_generation_time = (output_generation_time_2 - output_generation_time_1)/CLOCKS_PER_SEC;

        printf("\nOutput generation time = %g\n", output_generation_time);
        fprintf(pFile, "\nOutput generation time = %g\n", output_generation_time);

        no_of_kernel = no_of_kernel*2;

    }

    free(input_image);
    free(input_image_flattened);
    free(output_image);
    free(kernel);

    fclose(pFile);
    return 0;
}


// Generate random image
int generate_random_image()
{
    int i, j, k;
    for(i=0; i<Image_Row; i=i+1)
    {
        for(j=0; j<Image_Columns; j=j+1)
        {
            for(k=0; k<Image_Depth; k=k+1)
            {
                input_image[i*Image_Depth*Image_Columns + j*Image_Depth + k] = rand()%256;
                //input_image[i][j][k] = rand()%256
            }
        }
    }
    return 0;
}


int image_flatten(int in_channel)
{
    int i, j, k;
    for(i=0; i<Image_Row; i=i+1)
    {
        for(j=0; j<Image_Columns; j=j+1)
        {
            input_image_flattened[i*Image_Columns + j] = 0;

            for(k=0; k<in_channel; k=k+1)
            {
                input_image_flattened[i*Image_Columns + j] +=  input_image[i*in_channel*Image_Columns + j*in_channel + k];
            }
        }
    }
    return 0;
}


int generate_random_kernel(int o_channel, int kernel_size)
{
    int i, j ,k;
    free(kernel);
    kernel = (int *)malloc(kernel_size*kernel_size*o_channel*sizeof(int));

    for(i=0; i<kernel_size; i=i+1)
    {
        for(j=0; j<kernel_size; j=j+1)
        {
            for(k=0; k<o_channel; k=k+1)
            {
                kernel[i*kernel_size*o_channel + j*o_channel + k] = rand() % 8;
            }
        }
    }
    return 0;
}



int c_conv(int in_channel, int o_channel, int kernel_size, int stride)
{
    int i, j, k;
    int l, m;
    int Image_Row = 1280;
    int Image_Columns = 720;
    int Image_Depth = 3;

    double flattening_time_start = clock();

    image_flatten(in_channel);

// Calculate time to flatten the image
    double flattening_time_end = clock();
    double flattening_time = (flattening_time_end - flattening_time_start)/CLOCKS_PER_SEC;
    printf("\n%dx%d Image Flattening time = %g\n", Image_Row, Image_Columns, flattening_time);
    fprintf(pFile, "\n%dx%d size image flattening time = %g\n", Image_Row, Image_Columns, flattening_time);


    printf("For output channels = %d:\n", o_channel);
    fprintf(pFile, "For output channels = %d:\n", o_channel);
    double kernel_generation_time_start = clock();

    generate_random_kernel(o_channel, kernel_size);

    double kernel_generation_time_end = clock();
    double kernel_modification_time = (kernel_generation_time_end - kernel_generation_time_end)/CLOCKS_PER_SEC;
    printf("Kernel modification time = %g\n", kernel_modification_time);
    fprintf(pFile, "Kernel modification time = %g\n", kernel_modification_time);

    int output_rows = (int)((Image_Row-kernel_size)/stride) + 1;
    int output_columns = (int)((Image_Columns-kernel_size)/stride) + 1;
    free(output_image);
    

    output_image = (int *)malloc((output_columns)*(output_rows)*o_channel*sizeof(int));

    for(i=0; i<output_rows; i=i+1)
    {
        for(j=0; j<output_columns; j=j+1)
        {
            for(k=0; k<o_channel; k=k+1)
            {
                output_image[i*(output_columns)*o_channel + j*o_channel + k] = 0;

                for(l=0; l<kernel_size; l=l+1)
                {
                    for(m=0; m<kernel_size; m=m+1)
                    {
                        output_image[i*(output_columns)*o_channel + j*o_channel + k] += input_image_flattened[(i*stride+l)*(Image_Columns-kernel_size+1) + (j*stride+z)] * kernel[l*kernel_size*o_channel + m*o_channel + k] ;
                    }
                }
            }
        }
    }

    return 0;

}


