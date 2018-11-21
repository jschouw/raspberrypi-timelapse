# raspberrypi-timelapse
A simple solution for taking time lapses (on Raspberry Pi with PiCamera) using constant settings across all exposures.


Many of the basic tutorials for taking time lapses with Raspberry Pi do not account for the Pi's camera module
auto-adjusting camera settings such as shutter speed and white balance in between exposures. If the camera uses
different settings across every frame, it will create an undesirable 'flickering' effect in the final compilation.
This program tries to prevent flickering by using consistent settings across all exposures in the time lapse.

Note that this works best when the light in the scene does not change very much during the time lapse. The program
locks settings in at the *beginning* of the time lapse, so if, for example, a big cloud blocks the sun it will likely
lead to those frames being underexposed due to the loss of light. You can fix some of this in post-production, but
it's best to do whatever you can to avoid major changes in light. If you're outside and the clouds are unpredictable,
maybe try taking a shorter time lapse.
(Future development will likely try to tackle this difficult problem of adjusting camera settings while avoiding
flicker)