import threading
import time

from queue import Queue

class RateLimiter:
    """
    A rate limiter that limits the number of requests per second.

    Args:
        rate_limit_per_sec (int): The maximum number of requests allowed per second.

    Attributes:
        rate_limit_per_sec (int): The maximum number of requests allowed per second.
        lock (threading.Lock): A lock to ensure thread safety.
        timestamps (Queue): A queue to store the timestamps of requests.

    Methods:
        wait_for_token: Waits for a token to be available before proceeding with the request.
    """

    def __init__(self, rate_limit_per_sec):
        self.rate_limit_per_sec = rate_limit_per_sec
        self.lock = threading.Lock()
        self.timestamps = Queue(maxsize=rate_limit_per_sec)

    def wait_for_token(self):
        """
        Waits for a token to be available before proceeding with the request.
        If the rate limit has been reached, this method will block until a token becomes available.
        """
        with self.lock:
            now = time.time()
            while not self.timestamps.empty():
                # If the oldest timestamp is within the rate limit window, wait
                if now - self.timestamps.queue[0] < 1.0 / self.rate_limit_per_sec:
                    time.sleep((1.0 / self.rate_limit_per_sec) -
                               (now - self.timestamps.queue[0]))
                    now = time.time()
                else:
                    break
            # Update the timestamps queue
            if self.timestamps.full():
                self.timestamps.get()
            self.timestamps.put(now)


def make_request(url, rate_limiter):
    rate_limiter.wait_for_token()
    # Perform the request here
    # response = requests.get(url)
    print(f"Request to {url} at {time.time()}")


if __name__ == '__main__':

    rate_limiter = RateLimiter(2)  # 2 requests per second

    # Example usage with threads
    threads = []
    for i in range(10):  # Let's say we want to make 10 requests
        t = threading.Thread(target=make_request, args=(
            f"http://example.com/{i}", rate_limiter))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
