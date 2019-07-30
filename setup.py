
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

def find_version(*file_paths):
    with open(os.path.join(here, *file_paths), 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.strip().split('=')[1].strip(' \'"')
    raise RuntimeError(("Unable to find version string. "
                        "Should be __init__.py."))

with open('README.md', 'rb') as f:
    readme = f.read().decode('utf-8')

install_requires = [
    'numpy<=1.14.2',
    'pandas<=0.22.0',
    'daiquiri<=1.3.0',
    'Flask<=1.0.2']

setup(
    name='dcdl_player',
    keywords=['figures', 'letters', 'game'],
    version=find_version('dcdl_player', '__init__.py'),
    description='Play to "des chiffres et des lettres"',
    long_description=readme,
    license='MIT',
    author='Raphaël Delhome',
    author_email='raphael.delhome@club-internet.fr',
    maintainer='Raphaël Delhome',
    maintainer_email='',
    url='https://github.com/delhomer/dcdl_player',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Games',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3',
    install_requires=install_requires,
    packages=find_packages(),
    entry_points = {
        "console_scripts": ["dcdl=dcdl_player.tools.__main__:main"],
    }
)
