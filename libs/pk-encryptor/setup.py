from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as file:
    requirements = file.readlines()

setup(
    name='pk_encryptor',
    version='0.0.1',
    py_modules=['pk_encryptor'],
    packages=find_packages(),
    package_data={
        'pk_encryptor': ['resources/**/*'],
    },
    install_requires=requirements,
    data_files=[('', ['requirements.txt'])],
    author='Indeoo',
    author_email='indeooars@gmail.com',
    description='pk_encryptor.',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Indeoo/web3-wizzard-lib/',
)
