import os
import sys
import subprocess
#from PySide2 import QtCore
from PySide6 import QtCore

def is_webengine_functional():
    # 1. Check if module is even importable
    try:
        #from PySide2 import QtWebEngineWidgets
        from PySide6 import QtWebEngineWidgets

    except ImportError:
        print("Here fail #1")
        return False

    # 2. Locate the helper executable
    # Qt searches for this file to render web content
    process_path = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.LibraryExecutablesPath)
    print("process_path =", process_path)

    filename = "QtWebEngineProcess.exe" if sys.platform == "win32" else "QtWebEngineProcess"
    full_path = os.path.join(process_path, filename)

    if not os.path.exists(full_path):
        # Path might be different in virtualenvs or bundled apps
        # fallback check in standard PySide2/PySide6 path

        #import PySide2
        import PySide6
        #full_path = os.path.join(os.path.dirname(PySide2.__file__), "Qt", "bin", filename)
        full_path = os.path.join(os.path.dirname(PySide6.__file__), "Qt", "bin", filename)

    if not os.path.exists(full_path):
        print("Here fail #2")
        return False

    print("Here YES")
    return True

# --- MAIN LOGIC ---
if is_webengine_functional():
    print("Environment healthy. Launching Full Mode...")
    # use the embedded report viewer

else:
    print("QtWebEngine is polluted or missing. Launching Shoul use system web browser...")
    # Launch Fallback mode

