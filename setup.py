import setuptools

setuptools.setup(
    name='Flashlight',
    version="1.0",
    author='Fabian Wahren',
    author_email='fabianwahren@gmail.com',
    description='Puzzle Game',
    packages=setuptools.find_packages(),
    install_requires=[
        'pygame',
        'pygame_menu',
        'numpy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)