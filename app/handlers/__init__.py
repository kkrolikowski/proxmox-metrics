"""
Handlers package
================

This package maintains data flow inside application. It's used by application router

Functionality:
--------------

* Reading and parsing data from proxmox
* Generates Prometheus metrics
* Maintaining database operations
* Application healthchecks

Usage:
-------
Quick start example:

.. code-block:: python

    handler = Handler()
    app.add_routes([
        web.get("/", handler.healthcheck),
        web.post("/backups", handler.read_report_content),
        web.get("/metrics", handler.generate_prometheus_metrics)
    ])
"""