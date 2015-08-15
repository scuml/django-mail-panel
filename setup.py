from setuptools import setup, find_packages

setup(
    name='debug-toolbar-mail',
    version='1.0.0',
    description='A panel for django-debug-toolbar that allows for ' +
                'viewing of recently sent email.',
    long_description=open('README.md').read(),
    author='Stephen Mitchell',
    author_email='stephen@echodot.com',
    url='https://github.com/scuml/debug-toolbar-mail',
    download_url='https://pypi.python.org/pypi/debug-toolbar-mail',
    license='BSD',
    packages=find_packages(exclude=('tests', 'example')),
    install_requires=[
        'django>=1.8',
        'django-debug-toolbar>=1.0',
    ],
    include_package_data=True,
    zip_safe=False,                 # because we're including static files
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
