from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = "-e ."

def get_requirements(file_path:str) -> List[str]:
    '''
    This Function return the List of requirements of Library
    '''

    requirements = []
    with open(file_path, 'r') as file:
        requirements = file.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
    name="mlproject",
    version="0.0.1",
    author="Ansari Ehteesham Aqeel",
    author_email="an.ehteesham@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt')
)