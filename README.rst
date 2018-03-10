alfred-client |build-status|
============================

.. |build-status| image:: https://travis-ci.org/coyote240/alfred-client.svg?branch=master
    :target: https://travis-ci.org/coyote240/alfred-client
    

A Python client library for the Almighty Lightweight Fact Remove Exchange
Daemon (A.L.F.R.E.D.) by Open-Mesh_

.. _Open-Mesh: https://open-mesh.org


Dependencies
------------

This project relies upon alfred_ which in turn depends upon a configured 
batman-adv_ environment.

.. _alfred: https://open-mesh.org/projects/alfred/wiki

.. _batman-adv: https://www.open-mesh.org/projects/batman-adv/wiki

*See instructions for installing batctl and alfred below*


Installation
------------

Install the application by setting up and activating a virtual environment,
and then running::

  $ python3 -m venv ./env
  $ source ./env/bin/activate
  $ python setup.py install

Make a copy of the example config file and edit as needed::

  $ cp alfred_client/example_config.py alfred_client/config.py

And then run the application by calling the provided entry point::

  alfred_client --config=config.py

*To have alfred_client start at boot, follow the System startup instructions below*


Installing *batctl* and *alfred*
--------------------------------

The development of this project has focused nearly entirely on the Raspberry Pi
platform. In order to build and run *batctl* and *alfred*, you will need to install
the following:

* make
* gcc
* git
* python3-dev
* python3-venv
* libnl-3-dev
* libnl-genl-3-dev
* libcap-dev
* libgps-dev
* gpsd (optional, assuming we add gps modules later)


Build *batctl*
==============

Pull and build *batctl* from the OpenMesh source repository::

  $ git clone https://git.open-mesh.org/batctl.git
  $ cd batctl
  $ sudo make install


Build *alfred*
==============

Pull and build *alfred* from the OpenMesh source repository::

  $ git clone https://git.open-mesh.org/alfred.git
  $ cd alfred
  $ sudo make install


System startup
==============

To have *alfred* and *batadv-vis* start at system boot, unit files have been
included in with this project in the ``config`` directory. At a minimum, this
project requires that the ``alfred`` service is running. To enable visualization
data to be shared, the ``batadv-vis`` service must also be running.

On Raspbian (or Debian), perform these steps for each service you wish to run::

  $ sudo cp config/alfred.service /etc/systemd/system/alfred.service
  $ sudo systemctl daemon-reload
  $ sudo systemctl enable alfred.service
  $ sudo systemctl start alfred.service


Configuring the Raspberry Pi to run this project
------------------------------------------------

Add the ``batman-adv`` module to /etc/modules::

  sudo echo "batman-adv" >> /etc/modules

Configure ethernet for IPv4, DHCP. This will be our outside interface to the mesh,
as well as our maintenance interface.

On Raspbian (or Debian) edit ``/etc/network/interfaces`` to contain::

  auto eth0
  allow-hotplug eth0
  iface eth0 inet dhcp

Configure your wireless interface and attach the *batman-adv* interface::

  auto wlan0
  iface wlan0 inet6 manual
    wireless-channel 1
    wireless-essid <your essid>
    wireless-mode ad-hoc
    wireless-ap 02:12:34:56:78:9A
    pre-up ifconfig wlan0 mtu 1532

  auto bat0
  iface bat0 inet6 auto
  pre-up /usr/local/sbin/batctl if add wlan0

After completing this step, you may bring up the configured interfaces::

  sudo systemctl restart networking
