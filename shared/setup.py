from setuptools import find_packages, setup

setup(
    name="core",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    description="A Django app for shared authentication across multiple services",
    install_requires=[
        "Django>=5.1.6",
        "django-phonenumber-field[phonenumbers]>=5.0.0",
        "asgiref>=3.8.1",
        "sqlparse>=0.5.3",
        "pytz>=2025.1",
    ],
)
