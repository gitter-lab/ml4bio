# uses https://github.com/greenelab/manubot/blob/master/setup.py as a template
import pathlib
import re

import setuptools

directory = pathlib.Path(__file__).parent.resolve()

# version
init_path = directory.joinpath('ml4bio', '__init__.py')
text = init_path.read_text()
pattern = re.compile(r"^__version__ = ['\"]([^'\"]*)['\"]", re.MULTILINE)
version = pattern.search(text).group(1)

# long_description
readme_path = directory.joinpath('README.md')
long_description = readme_path.read_text()

setuptools.setup(
    # Package details
    name='ml4bio',
    version=version,
    url='https://github.com/gitter-lab/ml4bio',
    description='A graphical interface for sklearn classification to introduce machine learning to biologists',
    long_description_content_type='text/markdown',
    long_description=long_description,
    license='MIT',

    # Author details
    author='Fangzhou Mu',
    author_email='fmu2@wisc.edu',

    # Package topics
    keywords='education machine-learning classification',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
    ],

    packages=setuptools.find_packages(),

    # Specify python version
    python_requires='>=3.5',

    # Run-time dependencies
    install_requires=[
        'matplotlib',
        'numpy',
        'pandas',
        'pyqt>=5',
        'scikit-learn',
        'scipy',
    ],

    # Additional groups of dependencies
    extras_require={
    },

    # Create command line script
#    entry_points={
#        'console_scripts': [
#            'ml4bio = ml4bio:main',
#        ],
#    },

    # Include package data files from MANIFEST.in
    include_package_data=True,
)
