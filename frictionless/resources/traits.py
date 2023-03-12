from .table import TableResource
from .package import PackageResource
from .resource import ResourceResource


Convertible = (TableResource,)
Extractable = (TableResource, PackageResource, ResourceResource)
Indexable = (TableResource, PackageResource, ResourceResource)
Transformable = (TableResource, PackageResource, ResourceResource)
