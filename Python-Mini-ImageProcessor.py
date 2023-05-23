import argparse
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter as tk
import time


# Applies a threshold filter to the image
def threshold(image, threshold_value):
    img = image.copy()
    for x in range(img.width):
        for y in range(img.height):
            r, g, b = img.getpixel((x, y))
            if r < threshold_value or g < threshold_value or b < threshold_value:
                img.putpixel((x, y), (0, 0, 0))
            else:
                img.putpixel((x, y), (255, 255, 255))
    return img


# Modifies the brightness of the image
def brightness(image, brightness_value):
    img = image.copy()
    for x in range(img.width):
        for y in range(img.height):
            r, g, b = img.getpixel((x, y))

            # Multiplies each pixel value with the parameter value
            new_r = int(r * brightness_value)
            new_g = int(g * brightness_value)
            new_b = int(b * brightness_value)

            # Clamps the values to range 0-255
            new_r = min(255, max(0, new_r))
            new_g = min(255, max(0, new_g))
            new_b = min(255, max(0, new_b))
            img.putpixel((x, y), (new_r, new_g, new_b))
    return img


# Modifies the brightness of the image (Individual RGB brightness values)
def brightness_independent_rgb(image, brightness_value_r, brightness_value_g, brightness_value_b):
    img = image.copy()
    for x in range(img.width):
        for y in range(img.height):
            r, g, b = img.getpixel((x, y))

            # Multiplies each pixel value with the corresponding parameter value
            new_r = int(r * brightness_value_r)
            new_g = int(g * brightness_value_g)
            new_b = int(b * brightness_value_b)
            # Clamps the values to range 0-255
            new_r = min(255, max(0, new_r))
            new_g = min(255, max(0, new_g))
            new_b = min(255, max(0, new_b))
            img.putpixel((x, y), (new_r, new_g, new_b))
    return img


# Modifies the contrast of the image
def contrast(image, contrast_value):
    img = image.copy()

    for x in range(img.width):
        for y in range(img.height):
            pixel = img.getpixel((x, y))

            # Subtracts 128 from the pixel values and multiplies them with the factor parameter value
            new_r = int((pixel[0] - 128) * contrast_value + 128)
            new_g = int((pixel[1] - 128) * contrast_value + 128)
            new_b = int((pixel[2] - 128) * contrast_value + 128)
            # Clamps the values to range 0-255
            new_r = min(255, max(0, new_r))
            new_g = min(255, max(0, new_g))
            new_b = min(255, max(0, new_b))

            # Updates the pixels
            img.putpixel((x, y), (new_r, new_g, new_b))
    return img


# Blurs the image
def blur(image, blur_value):
    img = image.copy()

    # Creates a kernel with the size of 2 * radius + 1
    kernel_size = 2 * blur_value + 1
    kernel = []
    for i in range(kernel_size):
        row = []
        for j in range(kernel_size):
            value = 1 / (kernel_size ** 2)
            row.append(value)
        kernel.append(row)

    # Creates a bordered image with 0 values around the image for when kernel is at edge
    bordered_img = Image.new("RGB", (img.width + 2 * blur_value, img.height + 2 * blur_value))
    bordered_img.paste(img, (blur_value, blur_value))

    # Applies kernel to each pixel in the image and updates the pixel values
    for x in range(blur_value, img.width + blur_value):
        for y in range(blur_value, img.height + blur_value):
            pixel_sum = [0, 0, 0]
            for i in range(kernel_size):
                for j in range(kernel_size):
                    pixel = bordered_img.getpixel((x + i - blur_value, y + j - blur_value))
                    pixel_sum[0] += pixel[0] * kernel[i][j]
                    pixel_sum[1] += pixel[1] * kernel[i][j]
                    pixel_sum[2] += pixel[2] * kernel[i][j]
            new_pixel = tuple(int(channel) for channel in pixel_sum)
            img.putpixel((x - blur_value, y - blur_value), new_pixel)

    return img


# Sharpens the image
def sharpen(image, sharpen_value):
    img = image.copy()

    # Creates a kernel with the size of 2 * sharpen_value + 1
    kernel_size = 2 * sharpen_value + 1
    kernel = [[-1 / (kernel_size ** 2) for _ in range(kernel_size)] for _ in range(kernel_size)]
    kernel[sharpen_value][sharpen_value] = 1 + (kernel_size ** 2 - 1) / (kernel_size ** 2)

    # Creates a bordered image for when kernel is at edge
    bordered_img = Image.new("RGB", (img.width + 2 * sharpen_value, img.height + 2 * sharpen_value))
    bordered_img.paste(img, (sharpen_value, sharpen_value))

    # Applies kernel to each pixel in the image and updates the pixel values
    for x in range(sharpen_value, img.width + sharpen_value):
        for y in range(sharpen_value, img.height + sharpen_value):
            pixel_sum = [0, 0, 0]
            for i in range(kernel_size):
                for j in range(kernel_size):
                    pixel = bordered_img.getpixel((x + i - sharpen_value, y + j - sharpen_value))
                    pixel_sum[0] += pixel[0] * kernel[i][j]
                    pixel_sum[1] += pixel[1] * kernel[i][j]
                    pixel_sum[2] += pixel[2] * kernel[i][j]
            new_pixel = tuple(int(channel) for channel in pixel_sum)
            img.putpixel((x - sharpen_value, y - sharpen_value), new_pixel)

    return img


