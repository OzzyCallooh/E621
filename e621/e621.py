import json
import time

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

    def cached_download(self, url, path, ignore_age=False):
        should_download = True
        result = None

        # Check if file exists and its age does not exceed self.config.data['stale_time'] seconds old
        if path.exists() and (ignore_age or path.stat().st_mtime + self.config.data['stale_time'] > time.time()):
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

    def get_cached_pools(self):
        pool_ids = []
        for pool_file in self.pools_dir.glob('pool_*.json'):
            pool_id = int(pool_file.stem[5:])
            pool_ids.append(pool_id)
        return pool_ids

    def get_pool(self, pool_id):
        pool_data = self.cached_download(
            'https://e621.net/pools/{}.json'.format(pool_id),
            self.pools_dir / 'pool_{}.json'.format(pool_id)
        )
        return Pool(self, pool_id, pool_data)

    def get_post(self, post_id, ignore_age=False):
        post_data = self.cached_download(
            'https://e621.net/posts/{}.json'.format(post_id),
            self.posts_dir / 'post_{}.json'.format(post_id),
            ignore_age=ignore_age
        )['post']
        return Post(self, post_id, post_data)
