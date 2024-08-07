import tempfile
import unittest
import os
import customtkinter as ctk

from unittest.mock import patch, MagicMock
from pathlib import Path
from src.maidiary import save_log, refresh_logs, generate_key, decrypt_data, load_logs



class TestSaveAndRefreshLogs(unittest.TestCase):

    def create_mock_widget(*args, **kwargs):
        # Crea un widget mockato
        mock_widget = MagicMock()
        mock_widget.pack.side_effect = lambda *args, **kwargs: None
        mock_widget.grid.side_effect = lambda *args, **kwargs: None
        mock_widget.destroy.side_effect = lambda *args, **kwargs: None
        mock_widget.winfo_children.return_value = []  # Simula nessun child iniziale
        return mock_widget
    
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
    @patch('src.maidiary.ctk.CTkFrame', side_effect=create_mock_widget)
    @patch('src.maidiary.ctk.CTkTextbox', side_effect=create_mock_widget)
    @patch('src.maidiary.ctk.CTkButton', side_effect=create_mock_widget)
    def test_save_and_refresh_log(self, mock_messagebox, MockCTkFrame, MockCTkTextbox, MockCTkButton):

        mock_messagebox.return_value = True

        expected_log_path = self.LOGS_PATH / "log_file.txt"

        # Verifica che il file di log non esista prima del salvataggio
        self.assertFalse(expected_log_path.exists())

        saved_log_path = save_log(self.data, self.key, str(self.LOGS_PATH))

        # Verifica che il file di log esista dopo il salvataggio
        self.assertTrue(Path(saved_log_path).exists())

        #with open(saved_log_path, "rb") as file:
            #read_data = file.read()
        log = load_logs(str(self.LOGS_PATH), self.key)

        for log_name, data in log.items():
            #Verifico che non sia in scritto in binario e che sia corretto
            self.assertEqual(self.data, data)

        if os.name != "nt" and os.getenv("GITHUB_ACTIONS"):
            os.system('Xvfb :1 -screen 0 1600x1200x16  &')
            os.environ["DISPLAY"] = ":1.0"

        root = ctk.CTk()
        left_frame = ctk.CTkFrame(root)

        refresh_logs(log, left_frame, "mock_logs_path", "mock_key")

        # Verifica che i widget siano stati creati correttamente
        self.assertTrue(MockCTkTextbox.winfo_exists())
        self.assertTrue(MockCTkFrame.winfo_exists())
        self.assertTrue(MockCTkButton.winfo_exists())
        
        