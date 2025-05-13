1. Create a mesh file from the ios scan of the patient

2. Create an image of the mesh file. One patient generates 2 image files, with each image consisting of 3 angles of the teeth left/middle/right where one image is upper and the other lower

3. We take these 2 images and create 6 images from them. We need to use 4 of them: left/right and upper/lower

4. Each of these 4 images have a dimension of 1024x1024 and they all face the same direction. Along with this all the "left" images get their coordinates flipped to match their new angle

5. load the trained model

6. Run the model on the 4 images, and get an estimate for the 4 keypoints

7. Run the pixel matrix to fine tune the location of the 4 keypoints

8. Classify the degree of overbite

