"""Setup file for cdtea package
"""

import setuptools
import pytori

README_HEADER_LINES = 10

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.readlines()
    LONG_DESCRIPTION = '\n'.join(LONG_DESCRIPTION[README_HEADER_LINES:])
    LONG_DESCRIPTION = 'PyTORI\n' + LONG_DESCRIPTION

setuptools.setup(name='pytori',
                 version=pytori.__version__,
                 description='PyTORI',
                 long_description=LONG_DESCRIPTION,
                 long_description_content_type="text/markdown",
                 python_requires='==3.7, ==3.8',
                 url=pytori.__github_url__,
                 author='James Kennington',
                 author_email='jameswkennington@gmail.com',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 install_requires=[
                     'matplotlib',
                     'numpy',
                     'plotly',
                 ],
                 classifiers=[
                     "Programming Language :: Python",
                     "Programming Language :: Python :: 3.7",
                     "Programming Language :: Python :: 3.8",
                     "Operating System :: MacOS",
                     "Operating System :: POSIX :: Linux",
                     "Operating System :: Microsoft :: Windows",
                 ],
                 zip_safe=False,
                 include_package_data=True,
                 )
