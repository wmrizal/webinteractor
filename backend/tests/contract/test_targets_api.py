from __future__ import annotations


def build_target_payload(name: str = "Checkout flag") -> dict:
    return {
        "name": name,
        "baseUrl": "https://example.test",
        "pagePath": "/flags",
        "authProfile": "qa-session",
        "extractionRules": [
            {"key": "featureName", "selector": "#feature-name"},
            {"key": "featureState", "selector": "#feature-state"},
        ],
        "toggleRule": {
            "controlSelector": "#feature-toggle",
            "stateSelector": "#feature-state",
            "verificationMethod": "text-label",
        },
        "defaultDesiredState": "on",
    }


def test_target_crud_flow(contract_client):
    create_response = contract_client.post("/targets", json=build_target_payload())
    assert create_response.status_code == 201
    created_target = create_response.json()
    assert created_target["name"] == "Checkout flag"
    assert created_target["defaultDesiredState"] == "on"

    list_response = contract_client.get("/targets")
    assert list_response.status_code == 200
    listed_targets = list_response.json()
    assert len(listed_targets) == 1
    assert listed_targets[0]["id"] == created_target["id"]

    get_response = contract_client.get(f"/targets/{created_target['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["toggleRule"]["stateSelector"] == "#feature-state"

    update_response = contract_client.patch(
        f"/targets/{created_target['id']}",
        json={
            **build_target_payload(),
            "defaultDesiredState": "off",
            "pagePath": "/flags/beta",
        },
    )
    assert update_response.status_code == 200
    updated_target = update_response.json()
    assert updated_target["defaultDesiredState"] == "off"
    assert updated_target["pagePath"] == "/flags/beta"

    delete_response = contract_client.delete(f"/targets/{created_target['id']}")
    assert delete_response.status_code == 204

    missing_response = contract_client.get(f"/targets/{created_target['id']}")
    assert missing_response.status_code == 404
    assert missing_response.json()["code"] == "not_found"


def test_target_requires_https_and_rules(contract_client):
    invalid_response = contract_client.post(
        "/targets",
        json={
            **build_target_payload(),
            "baseUrl": "http://example.test",
            "extractionRules": [],
        },
    )
    assert invalid_response.status_code == 422
    assert invalid_response.json()["code"] == "validation_error"
