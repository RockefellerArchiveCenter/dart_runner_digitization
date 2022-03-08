from pathlib import Path
from shutil import copy2


def format_aspace_date(dates):
    '''
    Formats ASpace dates so that they can be parsed by Aquila. If assumes beginning of month or year if a start date, and end of month or year if an end date.

    Args:
        dates (dict): ArchivesSpace date JSON

    Returns:
        Tuple of a begin date and end date in format YYYY-MM-DD
    '''
    begin_date = dates['begin']
    end_date = False
    if dates['date_type'] == 'single':
        end_date = begin_date
    else:
        end_date = dates['end']
    if len(begin_date) == 4:
        begin_date = "{}-01-01".format(begin_date)
    elif len(begin_date) == 7:
        begin_date = "{}-01".format(begin_date)
    if len(end_date) == 4:
        end_date = "{}-12-31".format(end_date)
    elif len(end_date) == 7:
        end_date = "{}-31".format(end_date)
    return begin_date, end_date


def get_closest_dates(archival_object):
    '''
    Takes JSON for an archival object and returns a date from that object or its nearest ancestor with a date.

    Args:
        archival_object: JSON for AS archival object with resolved ancestors

    Returns:
        Dictionary for a date JSON
    '''
    # TODO: error handling
    dates = False
    if archival_object.get("dates"):
        dates = archival_object['dates'][0]
    else:
        for a in archival_object.get("ancestors"):
            if a.get("_resolved").get("dates"):
                dates = a['_resolved']['dates'][0]
                break
    return dates


def create_tag(tag_name, user_value, tag_file="bag-info.txt"):
    """Return dictionary for a custom DART tag"""
    return {"tagFile": tag_file, "tagName": tag_name, "userValue": user_value}


def matching_files(directory, suffix=None, prepend=False):
    """Get a list of files that start with a specific prefix, optionally removing
    any files that end in `_001`.
    Args:
        directory (str): The directory containing files.
        suffix (str): A suffix (file extension) to match filenames against.
        prepend (bool): Add the directory to the filepaths returned
    Returns:
        files (lst): a list of files that matched the identifier.
    """
    HIDDEN_FILES = (
        ".", "Thumbs")  # files which start with these strings will be skipped
    files = sorted([f for f in directory.iterdir() if (
        directory.joinpath(f).is_file() and not str(f.name).startswith(HIDDEN_FILES))])
    if suffix:
        files = sorted([f for f in files if str(f.name).endswith(suffix)])
    return [directory.joinpath(f) for f in files] if prepend else files


def copy_tiff_files(source_dir, dest_dir):
    """Takes Path objects"""
    tiff_files = matching_files(source_dir, suffix="tif")
    if not dest_dir.is_dir():
        dest_dir.mkdir(parents=True)
    copied_tiffs = []
    for tiff in tiff_files:
        copy2(tiff, Path(dest_dir, tiff.name))
        copied_tiffs.append(str(Path(dest_dir, tiff.name)))
    return copied_tiffs


def get_access_pdf(pdf_dir):
    """Gets a PDF file from a directory. Fails if there are multiple PDF files

    Args:
        pdf_dir (Path obj): directory containing PDF file
    """
    pdf_files = [f for f in pdf_dir.iterdir() if f.is_file(
    ) and not f.name.startswith(".") and f.name.endswith(".pdf")]
    if len(pdf_files) == 0:
        raise Exception("No PDF file found")
    elif len(pdf_files) > 1:
        raise Exception("More than one PDF file found")
    else:
        return pdf_files[0]
