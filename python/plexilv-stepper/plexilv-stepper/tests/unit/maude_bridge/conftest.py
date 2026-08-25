import pytest
import maude
import os

@pytest.fixture(scope="module")
def maude_module():
    # Initialize Maude and load the environment module
    maude.init()

    # We need to construct the path to semantics/src/plexil-v.maude
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
    env_file = os.path.join(base_dir, "semantics", "src", "plexil-v.maude")

    try:
        maude.load(env_file)
        mod = maude.getModule('PLEXIL-V')
        if not mod:
            pytest.skip("Could not find PLEXIL-V module in maude after loading.")
        return mod
    except Exception as e:
        pytest.skip(f"Could not load Maude environment for tests: {e}")