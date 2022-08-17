import json
import subprocess

from .helpers import create_tag


class BagCreator:

    def __init__(self, dart_command, workflow_json, tmp_dir, job_params_file):
        self.dart_command = dart_command
        self.workflow_json = workflow_json
        self.tmp_dir = tmp_dir
        self.job_params_file = job_params_file

    def run(self, refid, ao_uri, begin_date, end_date, rights_ids, files):
        """Uses DART Runner to create a bag.

        Args:
            refid (str): ArchivesSpace RefId
            ao_uri (str): ArchivesSpace URI
            begin_date (str): begin date
            end_date (str): end date
            rights_ids (array): list of rights IDs (which are integers)
            files (array): list of full filepaths to include in bag
        """
        try:
            self.refid = refid
            self.ao_uri = ao_uri
            self.job_params = self.construct_job_params(
                rights_ids, files, begin_date, end_date)
            self.create_dart_job()
            return self.refid
        except Exception as e:
            raise(e)

    def construct_job_params(self, rights_ids, files, begin_date, end_date):
        """Formats information for DART job parameters.

        Args:
            rights_ids (array): list of rights ids
            files (array): list of full filepaths
            begin_date (string): begin date
            end_date (string): end date

        Returns a dictionary
        """
        job_params = {"packageName": "{}.tar".format(self.refid),
                      "files": files,
                      "tags": [{"tagFile": "bag-info.txt",
                                "tagName": "ArchivesSpace-URI",
                                "value": self.ao_uri},
                               {"tagFile": "bag-info.txt",
                                "tagName": "Start-Date",
                                "value": begin_date},
                               {"tagFile": "bag-info.txt",
                                "tagName": "End-Date",
                                "value": end_date},
                               {"tagFile": "bag-info.txt",
                                "tagName": "Origin",
                                "value": "digitization"}]}
        for rights_id in rights_ids:
            job_params['tags'].append(create_tag("Rights-ID", str(rights_id)))
        return job_params

    def create_dart_job(self):
        """Runs a DART job."""
        with open(self.job_params_file, "w") as param_file:
            json.dump(self.job_params, param_file)
        cmd = f"{self.dart_command} --workflow={self.workflow_json} --output-dir={self.tmp_dir} < {self.job_params_file}"
        subprocess.run(cmd, shell=True, check=True)
