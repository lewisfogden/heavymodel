import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="heavymodel-lewisfogden", # Replace with your own username
    version="0.0.2",
    author="Lewis Fogden",
    author_email="lewisfogden@gmail.com",
    description="Heavy Model Actuarial Modelling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lewisfogden/heavymodel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
