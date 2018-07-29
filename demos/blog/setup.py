from setuptools import setup


install_requires = [
    'aiohttp',
    'aiohttp-jinja2',
    'bcrypt',
    'pytoml',
    'aiohttp_security[session]',
    'aioredis',
    'sqlalchemy',
    'asyncpg',
    'asyncpgsa',
]

setup(
    name='aiohttpdemo-blog',
    version='0.2',
    install_requires=install_requires,
)
