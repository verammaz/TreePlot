from setuptools import setup

setup(
        name='TreePlot',
        version='0.1.0',
        author='Vera Mazeeva',
        author_email='vmmazeeva@gmail.com',
        description=('Ladderized tree plotter'),
        packages=['treeplot'],
        scripts=[],
        install_requires=['plotly', 'kaleido']
    )