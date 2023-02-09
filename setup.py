from setuptools import find_packages, setup

setup(
    name='request-via-request-server',
    version='1.0',
    packages=find_packages(
        exclude=['tests', 'tests.*', '*.tests', '*.tests.*'],
    ),
    entry_points={
        'console_scripts': [
            'request_via_request_server = request_via_request_server.server:main'
        ],
    },
    requires=[],
)