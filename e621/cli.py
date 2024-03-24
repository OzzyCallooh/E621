import click
from pathlib import Path

from .e621 import E621
from .config import Config


@click.group
@click.option('-c', '--config', 'config_file_path', type=click.Path(exists=True), default=Path('config.yaml'))
@click.pass_context
def cli(ctx, config_file_path):
    ctx.ensure_object(dict)
    config = Config(config_file_path)
    ctx.obj['e621'] = E621(config)


@cli.command
@click.argument('pool_ids', type=int, nargs=-1)
@click.option('-t', '--threads', 'num_threads', type=int, default=3)
@click.pass_context
def download_pool(ctx, pool_ids, num_threads):
    e621 = ctx.obj['e621']
    pools = [ e621.get_pool(pool_id) for pool_id in pool_ids ]
    for pool in pools:
        pool.download(num_threads)

if __name__ == '__main__':
    cli()
