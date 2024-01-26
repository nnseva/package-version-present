# Utility to check presence of the package in the PyPi-like repository

## Installation

*Stable version* from the PyPi package repository
```bash
pip install package-version-present
```

*Last development version* from the GitHub source version control system
```
pip install git+git://github.com/nnseva/package-version-present.git
```

## Using

Additionally to the central PyPi repository at https://pypi.org, you can use
your own custom PyPi-like private repository in your project.

Building CI/CD scripts, it can be necessary to check, whether the
particular package version is present in your PyPi-like repository.

For example, you would like to check, whether the version is present, and
break a pipeline in this case, because the programmer starting a pipeline
should provide a unique version number differ from the existent.

That's exactly a purpose of this script.

Below is the example code in the bitbucket-pipelines.yml. Use these project
environment variables if you would like to use this example in your pipeline:

- PYPI_REPOSITORY_URL   - base URL of the custom private repository
- PYPI_USERNAME         - username to authenticate yourself in the repository
- PYPI_PASSWORD         - password to authenticate yourself in the repository

```yaml
      - step:
            name: Check the local version presence on the custom pypi repo
            image: snakepacker/python:all
            script:
                - python3.8 -mpip install package-version-present
                - package-version-present `python setup.py --name` `python setup.py --version` -R $PYPI_REPOSITORY_URL -U $PYPI_USERNAME -P "$PYPI_PASSWORD" -T -X
```

Notice that the script uses only built-in packages and doesn't need any additional libraries.

The script is self-descriptive, call it without parameters to see the help.

The script uses PyPi simple API, and is adopted to process the both, XML-based, as well as HTML based result.

After installation, run the following command in the command line to see the detailed help:

```bash
package-version-present
```
