import tempfile
import requests
from StringIO import StringIO
from PIL import Image
from flask import abort, send_file, request

MAX_WIDTH, MAX_HEIGHT = 4000, 4000

S3_BUCKET = None


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


def process(type, width, height, path):
    processors = {
        'contain': process_contain,
        'cover': process_cover,
        'crop': process_crop
    }

    # sanitise...
    if width > MAX_WIDTH:
        width = MAX_WIDTH
    if height > MAX_HEIGHT:
        height = MAX_HEIGHT

    with tempfile.NamedTemporaryFile(prefix='img-', delete=True) as fd:
        url = 'https://s3.amazonaws.com/%s/%s' % (S3_BUCKET, path, )
        resp = requests.get(url, stream=True)

        if not resp.ok:
            abort(404)

        for block in resp.iter_content(1024):
            if not block:
                break

            fd.write(block)

        fd.seek(0)

        img = Image.open(fd)
        ret = None

        if type in processors:
            ret = processors[type](img, width, height)

        if ret:
            img_io = StringIO()
            ret.save(img_io, 'JPEG', quality=request.args.get('qual', 100))
            img_io.seek(0)

            return send_file(img_io, mimetype='image/jpeg', cache_timeout=604800)
        else:
            abort(400)


def init_imageserver(app, s3_bucket):
    global S3_BUCKET
    S3_BUCKET = s3_bucket

    @app.route('/media/w<int:width>/h<int:height>/for/<path:path>')
    def contain_both(width, height, path):
        return process('contain', width, height, path)

    @app.route('/media/w<int:width>/for/<path:path>')
    def contain_width(width, path):
        return process('contain', width, None, path)

    @app.route('/media/h<int:height>/for/<path:path>')
    def contain_height(height, path):
        return process('contain', None, height, path)

    @app.route('/media/cover/w<int:width>/h<int:height>/for/<path:path>')
    def cover(width, height, path):
        return process('cover', width, height, path)

    @app.route('/media/crop/w<int:width>/h<int:height>/for/<path:path>')
    def crop(width, height, path):
        return process('crop', width, height, path)
