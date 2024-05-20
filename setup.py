from setuptools import setup

setup(
    name='sys_Hack',
    version='1.0',
    packages=['sys_Hack'],
    install_requires=[],
    author='Awais Naseer',
    description='Backdoor Access to OS',
    url='https://github.com/awaisn005/sys_Hack',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'sys-Hack=sys_Hack:main',
        ],
    },
)
