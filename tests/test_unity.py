from pathlib import Path
import shutil
import tempfile
from tkinter import messagebox
import unittest
import datetime
import os
from cryptography.fernet import InvalidToken
from unittest.mock import patch, mock_open, MagicMock
from maidiary.maidiary import encrypt_data, decrypt_data, delete_log
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
        self.temp_dir = tempfile.mkdtemp()  # Crea una directory temporanea
        self.username = "test_user"
        self.password = "test_password"
        self.salt = self.username.encode()
        self.key = generate_key(self.password, self.salt)
        self.LOGS_PATH = Path(self.temp_dir) / f"users/{self.username}_diary"
        self.LOGS_PATH.mkdir(parents=True, exist_ok=True)  # Mi assicuro che il percorso esista
        self.data = "secret test data"

    
    def test_save_log(self):
        log_path = save_log(self.data, self.key, str(self.LOGS_PATH))
        
        # Apro il file e controllo che i dati siano stati scritti correttamente
        with open(log_path, "rb") as file:
            read_data = file.read()
            self.assertNotEqual(read_data, "")  # Mi assicuro che il file non sia vuoto
            self.assertEqual(self.data, decrypt_data(read_data, self.key))
            

class TestSaveLog2(unittest.TestCase):
    def setUp(self):
            self.temp_dir = tempfile.mkdtemp()
            self.username = "test_user"
            self.password = "test_password"
            self.salt = self.username.encode()
            self.key = generate_key(self.password, self.salt)
            self.LOGS_PATH = Path(self.temp_dir) / f"users/{self.username}_diary"
            self.LOGS_PATH.mkdir(parents=True, exist_ok=True)  
            self.data = "secret test data"
    
    
    def test_save_log_2(self):
        # Assicura che il file esista
        #self.assertFalse(Path(self.log_path).exists())
        
        self.log_path = save_log(self.data, self.key, str(self.LOGS_PATH))
        
        # Verifica che il file sia stato eliminato
        self.assertTrue(Path(self.log_path).exists())


class TestLoadLogs(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.username = "test_user"
        self.password = "test_password"
        self.salt = self.username.encode()
        self.key = generate_key(self.password, self.salt)
        self.LOGS_PATH = Path(self.temp_dir) / f"users/{self.username}_diary"
        self.LOGS_PATH.mkdir(parents=True, exist_ok=True)  # Crea la struttura di directory necessaria

        # Preparo i dati e salva i file di log crittografati
        self.data1 = encrypt_data("secret test data 1", self.key)
        self.data2 = encrypt_data("secret test data 2", self.key)
        self.file1 = self.LOGS_PATH / "log1.txt"
        self.file2 = self.LOGS_PATH / "log2.txt"

        # Scrive i dati crittografati nei file
        with open(self.file1, "wb") as file:
            file.write(self.data1)
        with open(self.file2, "wb") as file:
            file.write(self.data2)


    def test_load_logs(self):
        logs = load_logs(str(self.LOGS_PATH), self.key)

        # Verifica che i contenuti decrittografati corrispondano ai dati originali
        with open(self.file1, "rb") as file:
            expected_data1 = decrypt_data(file.read(), self.key)
        with open(self.file2, "rb") as file:
            expected_data2 = decrypt_data(file.read(), self.key)

        # Usa entry.name (nome del file) per accedere ai valori nel dizionario
        self.assertEqual(logs[self.file1.name], expected_data1)
        self.assertEqual(logs[self.file2.name], expected_data2)

        # Verifica che tutti i file previsti siano presenti nel dizionario logs
        self.assertTrue(self.file1.name in logs)
        self.assertTrue(self.file2.name in logs)

       
class TestDeleteLog(unittest.TestCase):
    
        def setUp(self):
            self.temp_dir = tempfile.mkdtemp()
            self.username = "test_user"
            self.password = "test_password"
            self.salt = self.username.encode()
            self.key = generate_key(self.password, self.salt)
            self.LOGS_PATH = Path(self.temp_dir) / f"users/{self.username}_diary"
            self.LOGS_PATH.mkdir(parents=True, exist_ok=True)  
            self.data = "secret test data"
            self.log_path = "test_log.txt"
            with open(f"{self.LOGS_PATH}/{self.log_path}", "wb") as file:
                file.write(encrypt_data(self.data, self.key))
            
    
        @patch("tkinter.messagebox.askyesno")
        def test_delete_log(self, mock_messagebox):
            mock_messagebox.return_value=True
            left_frame=MagicMock()
            
            self.assertTrue(Path(f"{self.LOGS_PATH}/{self.log_path}").exists()) 

            delete_log(self.log_path, left_frame, self.LOGS_PATH, self.key)
            
            # Verifica che il file sia stato eliminato
            self.assertFalse(Path(f"{self.LOGS_PATH}/{self.log_path}").exists())  



if __name__ == '__main__':
    unittest.main()