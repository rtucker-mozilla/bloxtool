from setuptools import setup, find_packages

setup(name='bloxtool',
      version='0.22',
      description='Tool for interfacing with InfoBlox',
      url='https://github.com/rtucker-mozilla/bloxtool',
      author='Rob Tucker',
      author_email='rtucker@mozilla.com',
      license='Mozilla Public License',
      packages = [
          'bloxtool',
      ],
      install_requires = [
            "requests",
            "docopt",
            "pyaml",
      ],
      scripts=["bin/bloxtool"],
      zip_safe=False)
