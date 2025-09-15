from setuptools import setup, find_packages

setup(
    name='grid_py',                        # your project/package name
    version='0.1',
    packages=find_packages(where='src'), # find all subpackages inside src
    package_dir={'': 'src'},              # specify src as root package directory
    install_requires=[
        'ccxt',
        'pandas',
        'numpy',
        'matplotlib',
        'pandas-ta',
        'backtesting',
        'python-dotenv'
        # add any other dependencies here
    ],
    python_requires='>=3.12',
)