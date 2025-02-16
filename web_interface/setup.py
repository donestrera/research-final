from setuptools import setup, find_packages

setup(
    name="arduino-sensor-dashboard",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=4.2.0',
        'channels>=4.0.0',
        'pyserial>=3.5',
        'python-dotenv>=1.0.0',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A web dashboard for Arduino sensor monitoring",
    keywords="arduino, sensors, dashboard, monitoring",
    python_requires=">=3.8",
) 