# flask-imageserver
Simple image server for manipulating S3 stored images

```python
from my_app import app
from imageserver import init_imageserver

init_imageserver(app, s3_bucket='bucket-name')

app.run()
```

This provides the following routes.

* `/media/w<int:width>/h<int:height>/for/<path:path>`
* `/media/w<int:width>/for/<path:path>`
* `/media/h<int:height>/for/<path:path>`
* `/media/cover/w<int:width>/h<int:height>/for/<path:path>`
* `/media/crop/w<int:width>/h<int:height>/for/<path:path>`

Where:

* `width` is the desired output width
* `height` is the desired output height
* `path` is the path to the object within the S3 bucket

The available transformations are:

* `contain` returns an image for the input width/height with no surrounding whitespace maintaining the aspect ratio
* `cover` returns an image whose sizes are exactly the ones specified. The original image is scaled down to cover entirely the specified area and then the exceding parte of the image are "cut out" to fit the new aspect ratio
* `crop` returns an image whose sizes are exactly the ones specified. The reduced image is obtained picking it from a rectangle of the same sizes from the center of the image
