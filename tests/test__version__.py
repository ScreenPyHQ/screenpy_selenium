from screenpy_selenium import __version__


def test_metadata() -> None:
    assert __version__.__title__ == "screenpy_selenium"
    assert __version__.__license__ == "MIT"
    assert __version__.__author__ == "Perry Goy"
