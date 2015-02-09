def process_cover(img, width, height):
    orig_width, orig_height = img.size

    orig_width = float(orig_width)
    orig_height = float(orig_height)
    width = float(width)
    height = float(height)
    dest_width = width
    dest_height = height

    if width > orig_width or height > orig_height:
        # can't upscale
        return None

    # 1. resize
    if orig_width > orig_height:
        dest_height = dest_width * orig_height / orig_width
    else:
        dest_width = orig_width / orig_height * dest_height

    new_size = int(dest_width), int(dest_height)

    resized = img.resize(new_size, Image.ANTIALIAS)

    # 2. crop
    crop_x0 = int((dest_width / 2) - (width / 2))
    crop_x1 = int((dest_width / 2) + (width / 2))
    crop_y0 = int((dest_height / 2) - (height / 2))
    crop_y1 = int((dest_height / 2) + (height / 2))

    return resized.crop((crop_x0, crop_y0, crop_x1, crop_y1))
