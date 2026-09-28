# Exercises

Complete these in order. Use the scripts in `examples/` as references, but write the changes yourself first.

## Warm-up

1. Print the OpenCV version and confirm that NumPy imports.
2. Change the generated image dimensions and inspect the reported shape.
3. Save the generated image as a JPEG and compare its file size with PNG.

## Image operations

4. Add a grayscale output to `03_image_basics.py`.
5. Crop the center quarter of the image and save it.
6. Draw a diagonal line and a filled circle using different colors.
7. Apply median blur and Gaussian blur. Compare the results.
8. Detect edges with Canny and save the edge image.

## Reasoning checks

9. Why does `image.shape` list height before width?
10. Why can displaying a BGR image with an RGB-only library produce strange colors?
11. What assumptions make color thresholding fail outdoors?
12. For one use case in `REAL_WORLD_USE_CASES.md`, list two false-positive and two false-negative scenarios.

## Completion checkpoint

You are ready for the next lab when you can explain the input, transformation, output, and failure case for each of your programs without copying the answer from the library documentation.
