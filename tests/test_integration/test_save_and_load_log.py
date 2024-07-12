import tempfile
import unittest
import os
import datetime
from src.maidiary import generate_key, encrypt_data, load_logs


class TestSaveAndLoadLog(unittest.TestCase):

    def setUp(self):
        self.username = "test_user"
        self.password = "test_password"
        self.salt = self.username.encode()
        self.key = generate_key(self.password, self.salt)
        self.logs_path = tempfile.mkdtemp()
        

    def test_save_and_load_log(self):
        timestamp0 = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        data = "Test diary entry"
        encrypted_data = encrypt_data(data, self.key)
        file_name0 = f"{timestamp0}.txt"
        self.log_path = f"{self.logs_path}/{file_name0}"

        with open(self.log_path, "wb") as file:
            file.write(encrypted_data)

        logs = load_logs(self.logs_path, self.key)
        self.assertIn(file_name0, logs)
        self.assertEqual(logs[file_name0], data)
        


if __name__ == '__main__':
    unittest.main()
