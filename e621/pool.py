from concurrent.futures import ThreadPoolExecutor, as_completed

from pathvalidate import sanitize_filename


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

    def download_pool_post(self, i, post_id):
        post = self.e621.get_post(post_id)
        ext = post.data['file']['ext']
        md5 = post.data['file']['md5']
        url = post.data['file']['url']
        file_name = '{:03d}_{}.{}'.format(i, md5, ext)
        pool_post_path = self.path / file_name

        if not pool_post_path.exists():
            if url:
                print('Downloading:', url)
                response = self.e621.session.get(url)
                response.raise_for_status()
                pool_post_path.write_bytes(response.content)
            else:
                print('No URL for post:', post_id)
        else:
            print('Already downloaded:', pool_post_path)
        return post

    def download(self, num_threads=3):
        self.path.mkdir(parents=True, exist_ok=True)
        post_ids = self.data['post_ids']
        print('Post IDs:', post_ids)

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            n = 0
            for future in as_completed([
                executor.submit(self.download_pool_post, i, post_id)
                for i, post_id in enumerate(post_ids)
            ]):
                future.result()
                n += 1
                print(f'Downloaded {n}/{len(post_ids)}')
