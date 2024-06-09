from concurrent.futures import ThreadPoolExecutor, as_completed

from pathvalidate import sanitize_filename

from .post import Post

class Pool:
    def __init__(self, e621, pool_id, data):
        self.e621 = e621
        self.pool_id = pool_id
        self.data = data
        self.path = self.e621.pools_dir / self.get_pool_dir_name()

    def get_pool_dir_name(self):
        pool_dir_name = '{}_{}'.format(self.pool_id, self.data['name'])
        pool_dir_name = sanitize_filename(pool_dir_name)
        return pool_dir_name

    def download_pool_post(self, i, post_id, ignore_post_age):
        post = self.e621.get_post(post_id, ignore_age=ignore_post_age)
        pool_post_path = self.path / f'{i:03d}_{post.get_filename()}'
        post.download(post_path=pool_post_path)
        return post

    def download(self, num_threads=3, ignore_post_age=False):
        self.path.mkdir(parents=True, exist_ok=True)
        post_ids = self.data['post_ids']
        print('Post IDs:', post_ids)

        posts = []
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            n = 0
            for future in as_completed([
                executor.submit(self.download_pool_post, i, post_id, ignore_post_age)
                for i, post_id in enumerate(post_ids)
            ]):
                post = future.result()
                n += 1
                print(f'Downloaded {post.post_id} - {n}/{len(post_ids)}')
        
        Post.download_many(posts, num_threads=num_threads, ignore_post_age=ignore_post_age)
