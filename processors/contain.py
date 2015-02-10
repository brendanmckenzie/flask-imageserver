from PIL import Image


def process_contain(img, width, height):
    orig_width, orig_height = img.size

    orig_width = float(orig_width)
    orig_height = float(orig_height)

    if width and height:
        width = float(width)
        height = float(height)

        height_by_width = width * orig_height / orig_width
        width_by_height = orig_width / orig_height * height

        if height_by_width > height:
            width = width_by_height
        else:
            height = height_by_width
    elif width:
        width = float(width)
        height = width * orig_height / orig_width
    elif height:
        height = float(height)
        width = orig_width / orig_height * height

    new_size = int(width), int(height)

    return img.resize(new_size, Image.ANTIALIAS)
