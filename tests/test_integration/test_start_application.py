import unittest
import os
import tkinter as tk
import customtkinter as ctk
from unittest.mock import patch, MagicMock
from maidiary.maidiary import main, show_diary_page


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

    
    
    @patch('maidiary.maidiary.messagebox')
    @patch('maidiary.maidiary.os.path.exists')
    @patch('maidiary.maidiary.load_logs')
    @patch('maidiary.maidiary.generate_key')
    @patch('maidiary.maidiary.ctk.CTkTextbox', side_effect=create_mock_widget)
    @patch('maidiary.maidiary.ctk.CTkButton', side_effect=create_mock_widget)
    @patch('maidiary.maidiary.ctk.CTkLabel', side_effect=create_mock_widget)
    @patch('maidiary.maidiary.ctk.CTkSlider', side_effect=create_mock_widget)
    @patch('maidiary.maidiary.tk.PhotoImage', side_effect=mock_photoimage)
    @patch('maidiary.maidiary.ctk.CTkFrame', side_effect=create_mock_widget)
    @patch('maidiary.maidiary.create_main_frame', side_effect=create_mock_widget)
    def test_main(self, MockCTkFrame,  MockPhotoImage, MockCreateMainFrame,
                  mock_generate_key, mock_load_logs, mock_path_exists, mock_messagebox,
                  MockCTkSlider, MockCTkLabel, MockCTkButton, MockCTkTextbox):

        logo = tk.PhotoImage()
        MockPhotoImage.return_value = logo

        mock_path_exists.return_value = True
        mock_generate_key.return_value = b'test_key'
        mock_load_logs.return_value = {}
        mock_messagebox.askyesno.return_value = True
        mock_messagebox.showwarning.return_value = None

        if os.name != "nt" and os.getenv("GITHUB_ACTIONS"):
            os.system('Xvfb :1 -screen 0 1600x1200x16  &')
            os.environ["DISPLAY"] = ":1.0"

        root = ctk.CTk()
        MockCreateMainFrame.return_value = ctk.CTkFrame(root)
        main(root, Test=True)

        # Verifico che il frame principale si stato creato
        self.assertEqual(MockCTkFrame.call_count, 1)
        # e che il root non sia vuoto
        self.assertTrue(root.winfo_exists())

        main_frame = ctk.CTkFrame(root)

        user_entry = ctk.CTkEntry(root)
        user_entry.insert(0, 'test_user')
        password_entry = ctk.CTkEntry(root)
        password_entry.insert(0, 'test_password')

        show_diary_page(root, main_frame, user_entry, password_entry)

        #conto il numero di figli di root
        children = root.winfo_children()
        
        #controllo che il root esista e che non sia vuoto
        self.assertTrue(root.winfo_exists())
        self.assertGreater(len(children), 0)