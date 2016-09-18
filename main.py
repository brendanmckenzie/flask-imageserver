from flask import Flask
from imageserver import init_imageserver
import os
from providers import FileSystemProvider

app = Flask(__name__)

init_imageserver(app, provider=FileSystemProvider(os.getenv('MEDIA_ROOT')))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
