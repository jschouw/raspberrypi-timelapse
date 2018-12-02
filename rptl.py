import click
import os
from picamera import PiCamera
from time import sleep

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
    This program adjusts the camera at the beginning of the time lapse,
    freezes the camera's settings (such as shutter speed and white balance),
    and uses those settings for all exposures during that time lapse. This
    prevents a 'flickering' effect in the final video that is caused by the
    camera auto-adjusting before each exposure, however it means the camera
    will NOT adjust for any changes in lighting.
    For best results, avoid variations in lighting or color during the
    time lapse.
    """

    # Implicitly joined strings for a multi-line string that can be indented properly
    confirm_prompt_text = ('\n[Are you sure these settings are correct?]'
                           '\nDirectory name:  \'{}\''
                           '\nInterval:         {} second(s) between each exposure'
                           '\nTotal:            {} exposures'
                           '\nISO:              {}     (if ISO is the default \'None\', '
                           'it will be set automatically)\n').format(name, interval, total, iso)

    if not os.path.exists(name):
        # Show confirmation prompt so user can review settings
        if click.confirm(confirm_prompt_text, abort=True, default=True, show_default=True):
            try:  # Directory creation
                os.mkdir(name)
            except OSError:
                click.echo('\'{}\' is not a valid directory name! '
                           'Try using only letters, numbers, and underscores.'.format(name))

            # Camera creation, auto-adjust settings before disabling auto-adjust
            camera = PiCamera(resolution=(1280, 960))
            # Set custom ISO if provided by user
            if iso is not None:
                camera.iso = iso
            # Show progress bar while letting camera auto-adjust, sleep for 3 seconds
            with click.progressbar(length=3, label='Letting the camera auto-adjust', show_eta=False) as bar:
                for iteration in bar:
                    sleep(1)
            # Set shutter speed
            camera.shutter_speed = camera.exposure_speed
            camera.exposure_mode = 'off'
            click.echo('Shutter speed set to {}'.format(camera.shutter_speed))
            # Set white balance
            gains = camera.awb_gains
            camera.awb_mode = 'off'
            camera.awb_gains = gains
            click.echo('White balance set to {}'.format(camera.awb_gains))
            # Show progress bar and start time lapse
            with click.progressbar(camera.capture_continuous('image{counter:04d}.jpg'),
                                   label='Taking time lapse... Press Ctrl-C to abort!') as bar:
                for iteration in bar:
                    pass  # TODO: Find a better way to do this? It seems clunky. Test thoroughly!
    else:
        click.echo('\'{}\' directory already exists! Choose a unique directory name.'.format(name))
