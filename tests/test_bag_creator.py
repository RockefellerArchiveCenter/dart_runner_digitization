from create_bags.bag_creator import BagCreator


def test_construct_job_params():
    bag_creator = BagCreator("workflow.json", "tmp/dir")
    bag_creator.refid = "jsdfjp90fsfjlk"
    bag_creator.ao_uri = "/whatever"
    rights_ids = [2, 4]
    dates = ("1940-01-01", "1940-06-01")
    files = ["/path/to/file1.tif", "/path/to/file2.tif"]
    job_params = bag_creator.construct_job_params(
        rights_ids, files, dates[0], dates[1])
    assert isinstance(job_params, dict)
    for tag in job_params["tags"]:
        if tag["tagName"] == "Start-Date":
            assert tag["userValue"] == "1940-01-01"
    assert len(job_params["tags"]) == 6


def test_run_method(mocker):
    mocker.patch('create_bags.bag_creator.BagCreator.create_dart_job')
    create_bag = BagCreator("workflow.json", "tmp/dir").run(
        "329d56f6f0424bfb8551d148a125dabb", "ao_uri", "1900-01-01", "1910-12-31", [2, 4], ["/path/to/file1.tif", "/path/to/file2.tif"])
    assert create_bag
