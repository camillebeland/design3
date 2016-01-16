try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Design III',
    'install_requires': ['nose'],
    'scripts': [],
    'name': 'Pirates des Caraibes'
}

setup(**config)
