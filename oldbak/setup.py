import os
from setuptools import setup, find_packages

install_requires = [
    'PyAxe',
]

f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()


setup(
    name='PyAxeTool',
    version=__import__('PyAxeTool').__version__,
    description='An utility tool collection for make life easily',
    long_description=readme,
    author='Sun Jin',
    author_email='412640665@qq.com',
    url='https://github.com/sunjinopensource/PyAxeTool/',
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)
