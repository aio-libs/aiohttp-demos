from setuptools import setup


install_requires = (
    'aiohttp',
    'aiohttp-jinja2',
    'bcrypt',
    'pytoml',
    'aiohttp_security[session]',
    'redis==4.3.4',
    'sqlalchemy',
    'asyncpg',
    'asyncpgsa',
)

setup(
    name='aiohttpdemo-blog',
    version='0.2',
    install_requires=install_requires,
    packages=("aiohttpdemo_blog",)
)
