============
Data Compass
============

Data Flow Mapping.
 

Development Installation
=========================

Database Setup
--------------
PostgreSQL is used as a primary database engine.


On ubuntu or Debian based system to install and start Postgresql you can run something like

.. code:: bash

    sudo apt update
    sudo apt install postgresql postgresql-contrib libpq-dev
    sudo service postgresql start


After installing Postgresql, you will need to initialize the database.

Login as  Postgresql admin user (`postgres`)

.. code:: bash

    sudo su -l postgres


While logged in as `postgres` create the project database 

.. code:: bash

    createdb datacompass


Connect to the database shell

.. code:: bash

    psql data compass


While you are in the database shell create the database user and grant appropriate privileges to the user.

.. code:: sql

    CREATE USER datacompass WITH PASSWORD 'datacompass';
    GRANT ALL PRIVILEGES ON DATABASE datacomapss TO datacompass;
    exit;


Logout as `postgres` user

.. code:: bash

    exit

You may use any database name, user name or password, just Make sure you keep the
credentials because you will need them later in your project configuration.


Install system wide Python dependencies
---------------------------------------

Install Python development header files (python-dev) and Python package Installer `pip <https://pip.pypa.io/en/stable>`_

.. code:: bash

    sudo apt-get install python3-dev python3-pip


Setup a Python virtual environment
----------------------------------

It is recommended to isolate project dependencies in order to avoid potential
dependency conflicts. One of the simplest ways to achieve that is by using `Python virtual environments <https://realpython.com/python-virtual-environments-a-primer/>`_.

For development installation you may optionally use `Virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_ for convenience.

You can create a virtual environment for the project using any of your favorite tools.


Project setup
-------------

Download the source code

.. code:: bash

    git clone https://github.com/tehamalab/datacompass.git


Go to project root

.. code:: bash

    cd datacompass


make sure your python virtual environment is active then use pip to install project requirements.

.. code:: bash

    pip install -r requirements/development.txt


Change your project settings according to your requirements.

Example; to enable debug mode

.. code:: bash

    # .env file

    DJANGO_DEBUG=True


Project setting which can modified using

- using system environment variables
- using environment variables written in ``.env`` file at the project root


To check if things are OK run

.. code:: bash

    ./manage.py check


Create database tables

.. code:: bash

    ./manage.py migrate


Create a superuser for admin access

.. code:: bash

    ./manage.py createsuperuser


**NOTE:** When you are executing ``manage.py ...`` commands make sure the vertualenv is active.


Starting the development server
--------------------------------

Django comes with an inbuilt server which can be used during development.
You shouldn't be using this server on production sites.

To start the development server go to your project root directory run

.. code:: bash

    ./manage.py runserver


Running tests
-------------

To run all tests against multiple versions of Django and Python, use tox_

.. code:: bash

    tox

To run basic unit tests

.. code:: bash

    ./manage.py test

To check Python coding style, use flake8_

.. code:: bash

    flake8

To automatically sort imports, use isort_

.. code:: bash

    isort -rc .


.. _tox: https://tox.readthedocs.io/en/latest/
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://isort.readthedocs.io/en/latest/
