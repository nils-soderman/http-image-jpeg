# http-image.jpeg
A free addon for Blender which allows you to download &amp; open images by providing the image address/url.
The addon will download the image and pack it into the current blend file.

The reason I created this addon was because it always bugged me whenever I needed to get a reference image into Blender, how I first had do save the image on my hard drive, to then drag the image into Blender. I wanted to be able to just take it directly into Blender without having to take that extra step of saving it first. And so this addon was born.


# How to use it:

1. Copy the image adress for any image you want to import. You can normally do this by right clicking the image then chose "Copy image address"
2. Open Blender and press bring up the search menu (spacebar)
3. Type in the keyword url, and you'll see the function "Image: Open Image from URL - (http://image.jpeg)"
4. Click the function or press enter.
5. You'll be prompted to enter the image adress, the addon will automatically paste in whatever is in your clipboard, so if you copied the url before running this function, just hit enter/OK and you're done, the image is now in the .blend file. (If you did not copy the image adress before, just copy it now, enter it and press OK)

The function can also be called from the menu in the UV/Image Editor: Image > Open Image from URL

# Note:
The function is context sensitive, meaning that it will do different operations depending on which area of blender you import the image from.

3D View:
If you call this function from the 3D view, it will apply the image as a background image.

Node Editor:
If you call this function from the Node Editor, it will create an image node if possible.

Image Editor:
If you call this function from the Image Editor, it will set the image as active image.


# User Preferences:
If you look under the user preferences of the addon there is a few settings you can make.

#### Save images on drive: 
The images you open will be saved on your hard drive, if this is not enabled they will instead only be packed into the open blend file.

#### Pack images:
Pack the images into the open blend file


### Updater Settings:
This addon makes use of the Blender addon updater by Patrick W. Crawford
https://github.com/CGCookie/blender-addon-updater

This allows you to easily keep the addon up to date, in here you can turn on auto check for update or just manually check for updates from time to time.
