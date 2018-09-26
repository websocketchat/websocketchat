from setuptools import setup
from setuptools import find_packages

setup(
    name='websocketchat',
    python_requires='>=3.7',
    install_requires=[
        'pytz>=2018.5',
        'tornado>=5.1.1',
    ],
    packages=find_packages(
        exclude=[
            'tests'
        ]
    ),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Development Status :: 1 - Planning',
        'Natural Language :: English',
    ],
)

