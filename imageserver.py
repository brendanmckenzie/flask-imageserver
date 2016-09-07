from media import process


def init_imageserver(app, root_path):
    @app.route('/media/w<int:width>/h<int:height>/for/<path:path>')
    def contain_both(width, height, path):
        return process('contain', width, height, path, root_path)

    @app.route('/media/w<int:width>/for/<path:path>')
    def contain_width(width, path):
        return process('contain', width, None, path, root_path)

    @app.route('/media/h<int:height>/for/<path:path>')
    def contain_height(height, path):
        return process('contain', None, height, path, root_path)

    @app.route('/media/cover/w<int:width>/h<int:height>/for/<path:path>')
    def cover(width, height, path):
        return process('cover', width, height, path, root_path)

    @app.route('/media/crop/w<int:width>/h<int:height>/for/<path:path>')
    def crop(width, height, path):
        return process('crop', width, height, path, root_path)