# Erodes or dilates the image
def erode_dilate(image, kernel_size, operation):
    img = image.copy()
    kernel_radius = kernel_size // 2

    # Creates a bordered image for when kernel is at edge
    bordered_img = Image.new("RGB", (img.width + 2 * kernel_radius, img.height + 2 * kernel_radius))
    bordered_img.paste(img, (kernel_radius, kernel_radius))

    # Applies kernel to each pixel in the image and updates the pixel values
    for x in range(kernel_radius, img.width + kernel_radius):
        for y in range(kernel_radius, img.height + kernel_radius):
            pixels = []
            for i in range(kernel_size):
                for j in range(kernel_size):
                    pixel = bordered_img.getpixel((x + i - kernel_radius, y + j - kernel_radius))
                    pixels.append(pixel)
            if operation == "erode":
                new_pixel = min(pixels)
            elif operation == "dilate":
                new_pixel = max(pixels)
            else:
                raise print("Operation must be \"erode\" or \"dilate\"")
            img.putpixel((x - kernel_radius, y - kernel_radius), new_pixel)

    return img


# Detects edges in the image
def edge_detection(image):
    img = image.copy().convert("L")

    # Sobel kernels
    kernel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    kernel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    # Creates a bordered image for when kernel is at edge
    bordered_img = Image.new("L", (img.width + 2, img.height + 2))
    bordered_img.paste(img, (1, 1))

    # Applies kernel to each pixel in the image and updates the pixel values
    for x in range(1, img.width + 1):
        for y in range(1, img.height + 1):
            pixel_sum_x = 0
            pixel_sum_y = 0
            for i in range(3):
                for j in range(3):
                    pixel = bordered_img.getpixel((x + i - 1, y + j - 1))
                    pixel_sum_x += pixel * kernel_x[i][j]
                    pixel_sum_y += pixel * kernel_y[i][j]
            new_pixel = int((pixel_sum_x ** 2 + pixel_sum_y ** 2) ** 0.5)
            # Clamps the values to range 0-255
            new_pixel = min(255, max(0, new_pixel))
            img.putpixel((x - 1, y - 1), new_pixel)

    return img


