import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


def get_version():
    # type: () -> str

    version_filepath = os.path.join(os.path.dirname(__file__), 'guruguru', 'version.py')
    with open(version_filepath) as f:
        for line in f:
            if line.startswith('__version__'):
                return line.strip().split()[-1][1:-1]
    assert False


def get_install_requires():
    install_requires = [
        'requests',
        'tabulate',
        'pandas'
    ]
    return install_requires


def get_extra_requires():
    extras = {
        'test': ['pytest', 'pytest-cov', 'responses', 'freezegun'],
        'document': ['sphinx', 'sphinx_rtd_theme']
    }
    return extras


setup(
    name='guruguru',
    version=get_version(),
    author='nyk510',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='guruguru cli toolkit',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://atma.co.jp/',
    author_email='yamaguchi@atma.co.jp',
    install_requires=get_install_requires(),
    tests_require=get_extra_requires()['test'],
    extras_require=get_extra_requires(),
    entry_points={
        'console_scripts': ['guruguru = guruguru.cli:main']
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
