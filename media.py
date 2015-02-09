import tempfile
import requests
from StringIO import StringIO
from PIL import Image
from flask import abort, send_file, request
from contain import process_contain
from crop import process_crop
from cover import process_cover

MAX_WIDTH, MAX_HEIGHT = 4000, 4000

S3_BUCKET = None


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

    with tempfile.NamedTemporaryFile(prefix='img-') as fd:
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
