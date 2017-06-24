from setuptools import setup, find_packages

setup(name='zproj',
      packages=find_packages(),
      entry_points = {
          'console_scripts': [
              'zabc=zproj.zabc:main',
              'zmake=zproj.zmake:main',
              'zapp=zproj.zapp:main'
          ]
      },
      author='Andrew Henry',
      author_email='andrewmichaelhenry@gmail.com',
      include_package_data=True,
      install_requires=['peeker'])
