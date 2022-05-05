import logging
from configparser import ConfigParser
from pathlib import Path
from shutil import rmtree

import shortuuid

from .archivesspace import ArchivesSpaceClient
from .aws_upload import S3Uploader
from .bag_creator import BagCreator
from .helpers import copy_tiff_files, format_aspace_date, get_access_pdf


class DigitizationPipeline:

    def __init__(self):
        self.config = ConfigParser()
        current_path = Path(__file__).parents[0].resolve()
        config_path = Path(current_path, "local_settings.cfg")
        self.config.read(str(config_path))
        logging.basicConfig(
            datefmt='%m/%d/%Y %I:%M:%S %p',
            format='%(asctime)s %(message)s',
            level=logging.INFO,
            handlers=[
                logging.FileHandler("bag_creator.log"),
                logging.StreamHandler()
            ])

        self.root_dir = self.config.get("Directories", "root_dir")
        self.tmp_dir = self.config.get("Directories", "tmp_dir")
        self.as_client = ArchivesSpaceClient(
            self.config["ArchivesSpace"]["baseurl"],
            self.config["ArchivesSpace"]["username"],
            self.config["ArchivesSpace"]["password"],
            self.config["ArchivesSpace"]["repository"])
        self.s3_uploader = S3Uploader(
            self.config["AWS"]["region_name"],
            self.config["AWS"]["access_key"],
            self.config["AWS"]["secret_key"],
            self.config["AWS"]["bucket"])
        self.processed_filepath = self.config["Other"]["processed_list"]
        self.workflow_json = self.config["DART"]["workflow_json"]

    def run(self, rights_ids):
        logging.info("Starting run...")
        self.processed_list = self.get_processed_list()
        refids = [
            d.name for d in Path(
                self.root_dir).iterdir() if Path(
                self.root_dir,
                d).iterdir() and len(
                d.name) == 32 and d.name not in self.processed_list]
        for refid in refids:
            try:
                ao_uri = self.as_client.get_uri_from_refid(refid)
                dimes_identifier = shortuuid.uuid(ao_uri)
                pdf_path = get_access_pdf(
                    Path(self.root_dir, refid, "service_edited"))
                S3Uploader().upload_pdf_to_s3(
                    pdf_path, f"pdfs/{dimes_identifier}")
                logging.info(
                    f"PDF successfully uploaded: {dimes_identifier}.pdf")
                dir_to_bag = Path(self.tmp_dir, refid)
                list_of_files = self.add_files_to_dir(refid, dir_to_bag)
                begin_date, end_date = format_aspace_date(
                    self.as_client.find_closest_dates(ao_uri))
                created_bag = BagCreator().run(
                    refid, ao_uri, begin_date, end_date, rights_ids, list_of_files)
                logging.info(f"Bag successfully created: {created_bag}")
                rmtree(dir_to_bag)
                with open(self.processed_filepath, "a") as f:
                    f.write(f"\n{refid}")
                logging.info(
                    f"Directory {dir_to_bag} successfully removed")
            except Exception as e:
                logging.error(f"Error for ref_id {refid}: {e}")

    def add_files_to_dir(self, refid, dir_to_bag):
        master_tiffs = copy_tiff_files(
            Path(self.root_dir, refid, "master"), dir_to_bag)
        master_edited_tiffs = []
        if Path(self.root_dir, refid, "master_edited").is_dir():
            master_edited_tiffs = copy_tiff_files(
                Path(
                    self.root_dir, refid, "master_edited"), Path(
                    self.tmp_dir, refid, "service"))
        return master_tiffs + master_edited_tiffs

    def get_processed_list(self):
        """Parses a text file whose filepath is provided in the config.

        Returns a list
        """
        processed_list = open(self.processed_filepath).readlines()
        return [i.replace('\n', '') for i in processed_list]
