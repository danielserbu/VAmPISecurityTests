def pytest_addoption(parser):
    parser.addoption("--vulnerable", action="store", default=True)