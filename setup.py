from setuptools import setup, find_packages

with open('README.md', 'r', encoding='UTF-8') as fh:
    long_description = fh.read()

setup(name='easy_log',
      author='aneknana',
      author_email='',
      version='0.0.1',
      description='simple logger with retrier', 
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=find_packages(),
      classifiers=[
          'Programming Language :: Python :: 3', ],
      python_requires='>=3.10',
)
