import json

from .post import Post
from .pool import Pool

DEFAULT_USER_AGENT = 'E621 by OzzyCallooh'


class E621:
    def __init__(self, config):
        self.config = config
        self.session = config.start_session()
        self.config.cache_dir.mkdir(exist_ok=True)
        self.pools_dir = self.config.cache_dir / 'pools'
        self.pools_dir.mkdir(exist_ok=True)
        self.posts_dir = self.config.cache_dir / 'posts'
        self.posts_dir.mkdir(exist_ok=True)

    def cached_download(self, url, path):
        should_download = True
        result = None
        if path.exists():
            print('Using cached file:', path)
            try:
                result = json.loads(path.read_text(encoding='utf-8'))
                should_download = False
            except Exception as e:
                print('Error reading cached file:', path)
                print(e)
                should_download = True

        if should_download:
            print('Downloading:', url)
            response = self.session.get(
                url)
            response.raise_for_status()
            path.write_text(response.text, encoding='utf-8')
            result = response.json()

        return result

    def get_pool(self, pool_id):
        pool_data = self.cached_download(
            'https://e621.net/pools/{}.json'.format(pool_id),
            self.pools_dir / 'pool_{}.json'.format(pool_id)
        )
        return Pool(self, pool_id, pool_data)

    def get_post(self, post_id):
        post_data = self.cached_download(
            'https://e621.net/posts/{}.json'.format(post_id),
            self.posts_dir / 'post_{}.json'.format(post_id)
        )['post']
        return Post(self, post_id, post_data)
