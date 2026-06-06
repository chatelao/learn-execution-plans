import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

project = 'Execution Plan Mastery Tutorial'
copyright = '2024, Jules'
author = 'Jules'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
