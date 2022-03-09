import json
from subprocess import PIPE, Popen

from .helpers import create_tag


class BagCreator:

    def __init__(self, workflow_json, tmp_dir):
        self.workflow_json = workflow_json
        self.tmp_dir = tmp_dir

    def run(self, refid, ao_uri, begin_date, end_date, rights_ids, files):
        """
        Args:
        refid (str)
        rights_ids (array)
        """
        # directory_to_bag = "some directory"
        self.refid = refid
        self.ao_uri = ao_uri
        self.job_params = self.construct_job_params(
            rights_ids, files, begin_date, end_date)
        self.create_dart_job()
        return self.refid

    def construct_job_params(self, rights_ids, files, begin_date, end_date):
        """Formats information for DART job parameters

        Args:
            rights_ids (array): list of rights ids
            files (array): list of full filepaths
            dates (tuple): begin and end dates

        Returns a dictionary"""

        job_params = {"packageName": "{}.tar".format(self.refid),
                      "files": files,
                      "tags": [{"tagFile": "bag-info.txt",
                                "tagName": "ArchivesSpace-URI",
                                "userValue": self.ao_uri},
                               {"tagFile": "bag-info.txt",
                                "tagName": "Start-Date",
                                "userValue": begin_date},
                               {"tagFile": "bag-info.txt",
                                "tagName": "End-Date",
                                "userValue": end_date},
                               {"tagFile": "bag-info.txt",
                                "tagName": "Origin",
                                "userValue": "digitization"}]}
        for rights_id in rights_ids:
            job_params['tags'].append(create_tag("Rights-ID", str(rights_id)))
        return job_params

    def create_dart_job(self):
        """Runs a DART job"""
        job_json_input = (json.dumps(self.job_params) + "\n").encode()
        cmd = f"dart-runner --workflow={self.workflow_json} --output-dir={self.tmp_dir}"
        child = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
        stdout_data, stderr_data = child.communicate(job_json_input)
        if child.returncode != 0:
            stdout_message = stdout_data.decode('utf-8') if stdout_data else ""
            stderr_message = stderr_data.decode('utf-8') if stderr_data else ""
            raise Exception(stdout_message, stderr_message)
