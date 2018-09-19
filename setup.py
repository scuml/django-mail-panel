import os
from pathlib import Path
import sys
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(Path(__file__).absolute().parent)

if 'publish' in sys.argv:
    if 'test' in sys.argv:
        os.system('python setup.py sdist bdist_wheel upload -rtest')
    else:
        os.system('python setup.py sdist bdist_wheel')
        # twine upload --repository pypi dist/*1.1.0*  # For markdown to render, use twine
    sys.exit()


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='django-mail-panel',
    version='1.2.1',
    description='A panel for django-debug-toolbar that allows for ' +
                'viewing of recently sent email.',
    url='https://github.com/scuml/django-mail-panel',

    license="Apache",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author='Stephen Mitchell',
    author_email='stephen@echodot.com',

    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={'': ['LICENSE']},

    install_requires=[
        'django>=1.8',
        'django-debug-toolbar>=1.0',
    ],
    include_package_data=True,
    zip_safe=False,                 # because we're including static files
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
