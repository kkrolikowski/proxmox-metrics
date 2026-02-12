"""
MongoDB client package
==========================

This package maintains all the connection logic with MongoDB.

Implemented functionality
-------------------------

* Working on a collection. Reading and writing data.
* Maintaining data retention (parameter ``daysold``)

Usage:
-------
Quick start example:

.. code-block:: python

    db = DB({
        "url": mongo_url,
        "timeout": mongo_timeout * 1000,
        "collection": collecttion,
        "mongo_history_days": mongo_hisory_days
    })
    db.insert({"sensor": "cpu", "value": 45})
"""