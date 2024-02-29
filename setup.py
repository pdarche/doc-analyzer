from setuptools import setup, find_packages

setup(
    name='doc_analyzer',
    author='Peter Darche',
    version='0.1.10',
    packages=find_packages(),
    install_requires=[
        'PyMuPDF',
        'PyPDF2',
        'requests',
        'langchain',
        'llama_index==0.8.26',
        'boto3',
        'scikit-learn',
        'openai==0.27.8',
        'pydantic==1.10.12',
        'pydub',
        'textract',
        'html2text',
        'beautifulsoup4'
    ],
)
