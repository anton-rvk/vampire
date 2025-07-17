import os

current_directory = "."

for filename in os.listdir(current_directory):
    if filename.startswith("Category:"):
        old_path = os.path.join(current_directory, filename)
        new_filename = filename.replace("Category:", "")
        new_filename = new_filename.replace("(VTM)", "")
        new_filename = new_filename.lower()
        new_path = os.path.join(current_directory, new_filename)

        try:
            os.rename(old_path, new_path)
            print(f"Renamed '{filename}' to '{new_filename}'.")
        except Exception as e:
            print(f"Could not rename '{filename}': {e}")