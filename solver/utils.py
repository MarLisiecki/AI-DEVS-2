import os


def find_dotenv(start_path):
    current_path = os.path.abspath(start_path)

    while True:
        files_in_current_dir = os.listdir(current_path)

        if ".env" in files_in_current_dir:
            return os.path.join(current_path, ".env")

        new_path = os.path.dirname(current_path)

        if new_path == current_path:
            return None

        current_path = new_path


if __name__ == "__main__":
    pass
