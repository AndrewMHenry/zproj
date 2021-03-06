from setuptools import setup, find_packages

setup(name='zproj',
      version='1.0.10',
      packages=find_packages(),
      entry_points = {
          'console_scripts': [
              'zabc=zproj.zabc:main',
              'zmake=zproj.zmake:main',
              'zapp=zproj.zapp:main',
              'zproj=zproj.zproj_tools:main'
          ]
      },
      author='Andrew Henry',
      author_email='andrewmichaelhenry@gmail.com',
      url='https://github.com/AndrewMHenry/zproj',
      include_package_data=True,
      classifiers="Programming Language :: Python :: 3 :: Only",
      install_requires=['peeker'])
