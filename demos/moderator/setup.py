import os
import re

from setuptools import find_packages, setup


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__),
                           'moderator', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            msg = 'Cannot find version in moderator/__init__.py'
            raise RuntimeError(msg)


install_requires = [
    'aiohttp',
    'trafaret',
    'pyyaml',
    'numpy',
    'pandas',
    'scikit-learn',
    'scipy',
]


classifiers = [
    'License :: OSI Approved :: MIT License',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Operating System :: POSIX',
    'Development Status :: 3 - Alpha',
    'Framework :: AsyncIO',
]


setup(name='moderator',
      classifiers=classifiers,
      version=read_version(),
      description='Moderator AI app: UI and API',
      platforms=['POSIX'],
      author='Nikolay Novik',
      author_email='nickolainovik@gmail.com',
      url='https://github.com/jettify/moderator.ai',
      packages=find_packages(),
      include_package_data=True,
      install_requires=install_requires,
      license='Apache 2',
      zip_safe=False)
