# DART for Digitized Content

Uses [DART Runner](https://github.com/APTrust/dart-runner) to create bags of digitized content and upload them to an S3 bucket.


## Requirements

The entire suite has the following system dependencies:
- Python 3 (tested on Python 3.9)
- [ArchivesSnake](https://pypi.org/project/ArchivesSnake/) (Python library) (0.9.1 or greater) 
- [DART Runner](https://github.com/APTrust/dart-runner)

## Configuration

This script requires a `local_settings.cfg` file. For an example of the sections and keys required, see [local_settings.cfg.example](local_settings.cfg.example) in this repository.

The config file includes a path to Workflow JSON to be used with DART Runner; this must be exported from the DART GUI. [For more information see the DART documentation.](https://aptrust.github.io/dart-docs/users/workflows/#exporting-a-workflow)

The config file includes a path to an already processed list, which is a text file that the script automatically appends to when a bag has been completed. This ensures that a directory is not run over twice. The script automatically ignores directory names that are not the same number of characters as an RAC ASpace RefID, so these directories do not need to be added to the already processed list.

## Quick start

After cloning this repository and creating `local_settings.cfg`, run `dart_pipeline.py` with the list of rights IDs as arguments. E.g.,

```
$ python dart_pipeline.py -l 3 9
```

### Expected structure of original files

This pipeline expects to be pointed at a directory containing subdirectories (named by ArchivesSpace ref ids) for archival object components, each of which contains a subdirectory named `master` containing original TIFF files as well as a `service_edited` directory containing a multi-page PDF file. Optionally, there may be a `master_edited` subdirectory which contains mezzanine TIFF files.

```
/directory
    /refid1
        /master
            abcde_001.tif
            abcde_002.tif
            abcde_003.tif
        /master_edited
            abcde_001.tif
            abcde_002.tif
            abcde_003.tif
        /service_edited
            abcde.pdf
    /refid2
        /master
            edcba_001.tif
            edcba_002.tif
            edcba_003.tif
        /master_edited
            edcba_001.tif
            edcba_002.tif
            edcba_003.tif
        /service_edited
            edcba.pdf
```

## Logging

The pipeline will log to a file named `bag_creator.log` located in the same directory as the `dart_pipeline.py` script. Level and format can be configured by altering the settings in the `__init__` method of the `DigitizationPipeline` class.

## Tests

This library comes with unit tests. To quickly run tests, run `tox` from this directory.

