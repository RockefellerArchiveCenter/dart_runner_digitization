# DART for Digitized Content

Uses [DART Runner](https://github.com/APTrust/dart-runner) to create bags of digitized content that will be sent to [Zorya](https://github.com/RockefellerArchiveCenter/zorya) and upload PDF files to an S3 bucket.


## Requirements

The entire suite has the following system dependencies:
- Python 3 (tested on Python 3.10)
- ArchivesSnake (Python library) (0.9.1 or greater)
- [DART](https://github.com/APTrust/dart)

## Configuration

This script requires a `local_settings.cfg` file. For an example of the sections and keys required, see [local_settings.cfg.example](local_settings.cfg.example) in this repository

## Quick start

After cloning this repository and creating `local_settings.cfg`, run `dart_pipeline.py` with the directory containing original files (in directories with ArchivesSpace RefIDs), a temporary directory, and the list of rights IDs as arguments. E.g.,

```
$ python dart_pipeline.py /path/to/original/files /path/to/tmp -l 3 9
```

### Expected structure of original files

This pipeline expects to be pointed at a directory containing subdirectories (named by ArchivesSpace ref ids) for archival object components, each of which contains a subdirectory named `master` containing original TIFF files as well as a `service_edited` directory containing a multi-page PDF file. Optionally, there may be a `master_edited` subdirectory which contains mezzanine TIFF files.


## Tests

This library comes with unit tests. To quickly run tests, run `tox` from this directory.

