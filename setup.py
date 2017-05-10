import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

version = (0, 0, 1)

setup(
    name='django-gemstone',
    version=".".join([str(d) for d in version]),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',  # example license
    description='JSON RPC microservices with Django',
    long_description=README,
    url='https://github.com/vladcalin/django-gemstone',
    author='Calin Vlad',
    author_email='vlad.s.calin@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
