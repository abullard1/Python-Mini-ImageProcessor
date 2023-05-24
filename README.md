# Python-Mini-ImageProcessor
A small and simple python image processor to apply, view and save a variety of different custom image filters like threshold, brightness, 
contrast, blur, sharpen, dilate, erode, edge detection and mirror. Modified images can also be saved. Can also be used using command line arguments. 
This project was part of some of my university coursework.

## Usage
To use the program first mage sure that you have python installed. The easiest way to download python would be to download it from the Microsoft Store. The program was made
using Python 3.10. Lower versions have not been tested and might or might not work. Also make sure to have the python packages PIL (pillow) and tk (tkinter) installed.
To do this, simply open cmd.exe and type "pip install tk pillow". The necessary packages will then be downloaded and installed.
You can either run the program by using your command line or by running it using an IDE like Pycharm. To use the program via the command line (e.g. cmd.exe), navigate to the 
folder where the "Python-Mini-ImageProcessory.py" script is located by typing "cd [Absolute Path to folder in which Python-Mini-ImageProcessory.py is located]. 
After that, type "python Python-Mini-ImageProcessory.py [Optional: --contrast 2 --blur 2 etc.] [Optional: Absolute Path to image you want to modify or name of image if it
is located in the same directory of the script].
Example 1: python Python-Mini-ImageProcessory.py --blur 2  --contrast 3 --brightness 2 example_image.jpg
For a list of command line arguments use the argument --help.
If no image path or name is given, a file explorer window will open where you can select the image file to modify. After pressing enter, a GUI will open up where you can
see the changes made to the image via the command line arguments (if you input any) and make further changes, reset the changes, save the image or view all possible command line arguments.

###Showcase

<table>
  <tr>
    <td><kbd> <img src="Image Processing Pre.png" width="500" /> </kbd></td>
    <td><kbd> <img src="Image Processing Post.png" width="500" /> </kbd></td>
  </tr>
</table>
