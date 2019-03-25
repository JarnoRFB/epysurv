from setuptools import setup, find_packages
import os
# import versioneer

package = 'epysurv'

_here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=package,
    version="0.0.1",
    # cmdclass=versioneer.get_cmdclass(),
    description='Epidemiological surveillance in Python.',
    long_description=long_description,
    author='Rüdiger Busche',
    author_email='rbusche@uos.de',
    url='https://github.com/JarnoRFB/epysurv',
    license='MIT',
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.7'
    ],
)
