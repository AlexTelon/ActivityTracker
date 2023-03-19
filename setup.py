from setuptools import setup, find_packages

setup(
    name='activity_tracker',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pywin32',
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'activity_tracker = activity_tracker.main:main',
        ],
    },
)
