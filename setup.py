from setuptools import setup, find_packages
import os

version = '1.15.1'

base_dir = os.path.dirname(__file__)


setup(name='django-datatables-view',
      version=version,
      description='Django datatables view',
      long_description=open(os.path.join(base_dir, "README.rst")).read(),
      url='https://bitbucket.org/pigletto/django-datatables-view',
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Django',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4'
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
      ]
      )
