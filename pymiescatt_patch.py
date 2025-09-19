import importlib.util
import os
import sys

def patch_file(file_path):
    """
    Patches a given Python file by replacing the deprecated 'trapz' import
    from scipy.integrate with 'trapezoid as trapz'.
    
    Args:
        file_path (str): The absolute path to the Python file to patch.
    """
    if not os.path.isfile(file_path):
        print(f"\nWarning: File not found at the expected location: {file_path}")
        return

    print(f"\n--- Processing file: {os.path.basename(file_path)} ---")
    print(f"Target file path: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        old_import = "from scipy.integrate import trapz"
        new_import = "from scipy.integrate import trapezoid as trapz"
        
        modified_lines = []
        was_modified = False

        for line in lines:
            # Check for the specific import line to replace
            if line.strip() == old_import:
                modified_lines.append(new_import + '\n')
                print(f"- Replacing:  '{line.strip()}'")
                print(f"+ With:       '{new_import}'")
                was_modified = True
            else:
                modified_lines.append(line)
        
        # Write the changes back to the file if any were made
        if was_modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(modified_lines)
            print(f"Successfully patched '{os.path.basename(file_path)}'!")
        else:
            print(f"No changes needed for '{os.path.basename(file_path)}'. It may already be correct.")

    except IOError as e:
        print(f"\nError: Could not read or write to {file_path}.")
        print("Please check your file permissions.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred while processing {os.path.basename(file_path)}: {e}")


def fix_pymiescatt_imports():
    """
    Checks for PyMieScatt and patches 'Mie.py' and 'Inverse.py' if the
    installed SciPy version is 1.14 or newer.
    """
    print("--- Patching PyMieScatt ---")

    # --- 1. Check for SciPy and its version ---
    try:
        import scipy
        from packaging import version
    except ImportError:
        print("Error: The 'scipy' and 'packaging' libraries are required.")
        print("Please install them first, for example:")
        print("pip install scipy packaging")
        sys.exit(1)

    scipy_version_str = scipy.__version__
    print(f"Detected SciPy version: {scipy_version_str}")

    if version.parse(scipy_version_str) < version.parse("1.14"):
        print("Your SciPy version is older than 1.14. The patch is not needed.")
        sys.exit(0)
    
    print("SciPy version is 1.14 or newer. Checking for required fixes...")

    # --- 2. Locate the PyMieScatt package ---
    try:
        spec = importlib.util.find_spec("PyMieScatt")
        if spec is None or not spec.submodule_search_locations:
            print("\nError: Could not find the PyMieScatt package.")
            print("Please ensure it is installed in your current Python environment.")
            sys.exit(1)
        package_dir = spec.submodule_search_locations[0]
        print(f"Found PyMieScatt package at: {package_dir}")
    except Exception as e:
        print(f"An error occurred while finding PyMieScatt: {e}")
        sys.exit(1)

    # --- 3. Patch the relevant files ---
    mie_py_path = os.path.join(package_dir, "Mie.py")
    inverse_py_path = os.path.join(package_dir, "Inverse.py")
    
    patch_file(mie_py_path)
    patch_file(inverse_py_path)
    
    print("\n--- Patching complete. ---")


if __name__ == "__main__":
    fix_pymiescatt_imports()


