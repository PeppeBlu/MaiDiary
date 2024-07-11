import unittest
import os
import tkinter as tk
import customtkinter as ctk
from unittest.mock import patch, MagicMock
from maidiary.maidiary import show_diary_page


class TestShowDiaryPage(unittest.TestCase):

    def create_mock_widget(*args, **kwargs):
        mock_widget = MagicMock()
        mock_widget.pack.side_effect = lambda *args, **kwargs: None
        mock_widget.grid.side_effect = lambda *args, **kwargs: None
        mock_widget.destroy.side_effect = lambda *args, **kwargs: None
        mock_widget.winfo_children.return_value = []  # Simula nessun child iniziale
        return mock_widget


    @patch('maidiary.maidiary.messagebox')
    @patch('maidiary.maidiary.os.path.exists')
    @patch('maidiary.maidiary.load_logs')
    @patch('maidiary.maidiary.generate_key')
    @patch('maidiary.maidiary.ctk.CTkTextbox', side_effect=create_mock_widget)
    @patch('maidiary.maidiary.ctk.CTkButton', side_effect=create_mock_widget)
    @patch('maidiary.maidiary.ctk.CTkLabel', side_effect=create_mock_widget)
    @patch('maidiary.maidiary.ctk.CTkSlider', side_effect=create_mock_widget)
    def test_show_diary_page(self, mock_generate_key, mock_load_logs,
                             mock_path_exists, mock_messagebox, MockCTkSlider, MockCTkLabel, MockCTkButton, MockCTkTextbox):
        mock_path_exists.return_value = True
        mock_generate_key.return_value = b'test_key'
        mock_load_logs.return_value = {}
        mock_messagebox.askyesno.return_value = True
        mock_messagebox.showwarning.return_value = None
        
        if os.name != "nt" and os.getenv("GITHUB_ACTIONS"):
            os.system('Xvfb :1 -screen 0 1600x1200x16  &')
            os.environ["DISPLAY"] = ":1.0"
        root = ctk.CTk()
        main_frame = ctk.CTkFrame(root)

        user_entry = ctk.CTkEntry(root)
        user_entry.insert(0, 'test_user')
        password_entry = ctk.CTkEntry(root)
        password_entry.insert(0, 'test_password')

        show_diary_page(root, main_frame, user_entry, password_entry)

        #controllo che il main frame sia stato distrutto
        self.assertFalse(main_frame.winfo_exists())

        children = root.winfo_children()
        
        #root ha 4 figli: 2 Entry e 2 Frames (assegnati dalla show_diary_page)
        self.assertEqual(len(children), 4)
        self.assertEqual(MockCTkButton.call_count, 1)
        self.assertGreaterEqual(MockCTkLabel.call_count, 1)
        self.assertGreaterEqual(MockCTkSlider.call_count, 1)



if __name__ == '__main__':
    unittest.main()