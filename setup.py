from setuptools import setup


setup(
    name='rptl',
    version='0.1',
    py_modules=['rptl'],
    install_requires=[
        'Click',
        'picamera',
    ],
    entry_points='''
        [console_scripts]
        rptl=rptl:cli
    ''',
)
