import click
from pathlib import Path

from .e621 import E621
from .config import Config
from .gui import main as guimain

@click.group
@click.option('-c', '--config', 'config_file_path', type=click.Path(exists=True), default=Path('config.yaml'))
@click.pass_context
def cli(ctx, config_file_path):
    ctx.ensure_object(dict)
    config = Config(config_file_path)
    ctx.obj['e621'] = E621(config)

@cli.command
def gui():
    guimain()

# download search command:
@cli.command
@click.argument('query')
@click.option('-t', '--threads', 'num_threads', type=int, default=3)
@click.option('-l', '--limit', 'limit', type=int, default=20)
@click.pass_context
def download_search(ctx, query, num_threads, limit):
    e621 = ctx.obj['e621']
    e621.download_search(query, limit)

@cli.command
@click.argument('pool_ids', type=int, nargs=-1)
@click.option('-t', '--threads', 'num_threads', type=int, default=3)
@click.pass_context
def download_pool(ctx, pool_ids, num_threads):
    e621 = ctx.obj['e621']
    pools = [ e621.get_pool(pool_id) for pool_id in pool_ids ]
    for pool in pools:
        pool.download(num_threads)

@cli.command
@click.argument('pool_ids', type=int, nargs=-1)
@click.option('-t', '--threads', 'num_threads', type=int, default=3)
@click.option('-a', '--all', 'all_pools', is_flag=True, default=False)
@click.pass_context
def update_pool(ctx, pool_ids, num_threads, all_pools):
    e621 = ctx.obj['e621']

    if all_pools:
        pool_ids = tuple(set(list(pool_ids) + e621.get_cached_pools()))

    for pool_id in pool_ids:
        pool = e621.get_pool(pool_id)
        pool.download(num_threads, ignore_post_age=True)

if __name__ == '__main__':
    cli()
