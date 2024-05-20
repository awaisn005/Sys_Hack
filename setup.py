from setuptools import setup

setup(
    name='mac-changer',
    version='1.0',
    packages=['mac_changer'],
    install_requires=[],
    author='Awais Naseer',
    description='A tool to change the MAC address of a network interface',
    url='https://github.com/awaisn005/mac-changer',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'mac-changer=mac_changer:main',
        ],
    },
)
