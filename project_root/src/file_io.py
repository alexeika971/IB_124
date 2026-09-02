def read_file(file_path: str) -> bytes:
    """
    Read the entire contents of a file in binary mode.

    Args:
        file_path: Path to the file to read.

    Returns:
        The file contents as bytes.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read.
        OSError: For other I/O errors.
    """
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{file_path}' not found.")
    except PermissionError:
        raise PermissionError(f"Permission denied: Cannot read '{file_path}'.")
    except OSError as e:
        raise OSError(f"An I/O error occurred while reading '{file_path}': {e}")

def write_file(file_path: str, data: bytes) -> None:
    """
    Write data to a file in binary mode.

    Args:
        file_path: Path to the file to write.
        data: The data to write (as bytes).

    Raises:
        PermissionError: If the file cannot be written.
        OSError: For other I/O errors.
    """
    try:
        with open(file_path, 'wb') as f:
            f.write(data)
    except PermissionError:
        raise PermissionError(f"Permission denied: Cannot write to '{file_path}'.")
    except OSError as e:
        raise OSError(f"An I/O error occurred while writing to '{file_path}': {e}")