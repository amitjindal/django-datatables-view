from setuptools import setup, find_packages
import os

version = '1.10'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(name='django-datatables-view',
      version=version,
      description='Django datatables view',
      long_description=README,
      url='https://bitbucket.org/pigletto/django-datatables-view',
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Django',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
      ],
      keywords='django datatables view',
      author='Maciej Wisniowski',
      author_email='maciej.wisniowski@natcam.pl',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      dependency_links=[],
      install_requires=[
          'setuptools',
      ],
     )
