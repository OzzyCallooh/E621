from requests.sessions import Session


class RateLimitedSession(Session):
    """
    A session class that implements rate limiting for requests.

    This class extends the `Session` class from the `requests` library and adds rate limiting functionality.
    It takes a `rate_limiter` object as a parameter, which is responsible for enforcing the rate limit.

    Usage:
    ```
    rate_limiter = RateLimiter()
    session = RateLimitedSession(rate_limiter)
    response = session.request('GET', 'https://example.com')
    ```

    Args:
        rate_limiter: An object that implements the `wait_for_token` method, which enforces the rate limit.

    Attributes:
        rate_limiter: The rate limiter object associated with the session.

    Methods:
        request: Overrides the `request` method of the `Session` class to enforce rate limiting before making the actual request.
    """
    def __init__(self, rate_limiter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rate_limiter = rate_limiter

    def request(self, method, url, *args, **kwargs):
        """
        Send a request with rate limiting.

        This method overrides the `request` method of the `Session` class to enforce rate limiting before making the actual request.

        Args:
            method: The HTTP method to use for the request (e.g., 'GET', 'POST', etc.).
            url: The URL to send the request to.
            *args: Additional positional arguments to pass to the `request` method.
            **kwargs: Additional keyword arguments to pass to the `request` method.

        Returns:
            The response object returned by the `request` method of the `Session` class.
        """
        # Call the rate limiter before making the actual request
        self.rate_limiter.wait_for_token()
        # Now proceed with the actual request
        return super().request(method, url, *args, **kwargs)
