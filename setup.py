from setuptools import setup, find_packages

setup(
    name='sigradb',
    version='0.1.0',
    description='A package for handling data universes and data spaces using RDF and simphony-Future Open Semantic '
                'Platform (OSP)',
    author=';-)',
    author_email='a.hashibon@ucl.ac.uk',
    packages=find_packages(),
    install_requires=[
        'simphony_osp',
        'filelock',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='RDF, ontology, dataspace, graph data base, graphs',
)
