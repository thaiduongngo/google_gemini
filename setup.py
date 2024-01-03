import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().split("\n")

setuptools.setup(
    name="Google Gemini",
    version="0.0.1",
    author="NtD",
    author_email="thaiduong.ngo@gmail.com",
    description="Backend Python Gemini",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={},
    python_requires=">=3.11.7",
    install_requires=requirements,
)
