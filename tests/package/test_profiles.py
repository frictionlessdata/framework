import pytest
from frictionless import Package, Resource, system


# General


def test_package_profiles_invalid_local():
    profile = "data/profiles/camtrap.json"
    resource = Resource(name="table", path="data/table.csv")
    package = Package(resources=[resource], profiles=[profile])
    assert len(package.list_metadata_errors()) == 5
    for error in package.list_metadata_errors():
        assert "required" in error.message


def test_package_profiles_invalid_local_from_descriptor():
    profile = "data/profiles/camtrap.json"
    resource = Resource(name="table", path="data/table.csv")
    package = Package({"resources": [resource.to_descriptor()], "profiles": [profile]})
    assert len(package.list_metadata_errors()) == 5
    for error in package.list_metadata_errors():
        assert "required" in error.message


@pytest.mark.vcr
def test_package_external_profile_invalid_remote():
    profile = (
        "https://raw.githubusercontent.com/tdwg/camtrap-dp/main/camtrap-dp-profile.json"
    )
    resource = Resource(name="table", path="data/table.csv")
    package = Package(resources=[resource], profiles=[profile])
    assert len(package.list_metadata_errors()) == 5
    for error in package.list_metadata_errors():
        assert "required" in error.message


@pytest.mark.vcr
def test_package_external_profile_invalid_remote_from_descriptor():
    profile = (
        "https://raw.githubusercontent.com/tdwg/camtrap-dp/main/camtrap-dp-profile.json"
    )
    resource = Resource(name="table", path="data/table.csv")
    package = Package({"resources": [resource.to_dict()], "profiles": [profile]})
    assert len(package.list_metadata_errors()) == 5
    for error in package.list_metadata_errors():
        assert "required" in error.message


# Legacy


def test_package_profiles_from_descriptor_standards_v1():
    profile = "data/profiles/camtrap.json"
    resource = Resource(name="table", path="data/table.csv")
    package = Package({"resources": [resource.to_descriptor()], "profile": profile})
    assert len(package.list_metadata_errors()) == 5
    for error in package.list_metadata_errors():
        assert "required" in error.message


def test_package_profiles_to_descriptor_standards_v1():
    profile = "data/profiles/camtrap.json"
    resource = Resource(name="table", path="data/table.csv")
    package = Package(resources=[resource], profiles=[profile])
    with system.use_standards_version("v1"):
        descriptor = package.to_descriptor()
        assert descriptor["profile"] == profile
