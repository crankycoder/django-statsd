from setuptools import setup


setup(
    name='django-metlog-mozilla',
    version='0.1',
    description='Django interface with metlog',
    long_description=open('README.rst').read(),
    author='Victor Ng',
    author_email='vng@mozilla.com',
    license='MPL 2',
    install_requires=['metlog-py'],
    packages=['django_metlog',
              'django_metlog/patches',
              'django_metlog/clients',
              'django_metlog/loggers',
              'django_metlog/management'],
    url='https://github.com/crankycoder/django-metlog',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Framework :: Django'
        ],
    )
