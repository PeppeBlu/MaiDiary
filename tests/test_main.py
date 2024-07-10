import unittest
import os
import tkinter as tk
import customtkinter as ctk
from unittest.mock import patch, MagicMock
from maidiary.maidiary import main


class TestMain(unittest.TestCase):

    def create_mock_widget(*args, **kwargs):
        mock_widget = MagicMock()
        mock_widget.pack.side_effect = lambda *args, **kwargs: None
        mock_widget.grid.side_effect = lambda *args, **kwargs: None
        mock_widget.destroy.side_effect = lambda *args, **kwargs: None
        mock_widget.winfo_children.return_value = []  # Simula nessun child iniziale
        return mock_widget

    def mock_photoimage(*args, **kwargs):
        mock_photo = MagicMock()
        return mock_photo

    @patch('maidiary.maidiary.tk.PhotoImage', side_effect=mock_photoimage)
    @patch('maidiary.maidiary.ctk.CTkFrame', side_effect=create_mock_widget)
    @patch('maidiary.maidiary.create_main_frame', side_effect=create_mock_widget)
    def test_main(self, MockCTkFrame,  MockPhotoImage, MockCreateMainFrame):

        if os.name != "nt" and os.getenv("GITHUB_ACTIONS"):
            os.system('Xvfb :1 -screen 0 1600x1200x16  &')
            os.environ["DISPLAY"] = ":1.0"
        
        logo = tk.PhotoImage()
        MockPhotoImage.return_value = logo
        root = ctk.CTk()
        MockCreateMainFrame.return_value = ctk.CTkFrame(root)
        main(root, Test=True)

        # Verifico che il frame principale si stato creato
        self.assertEqual(MockCTkFrame.call_count, 1)