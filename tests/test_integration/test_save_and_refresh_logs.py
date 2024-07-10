import tempfile
import unittest
import os
import customtkinter as ctk

from unittest.mock import patch, MagicMock
from pathlib import Path
from maidiary.maidiary import save_log, refresh_logs, generate_key, decrypt_data



class TestSaveAndRefreshLogs(unittest.TestCase):

    def create_mock_widget(*args, **kwargs):
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
    def test_save_and_delete_log(self, mock_messagebox):
        # Configura i mock
        mock_messagebox.return_value = True

        # Percorso previsto per il file di log
        expected_log_path = self.LOGS_PATH / "log_file.txt"

        # Assicura che il file di log non esista prima del salvataggio
        self.assertFalse(expected_log_path.exists())

        # Salva il log
        saved_log_path = save_log(self.data, self.key, str(self.LOGS_PATH))

        # Verifica che il file di log esista dopo il salvataggio
        self.assertTrue(Path(saved_log_path).exists())

        # Apre il file di log e verifica che i dati siano corretti
        with open(saved_log_path, "rb") as file:
            read_data = file.read()

            #Verifico che non sia in scritto in binario e che sia corretto
            self.assertNotEqual(read_data, b"")
            self.assertEqual(self.data, decrypt_data(read_data, self.key))


    
    @patch('maidiary.maidiary.ctk.CTkFrame', side_effect=create_mock_widget)
    @patch('maidiary.maidiary.ctk.CTkTextbox', side_effect=create_mock_widget)
    @patch('maidiary.maidiary.ctk.CTkButton', side_effect=create_mock_widget)
    def test_refresh_logs(self, MockCTkFrame, MockCTkTextbox, MockCTkButton):
        # Simulazione dei log
        logs = {
            "log1.txt": "Contenuto del log 1"
        }

        if os.name != "nt" and os.getenv("GITHUB_ACTIONS"):
            os.system('Xvfb :1 -screen 0 1600x1200x16  &')
            os.environ["DISPLAY"] = ":1.0"

        root = ctk.CTk()
        left_frame = ctk.CTkFrame(root)

        # Chiamata alla funzione da testare
        refresh_logs(logs, left_frame, "mock_logs_path", "mock_key")

        # Verifica che i widget siano stati creati correttamente
        self.assertEqual(MockCTkFrame.call_count, 2)
        self.assertEqual(MockCTkTextbox.call_count, 1)  # Un textbox per ogni log
        self.assertEqual(MockCTkButton.call_count, 3)  # Due pulsanti per ogni log

        # Verifica che i pulsanti esistano
        self.assertTrue(MockCTkButton.winfo_exists())
        self.assertTrue(MockCTkButton.winfo_exists())