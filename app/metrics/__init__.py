"""
Prometheus metrics package
==========================

This packege is responsible for making a prometheus metrics out of the supplied
data. Those metrics will be consumed by prometheus.

Functionality:
--------------

* Generates prometheus metrics

Quick example:
--------------

.. code-block:: python

  from prometheus_client import Gauge

  backup_size = Gauge(
    "backup_size_bytes",
    "Backup size for VM",
    ["vmid", "name"]
  )

  backup_size.labels(vmid, name).set("20000000")
"""