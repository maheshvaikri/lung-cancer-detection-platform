from setuptools import setup, find_packages

setup(
    name='lung-cancer-detection-platform',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'flask>=2.1.0',
        'flask-jwt-extended>=4.4.0',
        'tensorflow>=2.9.0',
        'numpy>=1.22.3',
        'pandas>=1.4.2',
        'scikit-learn>=1.1.0',
        'cryptography>=3.4.7',
        'pyyaml>=6.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.1.1',
            'coverage>=6.3.2',
            'mypy>=0.950'
        ]
    },
    author='Healthcare AI Team',
    description='Privacy-Preserving Lung Cancer Detection Platform',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.8',
)