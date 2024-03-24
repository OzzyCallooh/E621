# E621 by Ozzy Callooh

This Python project is an e621 pool downloader.

```bash
# Download "The Internship" series by Jackaloo (436 posts, about 375 MB)
$ python -m e621 download-pool 933 13890 20420 32083 13092 16422 25947 29589
# Use --help for more info at any time.
$ python -m e621 --help
```

## Configuration

Create a copy of [sample_config.yaml](sample_config.yaml) as **config.yaml**. Fill out the fields, including your API key.

### Authentication: `login`, `api_key`

To run this tool, you may need an API key. Here's how you can get one:

1. [Log in](https://e621.net/session/new) to your E621 account.
2. Navigate to [Account](https://e621.net/users/home) &rarr; **Manage API Access**
3. Input your password again.
4. Upon viewing this page, an API key will have been generated for you, if one was not already. You can choose to regenerate or delete it.

For more information, see [Help: API](https://e621.net/help/api) on the E621 Wiki.
