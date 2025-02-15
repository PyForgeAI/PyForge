# PyForge REST

## License

Copyright 2021-2025 Avaiga Private Limited

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
except in compliance with the License. You may obtain a copy of the License at
[http://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)

Unless required by applicable law or agreed to in writing, software distributed under the
License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions
and limitations under the License.

## What is PyForge REST

PyForge is a Python library for creating Business Applications. More information on our
[website](https://www.pyforge.io). PyForge is split into multiple packages including
*pyforge-core* and *pyforge-rest* to let users install the minimum they need.

PyForge Core mostly includes business-oriented
features. It helps users create and manage business applications and improve analyses
capability through time, conditions and hypothesis.

PyForge REST is a set of APIs built on top of the
*pyforge-core* library developed by Avaiga. This project is meant to be used as a complement
for PyForge and its goal is to enable automation through rest APIs of processes built
on PyForge.

## Installation

The latest stable version of *pyforge-rest* is available through *pip*:
```bash
pip install pyforge-rest
```

### Development version

You can install the development version of *pyforge-rest* with *pip* and *git* via the pyforge repository:
```bash
pip install git+https://git@github.com/Avaiga/pyforge
```

This command installs the development version of *pyforge* package in the Python environment with all
its dependencies, including the *pyforge-rest* package.

If you need the source code for *pyforge-rest* on your system so you can see how things are done or
maybe participate in the improvement of the packages, you can clone the GitHub repository:

```bash
git clone https://github.com/Avaiga/pyforge.git
```

This creates the 'pyforge' directory holding all the package's source code, and the 'pyforge-rest'
source code is in the 'pyforge/rest' directory.

## Configuration

Before running, we need to define some variables. PyForge REST APIs depend on pre-configuration of pyforge config objects,
i.e, is mandatory to define all configuration of DataNodes, Tasks, Sequences, etc. The file containing this
configuration needs to be passed to the application at runtime. The following variable needs to be defined:
 - TAIPY_SETUP_FILE: the path to the file containing all of pyforge object configuration

If using Docker, the folder containing the file needs to be mapped as a volume for it to be accessible to the
application.

## Running

To run pyforge-rest, you need to install the required development packages.
We recommend using [Pipenv](https://pipenv.pypa.io/en/latest/) to create a virtual environment
and install the development packages.

```bash
pip install pipenv
pipenv install --dev
```

To run the application you can either run locally with:
```bash
flask run
```

or it can be run inside Docker with:
```bash
docker-compose up
```

You can also run with a Gunicorn or wsgi server.

### Running with Gunicorn

This project provide a simple wsgi entry point to run gunicorn or uwsgi for example.

For gunicorn you only need to run the following commands

```bash
pip install gunicorn

gunicorn myapi.wsgi:app
```
And that's it! Gunicorn is running on port 8000.

If you chose gunicorn as your wsgi server, the proper commands should be in your docker-compose file.

### Running with uwsgi

Pretty much the same as gunicorn here

```bash
pip install uwsgi
uwsgi --http 127.0.0.1:5000 --module myapi.wsgi:app
```

And that's it! Uwsgi is running on port 5000.

If you chose uwsgi as your wsgi server, the proper commands should be in your docker-compose file.

### Deploying on Heroku

Make sure you have a working Docker installation (e.g. docker ps) and that you’re logged in to Heroku (heroku login).

Log in to Container Registry:

```bash
heroku container:login
```

Create a heroku app
```bash
heroku create
```

Build the image and push to Container Registry:
```bash
heroku container:push web
```

Then release the image:
```bash
heroku container:release web
```

You can now access *pyforge-rest* on the URL that was returned on the `heroku create` command.
