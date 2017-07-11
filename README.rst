OpenDNA Autobahn-Python Runners
===============================

The OpenDNA Autobahn-Python Runners package provides a number of scripts that
can be used to launch Autobahn-Python components and connect them to a WAMP
router.


Contents
--------

1. Installation
2. Usage
3. Command-line Parameters
4. Twisted Runner
5. AsyncIO Runner
6. AsyncIO Multi-Runner
7. Roadmap


Installation
------------
``pip install autobahn-python-runners``

When the package is installed it will create the following scripts in your
Python environment's scripts path:

- ``run_twisted_component``
- ``run_asyncio_component``
- ``run_asyncio_components``

Optionally, you ``pip install uvloop`` for enhanced event-loop perforance with
the AsyncIO runners. You will need ``libuv`` with installed in order to do this.

Usage
-----
Usage can be achieved through one of two methods:

0. Execute one of the scripts created during installation
1. Execute one of the modules using the standard ``python -m`` method


Command-line Parameters
-----------------------
The following command-line parameters are supported by all of the runners
included in this package:

Required parameters:

- ``-c`` or ``--component`` is a fully-qualified path to an Autobahn-Python
  component class E.g. ``some_org.some_package.some_module.SomeClass``. Can be
  alternatively specified using the ``WAMP_COMPONENT`` enviornment variable
- ``-u`` or ``--url`` is a URL for the WAMP router to connect to
  E.g. ``ws://localhost:8080``. Can be alternatively specified using the
  ``WAMP_URL`` environment variable
- ``-r`` or ``--realm`` is a Realm on the WAMP router you are connecting to. E.g.
  ``my.realm.name``. Can be alternatively specified using the ``WAMP_REALM``
  environment variable

Optional parameters:

- ``-e`` or ``--extra-file`` is a path to a JSON file which will be loaded and
  supplied to the component class instance via the config parameter of the
  class constructor method
- ``-s`` or ``--use-ssl`` is value that will be cast to a boolean and used to
  specify whether or not SSL should be used for the WS connection. This
  parameter is usually unnecessary as the decision to use SSL is usually
  determined by the choice of WS protocol for the WAMP router URL. It is made
  available here simply for the purposes of completeness
- ``-l`` or ``--loglevel`` is used to specify the logging level used by the runner.
  Defaults to ``info`` with other permitted values being ``critical``, ``error``,
  ``warning`` and ``debug``
- ``--serializers`` is a fully qualified path to an Autobahn-Python serializer
  class. This parameter may be specified multiple times


Twisted Runner
--------------
The Twisted runner is provided by the ``opendna.autobahn.runners.run_twisted``
module and can be used to run components that derive from the
``autobahn.twisted.ApplicationSession`` class.


AsyncIO Runner
--------------
The AsyncIO runner is provided by the ``opendna.autobahn.runners.run_asyncio``
module and can be used to run components that derive from the
``autobahn.asyncio.ApplicationSession`` class.


AsyncIO Multi-Runner
--------------------
The AsyncIO multi-runner is provided by the ``opendna.autobahn.runners.multirun_asyncio``
module and can be used to run multiple components that derive from the
``autobahn.asyncio.ApplicationSession`` class within a single Python process.

These components will run within a single event-loop but each component will
establish a separate WS connection to the WAMP router.

The AsyncIO multi-runner makes the following changes to the parameter options:

- ``-c``/``--component`` may be passed multiple times in order to specify
  multiple component classes. Each class instance will connect to the same
  WAMP router and realm specified using the relevant parameters
- ``-e``/``--extra-file`` can still be used but behaves slightly differently in
  that it expects that the JSON file will contain a plain object where each
  key is a component class as specified using the ``-c``/``--component`` parameter
  and the value associated with each key is a plain object of data to be supplied
  to the relevant component class instance via the config parameter of the
  class constructor method


Roadmap
-------

Done:

- Twisted runner
- AsyncIO runner
- AsyncIO multi-runner
- Basic documentation
- uvloop support for AsyncIO runners

Todo:

- Tests

Maybe:

- Twisted multi-runner
- Option for multi-runners to transparently restart crashed components
