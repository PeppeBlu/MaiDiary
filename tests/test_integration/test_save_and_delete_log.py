import tempfile
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.maidiary import delete_log, save_log, generate_key, decrypt_data, encrypt_data


class TestSaveAndDeleteLog(unittest.TestCase):

    def setUp(self):
        # Setup comune per i test
        self.temp_dir = tempfile.mkdtemp()
        self.username = "test_user"
        self.password = "test_password"
        self.salt = self.username.encode()
        self.key = generate_key(self.password, self.salt)
        self.LOGS_PATH = Path(self.temp_dir) / f"users/{self.username}_diary"
        self.LOGS_PATH.mkdir(parents=True, exist_ok=True)
        self.data = "secret test data"

    @patch("tkinter.messagebox.askyesno")
    def test_save_and_delete_log(self, mock_messagebox):
    
        mock_messagebox.return_value = True
        expected_log_path = self.LOGS_PATH / "log_file.txt"

        # Assicura che il file di log non esista prima del salvataggio
        self.assertFalse(expected_log_path.exists())

        saved_log_path = save_log(self.data, self.key, str(self.LOGS_PATH))

        # Verifica che il file di log esista dopo il salvataggio
        self.assertTrue(Path(saved_log_path).exists())

        with open(saved_log_path, "rb") as file:
            read_data = file.read()

            #Verifico che non sia in scritto in binario e che sia corretto
            self.assertNotEqual(read_data, b"")
            self.assertEqual(self.data, decrypt_data(read_data, self.key))

        left_frame = MagicMock()
        delete_log(saved_log_path, left_frame, "", self.key)

        # Verifico che il file sia stato eliminato
        self.assertFalse(Path(saved_log_path).exists())