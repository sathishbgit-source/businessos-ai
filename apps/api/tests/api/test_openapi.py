from app.main import app


def test_openapi_metadata():
    schema = app.openapi()

    assert schema["info"]["title"] == "BusinessOS AI"
    assert schema["info"]["version"] == "0.1.0"

    assert (
        schema["info"]["description"]
        == (
            "BusinessOS AI API for authentication, organisations, "
            "invitations, notifications, and platform services."
        )
    )


def test_openapi_tags():
    schema = app.openapi()

    tags = {
        tag["name"]: tag["description"]
        for tag in schema["tags"]
    }

    assert set(tags) == {
        "Health",
        "Authentication",
        "Organisations",
        "Invitations",
        "Notifications",
        "Payments",
    }


def test_openapi_contains_api_routes():
    schema = app.openapi()

    paths = schema["paths"]

    assert "/api/v1/health" in paths
    assert "/api/v1/auth/register" in paths
    assert "/api/v1/auth/login" in paths
    assert "/api/v1/auth/me" in paths
    assert "/api/v1/organisations" in paths
    assert "/api/v1/invitations/accept" in paths
    assert "/api/v1/notifications" in paths
    assert (
        "/api/v1/organisations/{organisation_id}/payments"
        in paths
    )
    assert (
        "/api/v1/organisations/{organisation_id}/payments/{payment_id}"
        in paths
    )


def test_openapi_documents_rate_limiting():
    schema = app.openapi()

    operation = schema["paths"]["/api/v1/auth/login"]["post"]

    assert "429" in operation["responses"]
    assert (
        operation["responses"]["429"]["description"]
        == "Too many requests. Rate limit exceeded."
    )


def test_openapi_has_bearer_security_scheme():
    schema = app.openapi()

    security_schemes = schema["components"]["securitySchemes"]

    assert "HTTPBearer" in security_schemes
    assert security_schemes["HTTPBearer"]["type"] == "http"
    assert security_schemes["HTTPBearer"]["scheme"] == "bearer"
