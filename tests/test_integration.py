import shutil
import tempfile
import unittest
import os
import datetime
from unittest.mock import MagicMock
from maidiary.maidiary import generate_key, encrypt_data, load_logs, save_log, refresh_logs




class TestMaidiaryIntegration(unittest.TestCase):

    def setUp(self):
        self.username = "test_user"
        self.password = "test_password"
        self.salt = self.username.encode()
        self.key = generate_key(self.password, self.salt)
        self.LOGS_PATH = f"users/{self.username}_diary"
        self.logs_path = tempfile.mkdtemp()

    def tearDown(self):
        # Pulisci la directory temporanea dopo ogni test
        shutil.rmtree(self.logs_path)

    def test_save_and_load_log(self):
        data = "Test diary entry"
        encrypted_data = encrypt_data(data, self.key)
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        file_name = f"{timestamp}.txt"
        log_path = f"{self.logs_path}/{file_name}"

        with open(log_path, "wb") as file:
            file.write(encrypted_data)

        logs = load_logs(self.logs_path, self.key)
        self.assertIn(file_name, logs)
        self.assertEqual(logs[file_name], data)

    def test_save_and_load_multiple_logs(self):
        # Primo log
        data1 = "Test diary entry"
        encrypted_data1 = encrypt_data(data1, self.key)
        timestamp1 = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        file_name1 = f"{timestamp1}.txt"
        log_path1 = f"{self.logs_path}/{file_name1}"

        with open(log_path1, "wb") as file:
            file.write(encrypted_data1)

        # Attendi per garantire un timestamp univoco
        os.system("sleep 1")

        # Secondo log
        data2 = "Another test diary entry"
        encrypted_data2 = encrypt_data(data2, self.key)
        timestamp2 = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        file_name2 = f"{timestamp2}.txt"
        log_path2 = f"{self.logs_path}/{file_name2}"

        with open(log_path2, "wb") as file:
            file.write(encrypted_data2)

        logs = load_logs(self.logs_path, self.key)
        self.assertIn(file_name2, logs)
        self.assertEqual(logs[file_name2], data2)
        self.assertEqual(len(logs), 2)



# Esegui i test
if __name__ == '__main__':
    unittest.main()
