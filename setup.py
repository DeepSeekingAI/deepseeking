from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="deepseeking",
    version="0.1.0",
    author="DeepSeekingAI",
    author_email="deepseekingai@hotmail.com",
    description="AI-Powered Blockchain Prediction Market & Risk Management Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DeepSeekingAI/deepseeking",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "torch>=1.9.0",
        "transformers>=4.11.0",
        "web3>=5.24.0",
        "eth-brownie>=1.17.0",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "websockets>=10.0",
        "aiohttp>=3.8.0",
        "python-twitter>=3.5.0",
        "praw>=7.4.0",
        "requests>=2.26.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "pytest-asyncio>=0.16.0",
            "pytest-cov>=2.12.0",
            "black>=21.9b0",
            "isort>=5.9.3",
            "flake8>=3.9.2",
        ],
    },
) 