import unittest
import os
import tempfile
from cryptography.fernet import InvalidToken
from hypothesis import given, strategies as st

# Importiamo le funzioni dal file principale
from maidiary.maidiary import generate_key, encrypt_data, decrypt_data, calculate_quality, refresh_logs, load_logs, save_log, delete_log

class TestMaidiary(unittest.TestCase):

    def setUp(self):
        self.password = "test_password"
        self.salt = b"test_salt"
        self.key = generate_key(self.password, self.salt)
        self.data = "Test diary entry"

    def test_generate_key(self):
        key = generate_key(self.password, self.salt)
        self.assertEqual(len(key), 44)  # Fernet key should be 44 bytes

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


    def test_calculate_quality(self):
        quality = calculate_quality(10, 10, 10, 10, 10)
        self.assertEqual(quality, 10)

        quality = calculate_quality(7, 4, 9, 8, 10)
        self.assertNotEqual(quality, 10)

        quality = calculate_quality(0, 0, 0, 0, 0)
        self.assertEqual(quality, 0)

# Esegui i test
if __name__ == '__main__':
    unittest.main()
