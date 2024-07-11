from pathlib import Path
import unittest
from unittest.mock import patch
import tempfile
import unittest
from src.maidiary import save_log


class TestSaveLog(unittest.TestCase):

    def setUp(self):
        # Setup comune per i test
        self.temp_dir = tempfile.mkdtemp()
        self.username = "test_user"
        self.password = "test_password"
        self.salt = self.username.encode()
        self.key = b'some_generated_key'
        self.LOGS_PATH = Path(self.temp_dir) / f"users/{self.username}_diary"
        self.LOGS_PATH.mkdir(parents=True, exist_ok=True)
        self.data = "secret test data"

    @patch('src.maidiary.generate_key')
    @patch('src.maidiary.encrypt_data')
    @patch('src.maidiary.decrypt_data')
    def test_save_log(self, mock_decrypt_data, mock_encrypt_data, mock_generate_key):
        # Configura i mock
        mock_generate_key.return_value = self.key
        mock_encrypt_data.return_value = b'encrypted_data'
        mock_decrypt_data.return_value = self.data

        # Percorso previsto per il file di log
        expected_log_path = self.LOGS_PATH / "log_file.txt"

        # Assicura che il file di log non esista prima del salvataggio
        self.assertFalse(expected_log_path.exists())

        # Salva il log
        log_path = save_log(self.data, self.key, str(self.LOGS_PATH))

        # Verifica che il file di log esista dopo il salvataggio
        self.assertTrue(Path(log_path).exists())

        # Apre il file di log e verifica che i dati siano corretti
        with open(log_path, "rb") as file:
            read_data = file.read()
            self.assertNotEqual(read_data, b"")
            self.assertEqual(self.data, mock_decrypt_data(read_data, self.key))


if __name__ == '__main__':
    unittest.main()