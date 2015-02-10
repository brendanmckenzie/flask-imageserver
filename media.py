import tempfile
import requests
from StringIO import StringIO
from PIL import Image
from flask import abort, send_file, request
import processors

MAX_WIDTH, MAX_HEIGHT = 4000, 4000


_processors = {
    'contain': processors.process_contain,
    'cover': processors.process_cover,
    'crop': processors.process_crop
}


def process(type, width, height, path, s3_bucket):
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

        if type in _processors:
            ret = _processors[type](img, width, height)

        if ret:
            quality = request.args.get('qual', 100)

            img_io = StringIO()
            ret.save(img_io, 'JPEG', quality=quality)
            img_io.seek(0)

            return send_file(img_io,
                             mimetype='image/jpeg',
                             cache_timeout=604800)
        else:
            abort(400)
