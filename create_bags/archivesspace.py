from asnake.client import ASnakeClient
from asnake.utils import find_closest_value


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
            raise Exception("{} results found for search {}. Expected one result.".format(
                len(results.get("archival_objects")), find_by_refid_url))

    def find_closest_dates(self, ao_uri):
        """Uses find_closest_value from ArchivesSnake utils to get closest date.

        Args:
            ao_uri (str): archival object uri
        """
        all_dates = find_closest_value(ao_uri, "dates", self.client)
        return all_dates[0]
