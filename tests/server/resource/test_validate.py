from frictionless import Resource


# General


def test_server_resource_validate(api_client):
    resource = Resource(path="data/table.csv")
    response = api_client.post(
        "/resource/validate", json={"resource": resource.to_descriptor()}
    )
    assert response.status_code == 200
    assert response.json()["report"]["valid"] is True
