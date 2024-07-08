import unittest
import datetime
import os
from cryptography.fernet import InvalidToken
from unittest.mock import patch, mock_open
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
        self.username = "test_user"
        self.password = "test_password"
        self.salt = self.username.encode()
        self.key = generate_key(self.password, self.salt)
        self.LOGS_PATH = f"users/{self.username}_diary"
        self.data = "secret test data"

    @patch("builtins.open", new_callable=mock_open)        
    def test_save_log(self, mock_open):
        log_path = save_log(self.data, self.key, self.LOGS_PATH)
        mock_open.assert_called_with(log_path, "wb")
        mock_open().write.assert_called_with(encrypt_data(self.data, self.key))

        #apro il file e controllo che i dati siano stati scritti correttamente
        with open(log_path, "rb") as file:
            read_data = file.read()
            if read_data != "":
                self.assertEqual(self.data, decrypt_data(read_data, self.key))
            


class TestLoadLogs(unittest.TestCase):

    def setUp(self):
        self.username = "test_user"
        self.password = "test_password"
        self.salt = self.username.encode()
        self.key = generate_key(self.password, self.salt)
        self.LOGS_PATH = f"users/{self.username}_diary"
        self.data = "secret test data"

    @patch("os.scandir")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_logs(self, mock_open, mock_scandir):
        log_path = save_log(self.data, self.key, self.LOGS_PATH)

        #uso mock:scandir per simulare la presenza di un file
        mock_scandir.return_value = [log_path]
        logs = load_logs(self.LOGS_PATH, self.key)

        #controllo che logs sia un dizionario 
        self.assertIsInstance(logs, dict)



       
        

    
        
       


if __name__ == '__main__':
    unittest.main()