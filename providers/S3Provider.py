from BaseProvider import BaseProvider
import tempfile
import requests


class S3SystemProvider(BaseProvider):
    def __init__(self, s3_bucket):
        self.s3_bucket = s3_bucket

    def get_fd(self, path):
        with tempfile.NamedTemporaryFile(prefix='img-') as fd:
            url = 'https://s3.amazonaws.com/%s/%s' % (self.s3_bucket, path, )
            resp = requests.get(url, stream=True)

            if not resp.ok:
                return

            for block in resp.iter_content(1024):
                if not block:
                    break

                fd.write(block)

            fd.seek(0)

            return fd
