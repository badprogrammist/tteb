from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='tteb',
    version='0.1',
    py_modules=['tteb'],
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        tteb=tteb:cli
    ''',
)