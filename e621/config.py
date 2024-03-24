
import yaml
import base64
from pathlib import Path

from .util.ratelimitedsession import RateLimitedSession
from .util.ratelimiter import RateLimiter


class Config:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        with config_file_path.open('r') as file:
            self.data = yaml.safe_load(file)
        self.cache_dir = self.config_file_path.parent / self.data['cache_dir']

    def start_session(self):
        login = self.data['login']
        api_key = self.data['api_key']
        print('Using login:', login)

        # Prepare the Basic Auth value
        credentials = login + ':' + api_key
        credentials_bytes = credentials.encode('ascii')
        base64_credentials = base64.b64encode(credentials_bytes).decode('ascii')
        auth_header = f"Basic {base64_credentials}"

        # Initialize a session object
        max_requests_per_second = int(self.data.get('max_requests_per_second', '2'))
        session = RateLimitedSession(RateLimiter(max_requests_per_second))

        # Add Authorization and User-Agent headers to every request made with this session
        user_agent = self.data['user_agent']
        session.headers.update({
            'Authorization': auth_header,
            'User-Agent': user_agent
        })

        return session
