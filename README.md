# ExportLotusNotesCSV

Purpose
----------

Export data from Lotus Notes database(s) in standard format -> CSV. Also, export/save attachments and embedded objects as separate files in local directoryies with paths stored in CSV file.

Problem
----------

The problem with Lotus Notes document is the ability to insert virtually anything in Lotus Notes documents via attachment or embedding within document body.

This is a great feature, but exporting the data to a local file or another application is problematic as the embedded objects cannot be accessed within Lotus Notes programming environment (LotusScript, Java ..) One way to access the embedded objects is via the Domino Web server representation as it serves the documents as Web pages with embedded objects as images.

The LotusScript file (agent) exports all available data to CSV file. The Python script reads the CSV file (Document ID first column) and reads the document via Domino and Document ID (via View) and pulls images from the page (any images larger than 5KB) with images saved locally and path stored in CSV file.

Issues
----------
