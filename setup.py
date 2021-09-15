# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prance_cli_error_parser']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.2.0,<4.0.0',
 'openapi-spec-validator>=0.3.1,<0.4.0',
 'prance>=0.21.8,<0.22.0']

setup_kwargs = {
    'name': 'prance-cli-error-parser',
    'version': '0.1.0',
    'description': 'A command-line tool that parses and prints beautiful prance validation errors',
    'long_description': None,
    'author': "'Gilad Barnea'",
    'author_email': 'cr-gbarn-herolo@allot.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
