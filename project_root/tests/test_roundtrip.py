import os
import tempfile
import subprocess
import sys
import filecmp

def run_cryptocore(args):
    """Helper function to run the cryptocore command using python module."""
    # Запускаем через python -m src.cli_parser вместо cryptocore
    cmd = ['python', '-m', 'src.cli_parser'] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {' '.join(cmd)}", file=sys.stderr)
        print(f"stderr: {result.stderr}", file=sys.stderr)
        print(f"stdout: {result.stdout}", file=sys.stderr)
        return False
    return True

def test_roundtrip():
    """Test that encryption followed by decryption yields the original file."""
    # Создаем временную директорию для тестовых файлов
    with tempfile.TemporaryDirectory() as tmpdir:
        original_file = os.path.join(tmpdir, 'original.txt')
        encrypted_file = os.path.join(tmpdir, 'encrypted.bin')
        decrypted_file = os.path.join(tmpdir, 'decrypted.txt')

        # Создаем тестовый файл с содержимым
        test_content = b"This is a test file for the cryptocore tool.\nIt contains multiple lines and some special characters: \x00\x01\x02\nEnd of file."
        with open(original_file, 'wb') as f:
            f.write(test_content)

        # Ключ для тестирования
        key = '000102030405060708090a0b0c0d0e0f'

        print("Encrypting...")
        encrypt_args = [
            '-algorithm', 'aes',
            '-mode', 'ecb',
            '-encrypt',
            '-key', key,
            '-input', original_file,
            '-output', encrypted_file
        ]
        if not run_cryptocore(encrypt_args):
            return False

        print("Decrypting...")
        decrypt_args = [
            '-algorithm', 'aes',
            '-mode', 'ecb',
            '-decrypt',
            '-key', key,
            '-input', encrypted_file,
            '-output', decrypted_file
        ]
        if not run_cryptocore(decrypt_args):
            return False

        # Сравниваем оригинальный и расшифрованный файлы
        print("Comparing files...")
        if not filecmp.cmp(original_file, decrypted_file, shallow=False):
            print("Round-trip test failed: Decrypted file does not match original.", file=sys.stderr)
            # Выводим размеры файлов для отладки
            orig_size = os.path.getsize(original_file)
            dec_size = os.path.getsize(decrypted_file)
            print(f"Original size: {orig_size}, Decrypted size: {dec_size}", file=sys.stderr)
            return False

        print("✅ Round-trip test passed: Decrypted file matches original.")
        return True

if __name__ == "__main__":
    success = test_roundtrip()
    sys.exit(0 if success else 1)