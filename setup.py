import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ["torch",
                'torch-geometric',
                'biopandas',
                'seaborn',
                'sklearn',
                'tqdm',
                'wget'
                ]

setuptools.setup(
    name="pdb_pyg",
    version="0.0.1",
    author="Carlos Oliver, Dexiong Chen, Leslie O'Bray, Tim Kucera,",
    author_email="carlos.oliver@bsse.ethz.ch",
    description="Dead simple datasets for loading PDBs into torch-geometric.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)

