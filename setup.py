from setuptools import setup, find_packages
import os


def read(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()

setup(
    name="fenrir",
    version="0.0.1",
    author=["Victor Sotomayor Monroy", "Michel Gonzalez", "Barry Congressi", "Bryan Kristofferson", "Roberto Rafael Edde Verde"],
    author_email="victor@ufl.edu",
    description="A fantasy turn-based role-playing game",
    long_description=read('README.md'),
    license="MIT",
    url="https://github.com/Mgonzalez-droid/Project-Fenrir",
    packages=find_packages(),
    install_requires=["pygame"],
    include_package_data=True,

    entry_points={
        "console_scripts": [
            "fenrir = fenrir.app:run"
        ]
    }
)
