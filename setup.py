from setuptools import setup

setup(
    name='python_intensifies',
    version='0.0.2',
    author="Carvell Scott",
    author_email="carvell.scott@gmail.com",
    keywords=['intensify intensifies shaking memes'],
    py_modules=['intensify'],
    url="https://github.com/CarvellScott/",
    install_requires=[
        "pillow"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: EVERYONE',
        'Topic :: Fun',
        'License :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
        'Programming Language :: Python :: 3.6'
    ],
    description="A tool for INTENSIFYING images.",
    long_description=open('README.md').read(),
    entry_points={
        "console_scripts": [
            "intensify=intensify:main"
        ]
    }
)
