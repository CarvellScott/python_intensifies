from setuptools import setup

setup(
    name='python_intensifies',
    version='0.0.4',
    author="Carvell Scott",
    author_email="carvell.scott@gmail.com",
    keywords=['intensify intensifies shaking memes'],
    py_modules=['intensify'],
    url="https://github.com/CarvellScott/",
    install_requires=[
        "Pillow==5.4.1"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Artistic Software',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    description="A tool for INTENSIFYING images.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "intensify=intensify:main"
        ]
    }
)
