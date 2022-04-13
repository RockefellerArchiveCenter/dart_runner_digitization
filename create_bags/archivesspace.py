from asnake.client import ASnakeClient


class ArchivesSpaceClient:
    def __init__(self, baseurl, username, password, repo):
        self.client = ASnakeClient(
            baseurl=baseurl,
            username=username,
            password=password)
        self.repo = repo

    def get_uri_from_refid(self, refid):
        """Use find_by_id endpoint to return the URI of an archival object."""
        find_by_refid_url = f"repositories/{self.repo}/find_by_id/archival_objects?ref_id[]={refid}"
        results = self.client.get(find_by_refid_url).json()
        if len(results.get("archival_objects")) == 1:
            return results['archival_objects'][0]['ref']
        else:
            raise Exception("{} results found for search {}".format(
                len(results.get("archival_objects")), find_by_refid_url))  # TODO: make it clear that we want one result

    def get_ao_data(self, ao_uri):
        """Gets data for an archival object, including ancestors."""
        return self.client.get(
            ao_uri, params={
                "resolve": ["ancestors"]}).json()
