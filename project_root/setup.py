from setuptools import setup, find_packages

setup(
    name='cryptocore',
    version='1.0.0',
    description='AES-128 ECB Encryption/Decryption Tool',
    author='Your Name',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'cryptocore = src.cli_parser:main',
        ],
    },
    install_requires=[
        'pycryptodome',
    ],
    python_requires='>=3.6',
)