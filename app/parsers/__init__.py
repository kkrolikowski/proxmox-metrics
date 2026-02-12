"""
Parsers package
================

This package is responsible for transforming raw data to a structured JSON object,
that is ready to be saved in MongoDB database

Functionality
--------------

* Transforming raw data string into JSON object
* Implementing helper functions to produce unified values such as:
  
  * Megabytes and Gigabytes to bytes
  * hours, minutes to seconds

Quick start:
-------------

.. code-block:: python

  pr = ProxmoxReport(rawdata)
  backup_info = pr.report_parser()
"""