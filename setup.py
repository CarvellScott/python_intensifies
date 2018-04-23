from setuptools import setup

setup(
    name='python_intensifies',
    version='0.0.0',
    author="Carvell Scott",
    author_email="carvell.scott@gmail.com",
    keywords=['intensify intensifies shaking'],
    packages=['python_intensifies'],
    url="https://github.com/CarvellScott/",
    install_requires=[
        "moviepy"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: EVERYONE',
        'Topic :: Fun',
        'License :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
    ],
    description="A tool for INTENSIFYING images.",
    long_description=open('README.md').read(),
    entry_points={
        "console_scripts": [
            "intensify=python_intensifies.__main__:main"
        ]
    }
)
