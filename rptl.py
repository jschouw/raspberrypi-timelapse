import click

INTERVAL_MAX_LIMIT = 180  # 3 minutes
FRAMES_MAX_LIMIT = 1000
ISO_MIN_LIMIT = 100
ISO_MAX_LIMIT = 800

@click.command()
@click.option('--name', '-n', required=True,
              type=click.Path(file_okay=False, dir_okay=True),
              prompt='Enter a unique directory name to store images. NO spaces, ONLY letters and numbers',
              help='directory name')
@click.option('--iso', '-i', type=click.IntRange(ISO_MIN_LIMIT, ISO_MAX_LIMIT), help='manual ISO setting')
@click.argument('interval', type=click.IntRange(0, INTERVAL_MAX_LIMIT))
@click.argument('total', type=click.IntRange(0, FRAMES_MAX_LIMIT))
def cli(interval, total, name, iso):
    """Set the interval between each frame (in seconds) and the total # of frames."""
    click.echo('Interval: {}'.format(interval))
    click.echo('Total: {}'.format(total))
    click.echo('Directory Name: {}'.format(name))
    click.echo('ISO: {}'.format(iso))

