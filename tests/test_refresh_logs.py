import unittest
import os
import customtkinter as ctk
from unittest.mock import patch, MagicMock
from maidiary.maidiary import  refresh_logs


class TestRefreshLogs(unittest.TestCase):

    def create_mock_widget(*args, **kwargs):
        mock_widget = MagicMock()
        mock_widget.pack.side_effect = lambda *args, **kwargs: None
        mock_widget.grid.side_effect = lambda *args, **kwargs: None
        mock_widget.destroy.side_effect = lambda *args, **kwargs: None
        mock_widget.winfo_children.return_value = []  # Simula nessun child iniziale
        return mock_widget


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


if __name__ == '__main__':
    unittest.main()