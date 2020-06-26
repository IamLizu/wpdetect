from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
setup(
  name = 'wpdetect',
  packages = ['wpdetect'],
  version = '1.3.6',
  license='MIT',
  description = 'A WordPress detection tool, detects if a website is running WordPress',
  long_description=long_description,
  long_description_content_type='text/rst',
  author = 'S M Mahmudul Hasan',
  author_email = 'thegeek@iamlizu.com',
  url = 'https://iamlizu.com/tools/wpdetect/',
  download_url = 'https://github.com/IamLizu/wpdetect/archive/v_1_3_6.tar.gz',
  keywords = ['WordPress', 'Detect', 'wpdetect'],
  install_requires=[
          'pyfiglet',
      ],
  entry_points = {
        'console_scripts': [
            'wpdetect = wpdetect.__main__:main'
        ]
  },
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)