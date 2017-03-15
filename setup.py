from setuptools import setup, find_packages

setup(name='bloxtool',
      version='0.18',
      description='Tool for interfacing with InfoBlox',
      url='https://github.com/rtucker-mozilla/bloxtool',
      author='Rob Tucker',
      author_email='rtucker@mozilla.com',
      license='Mozilla Public License',
      packages=find_packages(),
      scripts=["bloxtool/bloxtool.py"],
      zip_safe=False)
