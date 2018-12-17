import pytest
try:
    from devpi_server import __version__  # noqa
except ImportError:
    pytestmark = pytest.mark.skip("No devpi-server installed")
try:
    from devpi import __version__  # noqa
except ImportError:
    pytestmark = pytest.mark.skip("No devpi-client installed")


def test_manual_index_creation(capfd, devpi, getjson):
    devpi(
        "index", "-c",
        "+pr-manual",
        "type=merge",
        "bases=%s/dev" % devpi.user,
        code=200)
    (out, err) = capfd.readouterr()
    data = getjson("+pr-manual")["result"]
    assert data["type"] == "merge"
    assert data["state"] == "new"
    assert data["messages"] == []
    devpi(
        "index",
        "+pr-manual",
        "state=pending",
        "messages+=Please accept these updated packages",
        code=200)
    (out, err) = capfd.readouterr()
    data = getjson("+pr-manual")["result"]
    assert data["state"] == "pending"
    assert data["messages"] == ["Please accept these updated packages"]


def test_manual_index_creation_invalid_prefix(capfd, devpi):
    devpi(
        "index", "-c",
        "invalid_prefix",
        "type=merge",
        "bases=%s/dev" % devpi.user,
        code=400)
    (out, err) = capfd.readouterr()
    assert "indexname 'invalid_prefix' must start with '+pr-'." in out


def test_manual_index_creation_invalid_name(capfd, devpi):
    devpi(
        "index", "-c",
        "+pr-invalid[name]",
        "type=merge",
        "bases=%s/dev" % devpi.user,
        code=400)
    (out, err) = capfd.readouterr()
    assert "indexname 'invalid[name]' contains characters" in out


def test_index_creation(capfd, devpi, getjson):
    devpi(
        "pr",
        "20180717",
        "%s/dev" % devpi.user,
        code=200)
    (out, err) = capfd.readouterr()
    data = getjson("+pr-20180717")["result"]
    assert data["type"] == "merge"
    assert data["state"] == "new"
    assert data["messages"] == []
    devpi(
        "submit-pr",
        "20180717",
        "-m", "Please accept these updated packages",
        code=200)
    (out, err) = capfd.readouterr()
    data = getjson("+pr-20180717")["result"]
    assert data["state"] == "pending"
    assert data["messages"] == ["Please accept these updated packages"]


def test_pr_listing(capfd, devpi, getjson):
    # a new one
    devpi(
        "pr",
        "20181217",
        "%s/dev" % devpi.user,
        code=200)
    # a submitted one
    devpi(
        "pr",
        "20180717",
        "%s/dev" % devpi.user,
        code=200)
    devpi(
        "submit-pr",
        "20180717",
        "-m", "Please accept these updated packages",
        code=200)
    devpi(
        "list-prs",
        code=200)
