from setuptools import setup

setup(
    name='opentelemetry-decorators',
    version='23.09.23',
    packages=['opentelemetry', 'opentelemetry.decorators', 'opentelemetry.decorators.handlers'],
    install_requires=[
        'opentelemetry-api',
        'opentelemetry-sdk'
    ],
    url='',
    license='',
    author='Rishavjeet Singh Sidhu',
    author_email='',
    description='Decorator for automatically handling propagation, with flexibility to do manual integration.'
)
