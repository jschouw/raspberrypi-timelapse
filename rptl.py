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
                click.echo('Directory \'{}\' created!'.format(name))
            except OSError:
                click.echo('\'{}\' is not a valid directory name! '
                           'Try using only letters, numbers, and underscores.'.format(name))

            # Create camera and adjust settings
            camera = PiCamera(resolution=(1280, 720))
            if iso is not None:
                camera.iso = iso
            sleep(3)  # TODO: Show the user this is happening so they don't think it's broken
            camera.shutter_speed = camera.exposure_speed
            camera.exposure_mode = 'off'
            gains = camera.awb_gains
            camera.awb_mode = 'off'
            camera.awb_gains = gains

            # Start time lapse
            count = 0
            for filename in camera.capture_continuous(name.join('{counter:04d}.jpg')):  # TODO: Test naming convention!
                click.echo('{} captured.'.format(filename))
                count += 1
                if count >= total:
                    break  # Break the loop of capture_continuous() to stop the time lapse

    else:
        click.echo('\'{}\' directory already exists! Choose a unique directory name.'.format(name))
