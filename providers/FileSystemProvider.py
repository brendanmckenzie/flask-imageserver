from BaseProvider import BaseProvider


class FileSystemProvider(BaseProvider):
    def __init__(self, root_path):
        self.root_path = root_path

    def get_fd(self, path):
        return open(self.root_path + '/' + path, 'r')
