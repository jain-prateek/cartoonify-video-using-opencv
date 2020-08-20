# cartoonify-video-using-opencv
code to cartoonify video using opencv

How to create a cool cartoon effect with OpenCV and Python
Over the last few years professional cartoonizer software has popped up all over the place but is only rarely freeware. In order to achieve the basic cartoon effect, you don't need powerful rendering software or even years of experience. All you need is essentially a bilateral filter and some edge detection. The bilateral filter will reduce the color palette, which is essential for the cartoon look, and edge detection will allow you to produce bold silhouettes.


Using OpenCV and Python, an RGB color image can be converted into a cartoon in five steps:

Apply a bilateral filter to reduce the color palette of the image.
Convert the original color image to grayscale.
Apply a median blur to reduce image noise in the grayscale image.
Create an edge mask from the grayscale image using adaptive thresholding.
Combine the color image from step 1 with the edge mask from step 4.

Step 1: Edge-aware smoothing using a bilateral filter
Because a bilateral filter smooths flat regions while keeping edges sharp, it is ideally suited to convert an RGB image into a cartoon. Unfortunately, bilateral filters are orders of magnitudes slower than other smoothing operators (e.g., Gaussian blur). Thus, if speed is important, it might be a good idea to operate on a down-scaled version of the original image. However, even at a reduced scale the bilateral filter might still be horrendously slow. Another trick is therefore to repeatedly (say, seven times via num_bilateral=7) apply a small bilateral filter instead of applying a large bilateral filter once:

import cv2

num_down = 2       # number of downsampling steps
num_bilateral = 7  # number of bilateral filtering steps

img_rgb = cv2.imread("img_example.jpg")

# downsample image using Gaussian pyramid
img_color = img_rgb
for _ in xrange(num_down):
    img_color = cv2.pyrDown(img_color)

# repeatedly apply small bilateral filter instead of
# applying one large filter
for _ in xrange(num_bilateral):
    img_color = cv2.bilateralFilter(img_color, d=9,
                                    sigmaColor=9,
                                    sigmaSpace=7)

# upsample image to original size
for _ in xrange(num_down):
    img_color = cv2.pyrUp(img_color)
The three parameters in cv2.bilateralFilter control the diameter of the pixel neighborhood (d) and the standard deviation of the filter in color space (sigmaColor) as well as coordinate space (sigmaSpace).

Steps 2-3: Reduce noise using a median filter
OpenCV offers a variety of choices when it comes to edge detection. The beauty of adaptive thresholding is that it detects the most salient features in each (small) neighborhood of an image, independent of the overall properties of the image, which is exactly what we want when we seek to draw bold, black outlines around objects and people in a cartoon. However, this property also makes adaptive thresholding susceptible to noise. It is therefor a good idea to pre-process the image with a median filter, which replaces each pixel value with the median value of all the pixels in a small (e.g., 7 pixel) neighborhood:

# convert to grayscale and apply median blur
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
img_blur = cv2.medianBlur(img_gray, 7)
Step 4: Create an edge mask using adaptive thresholding
After noise reduction it is safe to apply adaptive thresholding. Even if there is some image noise left, the cv2.ADAPTIVE_THRESH_MEAN_C algorithm with blockSize=9 will ensure that the threshold is applied to the mean of a 9x9 neighborhood minus C=2:

# detect and enhance edges
img_edge = cv2.adaptiveThreshold(img_blur, 255,
                                 cv2.ADAPTIVE_THRESH_MEAN_C,
                                 cv2.THRESH_BINARY,
                                 blockSize=9,
                                 C=2)
Step 5: Combine color image with edge mask
The last step is to combine the processed color image (img_color) with the edge mask (img_edge):

# convert back to color, bit-AND with color image
img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
img_cartoon = cv2.bitwise_and(img_color, img_edge)

# display
cv2.imshow("cartoon", img_cartoon)
The result looks like this:


The complete source code is available for free on GitHub (refer to the Cartoonizer class in the filters module). For a more detailed explanation, please refer to the book OpenCV with Python Blueprints.
