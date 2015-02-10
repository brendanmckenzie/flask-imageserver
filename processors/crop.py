def process_crop(img, width, height):
    orig_width, orig_height = img.size

    orig_width = float(orig_width)
    orig_height = float(orig_height)
    width = float(width)
    height = float(height)

    if width > orig_width or height > orig_height:
        # can't upscale
        return None

    crop_x0 = int((orig_width / 2) - (width / 2))
    crop_x1 = int((orig_width / 2) + (width / 2))
    crop_y0 = int((orig_height / 2) - (height / 2))
    crop_y1 = int((orig_height / 2) + (height / 2))

    return img.crop((crop_x0, crop_y0, crop_x1, crop_y1))
