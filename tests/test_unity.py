from pathlib import Path
import tempfile
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import unittest
from cryptography.fernet import InvalidToken
from unittest.mock import Mock, patch, MagicMock
from maidiary.maidiary import encrypt_data, decrypt_data, delete_log, refresh_logs
from maidiary.maidiary import generate_key, calculate_quality, load_logs, save_log





class TestGenerateKey(unittest.TestCase):

    def test_generate_key(self):
        password = "mypassword"
        salt = b"mysalt"
        key = generate_key(password, salt)
        self.assertIsInstance(key, bytes)
        self.assertEqual(len(key), 44)  # La lunghezza di una chiave base64 urlsafe è 44


class TestEncryptionDecryptionFunctions(unittest.TestCase):

    def setUp(self):
        self.username = "test_user"
        self.password = "test_password"
        self.salt = self.username.encode()
        self.key = generate_key(self.password, self.salt)
        self.data = "secret test data"
        

    def test_encrypt_decrypt_data(self):
        encrypted_data = encrypt_data(self.data, self.key)
        decrypted_data = decrypt_data(encrypted_data, self.key)
        self.assertEqual(self.data, decrypted_data)


    def test_invalid_key_decrypt(self):
        invalid_key = generate_key("wrong_password", self.salt)
        encrypted_data = encrypt_data(self.data, self.key)
        with self.assertRaises(InvalidToken):
            decrypt_data(encrypted_data, invalid_key)


    def test_invalid_data_to_decrypt(self):
        with self.assertRaises(InvalidToken):
            decrypt_data("not encrypted".encode(), self.key)


class TestCalculateQuality(unittest.TestCase):

    def test_calculate_quality_max(self):
        from maidiary.maidiary import calculate_quality
        quality = calculate_quality(10, 10, 10, 10, 10)
        self.assertEqual(quality, 10)

    def test_calculate_quality_not_max(self):
        quality = calculate_quality(7, 4, 9, 8, 10)
        self.assertNotEqual(quality, 10)

    def test_calculate_quality_min(self):
        quality = calculate_quality(0, 0, 0, 0, 0)
        self.assertEqual(quality, 0)


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

    @patch('maidiary.maidiary.generate_key')
    @patch('maidiary.maidiary.encrypt_data')
    @patch('maidiary.maidiary.decrypt_data')
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
            self.assertNotEqual(read_data, b"")  # Verifica che il file non sia vuoto
            self.assertEqual(self.data, mock_decrypt_data(read_data, self.key))  # Verifica che i dati siano corretti


class TestLoadLogs(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.username = "test_user"
        self.password = "test_password"
        self.salt = self.username.encode()
        self.key = b'some_generated_key'
        self.LOGS_PATH = Path(self.temp_dir) / f"users/{self.username}_diary"
        self.LOGS_PATH.mkdir(parents=True, exist_ok=True)  # Crea la struttura di directory necessaria

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

    @patch('maidiary.maidiary.generate_key')
    @patch('maidiary.maidiary.decrypt_data')
    def test_load_logs(self, mock_decrypt_data, mock_generate_key):
        # Configura i mock
        mock_generate_key.return_value = self.key

        # Definisco un side_effect che rispecchi l'ordine di lettura effettivo dei file
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
    @patch("maidiary.maidiary.decrypt_data")  # Mockiamo la funzione di decriptazione
    def test_delete_log(self, mock_decrypt_data, mock_messagebox):
        mock_messagebox.return_value = True
        left_frame = MagicMock()
        
        self.assertTrue(Path(f"{self.LOGS_PATH}/{self.log_path}").exists())

        # Configuriamo il mock per restituire il dato decriptato atteso
        mock_decrypt_data.return_value = self.data.decode()  # Decodifica il dato criptato

        delete_log(self.log_path, left_frame, self.LOGS_PATH, self.key)

        # Verifica che il file sia stato eliminato
        self.assertFalse(Path(f"{self.LOGS_PATH}/{self.log_path}").exists())  


class TestRefreshLogs(unittest.TestCase):

    @patch('maidiary.maidiary.make_delete_command')
    @patch('maidiary.maidiary.make_visualize_command')
    @patch('maidiary.maidiary.load_logs')
    def test_refresh_logs(self, mock_load_logs, mock_make_visualize_command, mock_make_delete_command):
        # Configurazione iniziale
        mock_load_logs.return_value = {
            "log1.txt": "Contenuto del log 1",
            "log2.txt": "Contenuto del log 2"
        }
        logs = {
            "log1.txt": "Contenuto del log 1",
            "log2.txt": "Contenuto del log 2"
        }

        # Creazione del frame
        root = ctk.CTk()
        left_frame = ctk.CTkFrame(root)

        # Chiamata alla funzione
        refresh_logs(logs, left_frame, "mock_logs_path", "mock_key")

        # Verifica che i widget siano stati creati correttamente
        self.assertEqual(len(left_frame.winfo_children()), 4)  # 2 log_frame + 2 buttons_frame

        # Verifica delle chiamate delle funzioni di comando
        self.assertEqual(mock_make_delete_command.call_count, 2)
        self.assertEqual(mock_make_visualize_command.call_count, 2)

        # Distruzione dei widget
        for widget in left_frame.winfo_children():
            widget.destroy()




if __name__ == '__main__':
    unittest.main()