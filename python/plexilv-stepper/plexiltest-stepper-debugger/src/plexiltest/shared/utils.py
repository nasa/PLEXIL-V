import sys
import ctypes
import importlib.resources
from pathlib import Path

def load_stepper_library():
    """
    Loads the PlexilStepper C++ library, handling both standard installs
    (production) with 'pip install .' and editable installs (development) with
    'pip install -e .'
    """
    if sys.platform == "darwin":
        lib_name = "libPlexilStepper.dylib"
    elif sys.platform.startswith("win"):
        lib_name = "PlexilStepper.dll"
    elif sys.platform.startswith("linux"):
        lib_name = "libPlexilStepper.so"
    else:
        raise NotImplementedError(f"Unsupported operating system: {sys.platform}")

    # Try Production Location (Standard 'pip install .')
    # This looks in the active Python environment's site-packages/plexiltest/cext/
    # where cext should be the install location set for the C++ code in CMakeLists.txt
    try:
        resource = importlib.resources.files("plexiltest.cext") / lib_name
        with importlib.resources.as_file(resource) as lib_path:
            if lib_path.exists():
                return ctypes.CDLL(str(lib_path))
    except Exception:
        pass  # If it fails, we assume we are in development mode

    # Try Development Location (Editable 'pip install -e .')
    # If running interactively (REPL), __file__ doesn't exist, so fallback to current dir.
    if '__file__' in globals():
        current_file = Path(__file__).resolve()
        # Navigate up to project root
        root_dir = current_file.parent.parent.parent
    else:
        root_dir = Path.cwd()

    dev_path = root_dir / "build" / "cpp" / lib_name

    if dev_path.exists():
        return ctypes.CDLL(str(dev_path))

    # If neither location worked, raise an error
    raise FileNotFoundError(
        f"Could not find {lib_name}.\n"
        f"Ensure the project is built. Checked development path:\n  {dev_path}"
    )


def get_library_filename(base_name: str) -> str:
    """
    Generates the platform-specific library filename.
    Example: 'mylib' -> 'mylib.dll' (Win), 'libmylib.so' (Linux), 'libmylib.dylib' (Mac)
    """
    if sys.platform.startswith("win"):
        return f"{base_name}.dll"

    elif sys.platform.startswith("linux"):
        return f"lib{base_name}.so"

    elif sys.platform == "darwin":
        return f"lib{base_name}.dylib"

    else:
        raise NotImplementedError(f"Unsupported operating system: {sys.platform}")