# [Extra] Mirrors the image
def mirror(image, side):
    img = image.copy()
    width, height = img.size
    if side == "left":
        for y in range(height):
            for x in range(width // 2, width):
                left_pixel = img.getpixel((width - x - 1, y))
                img.putpixel((x, y), left_pixel)
    elif side == "right":
        for y in range(height):
            for x in range(width // 2):
                right_pixel = img.getpixel((width - x - 1, y))
                img.putpixel((x, y), right_pixel)
    else:
        raise argparse.ArgumentTypeError("Mirror value must be \"left\" or \"right\"")
    return img


# Helper methods #
# Checks if an image was given as an argument, displays a file explorer selection dialog if not
def image_provided_check(args):
    if args.image:
        img_path = args.image
    else:
        # Displays a file explorer selection dialog
        img_path = filedialog.askopenfilename(title="Select an image to process")

    return img_path


# Prints the time it took to generate the processed image
def print_elapsed_time(start_time):
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time it took to generate the processed image: {elapsed_time:.2f} seconds")


# parse tuple for argparse argument
def tuple_args(string):
    try:
        string = string.replace(" ", "")
        return tuple(map(float, string.split(",")))
    except ValueError:
        raise argparse.ArgumentTypeError("Tuple must be comma seperated float values. "
                                         "Tuple format example: 1.1,1.4,2.1")


# Parses the command line arguments
def argparse_parsing(args, img_path):
    # Loads the image using the Image module of the PIL library
    img = Image.open(img_path)
    processed_img = img

    # Processes the image according to the given arguments
    if args.threshold is not None:
        processed_img = threshold(img, args.threshold)
    if args.brightness != 1.0:
        processed_img = brightness(processed_img, args.brightness)
    if args.brightness_independent_rgb is not None:
        processed_img = brightness_independent_rgb(processed_img, args.brightness_rgb[0], args.brightness_rgb[1],
                                                   args.brightness_rgb[2])
    if args.contrast != 1.0:
        processed_img = contrast(processed_img, args.contrast)
    if args.blur is not None:
        processed_img = blur(processed_img, args.blur)
    if args.sharpen is not None:
        processed_img = sharpen(processed_img, args.sharpen)
    if args.erode is not None:
        processed_img = erode_dilate(processed_img, args.erode, "erode")
    if args.dilate is not None:
        processed_img = erode_dilate(processed_img, args.dilate, "dilate")
    if args.edge_detection is not False:
        processed_img = edge_detection(processed_img)
    if args.mirror is not None:
        processed_img = mirror(processed_img, args.mirror)

    return processed_img


def add_parse_arguments():
    parser = argparse.ArgumentParser(usage="\nTo apply filters to an image, input the absolute path of the image \n"
                                           "you want to modify or just the name of the image (including file ending) \n"
                                           "it is in the same directory as the script. If no arguments are given, \n"
                                           "you can select the image via the File Explorer Popup. To apply filters \n"
                                           "you can either use the GUI or use the console with the attributes \n"
                                           "listed below.")
    parser.add_argument("--threshold", help="Applies a threshold filter to the image. (float)", type=int)
    parser.add_argument("--brightness", help="Applies a brightness filter to the image. (float)", type=float,
                        default=1.0)
    parser.add_argument("--brightness_independent_rgb", type=tuple_args,
                        help="Applies a brightness filter to the individual color channels of the image. "
                             "(tuple) Example tuple: 1.1, 1.4, 2.1")
    parser.add_argument("--contrast", help="Applies a contrast filter to the image. (float)", type=float, default=1.0)
    parser.add_argument("--blur", help="Applies a blur filter to the image. (int)", type=int, default=None)
    parser.add_argument("--sharpen", help="Applies a sharpening filter to the image. (int)", type=int, default=None)
    parser.add_argument("--erode", help="Applies an erode filter to the image. (int)", type=int, default=None)
    parser.add_argument("--dilate", help="Applies a dilate filter to the image. (int)", type=int, default=None)
    parser.add_argument("--edge_detection", help="Applies an edge detection filter to the image.", default=False)
    parser.add_argument("--mirror", help="Mirrors the image. (left/right)", choices=["left", "right"], default=None)
    parser.add_argument("image", help="The image to process.", nargs="?")
    # (nargs="?") means that the argument is optional
    args = parser.parse_args()
    return args


# Sets up the Tkinter window and displays the processed image
def tkinter_setup(original_img=None, processed_img=None):
    original_image = original_img.copy()
    processed_img = processed_img.copy()

    def apply_filter():
        nonlocal processed_img
        filter_name = filter_var.get()
        filter_value = value_entry.get()
        print(f"Applying filter: {filter_name} with value: {filter_value}")
        # Records the time when the filter is applied
        start_time = time.time()
        # Applies the selected filter to the image
        if filter_name == "threshold":
            if filter_value == "" or int(filter_value) < 0 or int(filter_value) > 255:
                print("Error: Threshold value must be between 0 and 255")
            else:
                processed_img = threshold(processed_img, int(filter_value))
        elif filter_name == "brightness":
            if filter_value == "":
                print("Error: No value input.")
            else:
                processed_img = brightness(processed_img, float(filter_value))
        elif filter_name == "brightness_independent_rgb":
            if filter_value == "":
                print("Error: No value input.")
            else:
                r, g, b = tuple_args(filter_value)
                processed_img = brightness_independent_rgb(processed_img, r, g, b)
        elif filter_name == "contrast":
            if filter_value == "":
                print("Error: No value input.")
            else:
                processed_img = contrast(processed_img, float(filter_value))
        elif filter_name == "blur":
            if filter_value == "" or int(filter_value) < 0:
                print("Error: Blur value must be greater than 0")
            else:
                processed_img = blur(processed_img, int(filter_value))
        elif filter_name == "sharpen":
            if filter_value == "" or int(filter_value) < 0:
                print("Error: Sharpen value must be greater than 0")
            else:
                processed_img = sharpen(processed_img, int(filter_value))
        elif filter_name == "erode":
            if filter_value == "" or int(filter_value) < 0:
                print("Error: Erode value must be greater than 0")
            else:
                processed_img = erode_dilate(processed_img, int(filter_value), "erode")
        elif filter_name == "dilate":
            if filter_value == "" or int(filter_value) < 0:
                print("Error: Dilate value must be greater than 0")
            else:
                processed_img = erode_dilate(processed_img, int(filter_value), "dilate")
        elif filter_name == "edge_detection":
            processed_img = edge_detection(processed_img)
        elif filter_name == "mirror":
            processed_img = mirror(processed_img, filter_value)

        # Records the time the operation took to complete
        end_time = time.time()
        # Calculates and prints the elapsed time it took to generate the processed image
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")

        # Updates the displayed image
        photo = ImageTk.PhotoImage(processed_img)
        label.config(image=photo)
        label.image = photo

    # Resets the processed image to its original state
    def reset_image():
        nonlocal processed_img
        processed_img = original_image.copy()
        # Updates the displayed image
        photo = ImageTk.PhotoImage(original_image)
        label.config(image=photo)
        label.image = photo

    # Saves the processed image
    def save_image():
        nonlocal processed_img
        processed_img.save("processed_image.jpg")
        print("Image saved as processed_image.jpg")

    def open_popup():
        top = tk.Toplevel()
        top.geometry("350x850")
        top.title("Help")
        top.attributes("-topmost", True)
        tk.Label(top, text="\bUsage:\b\n\nTo apply filters to an image, input the absolute path of the image"
                           "you want to modify or just the name of the image (including file ending)"
                           "if it is in the same directory as the script. If no arguments are given,"
                           "you can select the image via the File Explorer Popup. To apply filters"
                           "you can either use the GUI or use the console with the attributes"
                           "listed below.\n\n"
                           "\bpositional arguments:\b\n"
                           "image\n"
                           "The image to process.\n\n"
                           "\boptions:\b\n"
                           "-h, --help\n"
                           "Shows available filters/arguments. \n\n"
                           "--threshold THRESHOLD\n"
                           "Applies a threshold filter to the image. (float)\n"
                           "--brightness BRIGHTNESS\n"
                           "Applies a brightness filter to the image. (float)\n\n"
                           "--brightness_independent_rgb BRIGHTNESS_INDEPENDENT_RGB\n"
                           "Applies a brightness filter to the individual color"
                           "channels of the image. (tuple) Example tuple: 1.1,"
                           "1.4, 2.1\n\n"
                           "--contrast CONTRAST"
                           "\nApplies a contrast filter to the image. (float)\n\n"
                           "--blur BLUR"
                           "\nApplies a blur filter to the image. (int)\n\n"
                           "--sharpen SHARPEN"
                           "\nApplies a sharpening filter to the image. (int)\n\n"
                           "--erode ERODE"
                           "\nApplies an erode filter to the image. (int)\n\n"
                           "--dilate DILATE"
                           "\nApplies a dilate filter to the image. (int)\n\n"
                           "--edge_detection EDGE_DETECTION"
                           "\nApplies an edge detection filter to the image.\n\n"
                           "--mirror {left,right}"
                           "\nMirrors the image. (left/right)", wraplength=290, anchor='w', justify='left').pack()

    # Sets the maximum size of the image to 500x500 pixels
    max_size = (500, 500)
    processed_img.thumbnail(max_size)

    # Displays the image in a Tkinter window
    tkinter_root = tk.Tk()
    tkinter_root.title("Image Processing")
    tkinter_root.attributes("-topmost", True)
    tkinter_root.configure(background="white")

    filter_label = tk.Label(tkinter_root, text="Filter:")
    filter_label.pack()

    filter_var = tk.StringVar(tkinter_root)
    filter_var.set("threshold")  # default value

    filter_options = ["threshold", "brightness", "brightness_independent_rgb", "contrast",
                      "blur", "sharpen", "erode", "dilate", "edge_detection", "mirror"]
    filter_menu = tk.OptionMenu(tkinter_root, filter_var, *filter_options)
    filter_menu.pack()

    value_label = tk.Label(tkinter_root, text="Value:")
    value_label.pack()

    value_entry = tk.Entry(tkinter_root)
    value_entry.pack()

    apply_button = tk.Button(tkinter_root, text="Apply", command=apply_filter, height=1, width=10)
    apply_button.pack()

    reset_button = tk.Button(tkinter_root, text="Save", command=save_image, height=1, width=10)
    reset_button.pack()

    reset_button = tk.Button(tkinter_root, text="Reset", command=reset_image, height=1, width=10)
    reset_button.pack()

    help_button = tk.Button(tkinter_root, text="Help", command=lambda: open_popup(), height=1, width=10)
    help_button.pack()

    photo = ImageTk.PhotoImage(processed_img)
    label = tk.Label(tkinter_root, image=photo)
    label.pack(expand=True)

    tkinter_root.resizable(width=False, height=False)
    tkinter_root.mainloop()


def main():
    args = add_parse_arguments()
    # If an image path is given as an argument, the image is processed and displayed without showing the file explorer
    if args is not None:
        img_path = image_provided_check(args)
        original_img = Image.open(img_path)
        processed_img = argparse_parsing(args, img_path)
        tkinter_setup(original_img, processed_img)
    # If no image path is given as an argument, the file explorer is shown
    else:
        tkinter_setup()


if __name__ == "__main__":
    main()
