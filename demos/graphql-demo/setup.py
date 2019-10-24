import os
import re

from setuptools import find_packages, setup


REGEXP = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")


def read_version():

    init_py = os.path.join(os.path.dirname(__file__), 'graph', '__init__.py')

    with open(init_py) as f:
        for line in f:
            match = REGEXP.match(line)
            if match is not None:
                return match.group(1)
        else:
            msg = f'Cannot find version in ${init_py}'
            raise RuntimeError(msg)


install_requires = [
    'aiohttp',
    'aiopg[sa]',
    'aiohttp_jinja2',
    'aiohttp_graphql',
    'aioredis',
    'aiodataloader',
    'trafaret_config',
    'graphene==2.1.7',
    'graphql-core==2.2.1',
    'graphql-ws',
    'psycopg2-binary',
    'Faker',
]


setup(
    name='graph',
    version=read_version(),
    description='The GraphQL example from aiohttp',
    platforms=['POSIX'],
    packages=find_packages(),
    package_data={
        '': ['config/*.*']
    },
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
)
