alfred-client |build-status|
============================

.. |build-status| image:: https://travis-ci.org/coyote240/alfred-client.svg?branch=master
    :target: https://travis-ci.org/coyote240/alfred-client
    

A Python client library for the Almighty Lightweight Fact Remove Exchange
Daemon (A.L.F.R.E.D.) by Open-Mesh_

.. _Open-Mesh: https://open-mesh.org


Installation
------------

Install the application by setting up and activating a virtual environment,
and then running::

  $ python3 -m venv ./env
  $ source ./env/bin/activate
  $ python setup.py install

And then run the application by calling the provided entry point::

  alfred_client --config=config.py

