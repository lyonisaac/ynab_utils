from setuptools import setup, find_packages

setup(
    name="ynab-tools-core",
    version="0.1.0",
    description="Core package for YNAB tools and utilities",
    author="YNAB Tools",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "groq>=0.4.0",
        "typing-extensions>=4.5.0",
    ],
    python_requires=">=3.7",
)