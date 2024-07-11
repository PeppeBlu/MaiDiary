from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from src.maidiary import delete_log


class TestDeleteLog(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.username = "test_user"
        self.password = "test_password"
        self.salt = self.username.encode()
        self.key = b'some_generated_key'  # Chiave mockata
        self.LOGS_PATH = Path(self.temp_dir) / f"users/{self.username}_diary"
        self.LOGS_PATH.mkdir(parents=True, exist_ok=True)
        self.data = b'encrypted_test_data'  # Dati criptati mockati
        self.log_path = "test_log.txt"

        # Scrive i dati criptati nel file di log
        with open(f"{self.LOGS_PATH}/{self.log_path}", "wb") as file:
            file.write(self.data)
 
    @patch("tkinter.messagebox.askyesno")
    @patch("src.maidiary.decrypt_data")  # Mockiamo la funzione di decriptazione
    def test_delete_log(self, mock_decrypt_data, mock_messagebox):
        mock_messagebox.return_value = True
        left_frame = MagicMock()

        self.assertTrue(Path(f"{self.LOGS_PATH}/{self.log_path}").exists())

        # Configuriamo il mock per restituire il dato decriptato atteso
        mock_decrypt_data.return_value = self.data.decode()  # Decodifica il dato criptato

        delete_log(self.log_path, left_frame, self.LOGS_PATH, self.key)

        # Verifica che il file sia stato eliminato
        self.assertFalse(Path(f"{self.LOGS_PATH}/{self.log_path}").exists())


if __name__ == '__main__':
    unittest.main()