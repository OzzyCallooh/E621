from concurrent.futures import ThreadPoolExecutor, as_completed

class Post:
    def __init__(self, e621, post_id, data):
        self.e621 = e621
        self.post_id = post_id
        self.data = data

    def get_filename(self):
        ext = self.data['file']['ext']
        md5 = self.data['file']['md5']
        return '{}.{}'.format(md5, ext)

    def get_post_path(self):
        return self.e621.posts_dir / self.get_filename()

    def download(self, post_path=None, ignore_post_age=False):
        url = self.data['file']['url']
        if post_path is None:
            post_path = self.get_post_path()

        if not post_path.exists():
            if url:
                print('Downloading:', url)
                response = self.e621.session.get(url)
                response.raise_for_status()
                post_path.write_bytes(response.content)
            else:
                print('No URL for post:', self.post_id)
        else:
            print('Already downloaded:', post_path)

    @staticmethod
    def download_many(posts, num_threads=3, ignore_post_age=False):
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            n = 0
            for future in as_completed([
                executor.submit(Post.download, post, ignore_post_age=ignore_post_age)
                for post in posts
            ]):
                post = future.result()
                n += 1
                print(f'Downloaded {post.post_id} - {n}/{len(posts)}')
