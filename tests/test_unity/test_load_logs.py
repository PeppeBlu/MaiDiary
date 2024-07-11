from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from src.maidiary import load_logs


class TestLoadLogs(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.username = "test_user"
        self.password = "test_password"
        self.salt = self.username.encode()
        self.key = b'some_generated_key'
        self.LOGS_PATH = Path(self.temp_dir) / f"users/{self.username}_diary"
        self.LOGS_PATH.mkdir(parents=True, exist_ok=True)

        # Preparo i dati e salva i file di log crittografati
        self.data1 = b'encrypted_data_1'
        self.data2 = b'encrypted_data_2'
        self.file1 = self.LOGS_PATH / "log1.txt"
        self.file2 = self.LOGS_PATH / "log2.txt"

        # Scrive i dati crittografati nei file
        with open(self.file1, "wb") as file:
            file.write(self.data1)
        with open(self.file2, "wb") as file:
            file.write(self.data2)

    @patch('src.maidiary.generate_key')
    @patch('src.maidiary.decrypt_data')
    def test_load_logs(self, mock_decrypt_data, mock_generate_key):
        
        mock_generate_key.return_value = self.key

       
        def decrypt_side_effect(data, key):
            if data == self.data1:
                return "secret test data 1"
            elif data == self.data2:
                return "secret test data 2"
            return ""

        mock_decrypt_data.side_effect = decrypt_side_effect

        logs = load_logs(str(self.LOGS_PATH), self.key)

        # Verifica che i contenuti decrittografati corrispondano ai dati originali
        self.assertEqual(logs[self.file1.name], "secret test data 1")
        self.assertEqual(logs[self.file2.name], "secret test data 2")


if __name__ == '__main__':
    unittest.main()