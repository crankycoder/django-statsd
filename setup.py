from setuptools import setup


setup(
    name='django-metlog-mozilla',
    version='0.1',
    description='Django interface with metlog',
    long_description=open('README.rst').read(),
    author='Andy McKay',
    author_email='andym@mozilla.com',
    license='BSD',
    install_requires=['statsd'],
    packages=['django_statsd',
              'django_statsd/patches',
              'django_statsd/clients',
              'django_statsd/loggers',
              'django_statsd/management'],
    url='https://github.com/andymckay/django-statsd',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Framework :: Django'
        ],
    )
