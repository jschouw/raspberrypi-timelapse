import click
import os

INTERVAL_MAX_LIMIT = 180  # 3 minutes
FRAMES_MAX_LIMIT = 1000
ISO_MIN_LIMIT = 100
ISO_MAX_LIMIT = 1000


@click.command()
@click.option('--name', '-n', required=True,
              type=click.Path(file_okay=False, dir_okay=True, writable=True),
              prompt='Enter a unique directory name to store images. NO spaces, ONLY letters, numbers, and underscores',
              help='directory name')
@click.option('--iso', '-i', type=click.IntRange(ISO_MIN_LIMIT, ISO_MAX_LIMIT), help='manual ISO setting')
@click.argument('interval', type=click.IntRange(0, INTERVAL_MAX_LIMIT))
@click.argument('total', type=click.IntRange(0, FRAMES_MAX_LIMIT))
def cli(interval, total, name, iso):
    """
    \b
    [Raspberry Pi Time Lapse]
    Takes time lapses using consistent camera settings across all exposures.
    \b
    Specify the INTERVAL between each exposure (in seconds) and the
    TOTAL number of exposures.
    If you are manually setting the ISO, try 100 or 200 for daytime, and
    400 or 800 for nighttime or low light environments.
    \b
    Note that this program adjusts the camera at the beginning of the time
    lapse, freezes the camera's settings (such as shutter speed and
    white balance), and uses those settings for all exposures during that
    time lapse. This prevents a 'flickering' effect in the final video
    that is caused by the camera auto-adjusting before each exposure,
    however it means the camera will not adjust for any major changes in
    lighting during the time lapse.
    For best results, avoid variations in lighting or color during the
    time lapse.
    """

    if not os.path.exists(name):
        try:
            os.mkdir(name)
            click.echo('Directory \'{}\' created!'.format(name))
            click.echo('[Settings]')
            click.echo('Interval: {}'.format(interval))
            click.echo('Total: {}'.format(total))
            click.echo('ISO: {}'.format(iso))
        except OSError:
            click.echo('\'{}\' is not a valid directory name! Try using only letters, numbers, and underscores.'.format(name))
    else:
        click.echo('\'{}\' directory already exists! Choose a unique directory name.'.format(name))
