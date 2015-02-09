import tempfile
import requests
from StringIO import StringIO
from PIL import Image
from flask import abort, send_file, request
from contain import process_contain
from crop import process_crop
from cover import process_cover

MAX_WIDTH, MAX_HEIGHT = 4000, 4000


def process(type, width, height, path, s3_bucket):
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
        url = 'https://s3.amazonaws.com/%s/%s' % (s3_bucket, path, )
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
