from pathlib import Path
import shutil
import tempfile
import unittest
import datetime
import os
from cryptography.fernet import InvalidToken
from unittest.mock import patch, mock_open, MagicMock
from maidiary.maidiary import encrypt_data, decrypt_data, generate_key, calculate_quality, load_logs, save_log



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
        with self.assertRaises(TypeError):
            decrypt_data("not encrypted", self.key)



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
        self.LOGS_PATH.mkdir(parents=True, exist_ok=True)  # Assicurati che il percorso esista
        self.data = "secret test data"

    def tearDown(self):
        # Pulisci la directory temporanea dopo ogni test
        for item in Path(self.temp_dir).glob("*"):
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

    def test_save_log(self):
        # Assumi che save_log restituisca il percorso del file come stringa
        log_path = save_log(self.data, self.key, str(self.LOGS_PATH))
        
        # Apri il file e controlla che i dati siano stati scritti correttamente
        with open(log_path, "rb") as file:
            read_data = file.read()
            self.assertNotEqual(read_data, "")  # Assicurati che il file non sia vuoto
            self.assertEqual(self.data, decrypt_data(read_data, self.key))
            


class TestLoadLogs(unittest.TestCase):

    def setUp(self):
        # Crea una directory temporanea
        self.temp_dir = tempfile.mkdtemp()
        self.username = "test_user"
        self.password = "test_password"
        self.salt = self.username.encode()
        self.key = generate_key(self.password, self.salt)
        self.LOGS_PATH = Path(self.temp_dir) / f"users/{self.username}_diary"
        self.LOGS_PATH.mkdir(parents=True, exist_ok=True)  # Crea la struttura di directory necessaria

        # Prepara i dati e salva i file di log crittografati
        self.data1 = encrypt_data("secret test data 1", self.key)
        self.data2 = encrypt_data("secret test data 2", self.key)
        self.file1 = self.LOGS_PATH / "log1.txt"
        self.file2 = self.LOGS_PATH / "log2.txt"

        # Scrive i dati crittografati nei file
        with open(self.file1, "wb") as file:
            file.write(self.data1)
        with open(self.file2, "wb") as file:
            file.write(self.data2)

    def tearDown(self):
        # Rimuove la directory temporanea e tutto il suo contenuto
        shutil.rmtree(self.temp_dir)

    def test_load_logs(self):
        # Esegue la funzione da testare
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


       
        

    
        
       


if __name__ == '__main__':
    unittest.main()