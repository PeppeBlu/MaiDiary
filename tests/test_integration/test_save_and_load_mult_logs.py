import tempfile
import unittest
import os
import datetime
from src.maidiary import generate_key, encrypt_data, load_logs


class TestSaveAndLoadMultipleLog(unittest.TestCase):

    def setUp(self):
        self.username = "test_user"
        self.password = "test_password"
        self.salt = self.username.encode()
        self.key = generate_key(self.password, self.salt)
        self.logs_path = tempfile.mkdtemp()


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

        # Controllo la presenza e la correttenzza dei file
        self.assertEqual(len(logs), 2)
        self.assertIn(file_name2, logs)
        self.assertIn(file_name1, logs)
        self.assertEqual(logs[file_name2], data2)
        self.assertEqual(logs[file_name1], data1)
        


if __name__ == '__main__':
    unittest.main()
