from typing import Optional
from .control import ZenodoControl
from ...resource import Resource
from ...package import Package
from ...package import Manager
from ... import helpers


class ZenodoManager(Manager[ZenodoControl]):

    # Read

    # TODO: implement
    def read_catalog(self):
        pass

    # TODO: improve
    def read_package(self, *, record: Optional[str] = None):
        pyzenodo3 = helpers.import_from_extras("pyzenodo3", name="zenodo")
        client = pyzenodo3.Zenodo()
        record = record or self.control.record
        assert record
        dataset = client.get_record(record)
        package = Package()
        package.title = dataset.data["metadata"]["title"]
        for file in dataset.data["files"]:
            path = file["links"]["self"]
            if path.endswith(("datapackage.json", "datapackage.yaml")):
                return Package.from_descriptor(path)
            package.add_resource(Resource(path=path))
        return package

    # Write
    # TODO: implement