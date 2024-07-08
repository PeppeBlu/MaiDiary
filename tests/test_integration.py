import unittest
import os
import datetime
from maidiary.maidiary import generate_key, encrypt_data, load_logs



class TestMaidiaryIntegration(unittest.TestCase):

    def setUp(self):
        self.username = "test_user"
        self.password = "test_password"
        self.salt = self.username.encode()
        self.key = generate_key(self.password, self.salt)
        self.LOGS_PATH = f"users/{self.username}_diary"
        os.makedirs(self.LOGS_PATH, exist_ok=True)

    def tearDown(self):
        for file in os.scandir(self.LOGS_PATH):
            os.remove(file.path)
        os.rmdir(self.LOGS_PATH)

    def test_save_and_load_log(self):
        data = "Test diary entry"
        encrypted_data = encrypt_data(data, self.key)
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        log_path = f"{self.LOGS_PATH}/{timestamp}.txt"

        with open(log_path, "wb") as file:
            file.write(encrypted_data)

        logs = load_logs(self.LOGS_PATH, self.key)
        self.assertIn(f"{timestamp}.txt", logs)
        self.assertEqual(logs[f"{timestamp}.txt"], data)

    def test_save_and_load_multiple_logs(self):
        data = "Test diary entry"
        encrypted_data = encrypt_data(data, self.key)
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        log_path = f"{self.LOGS_PATH}/{timestamp}.txt"

        with open(log_path, "wb") as file:
            file.write(encrypted_data)

        data = "Another test diary entry"
        encrypted_data = encrypt_data(data, self.key)
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        log_path = f"{self.LOGS_PATH}/{timestamp}.txt"

        with open(log_path, "wb") as file:
            file.write(encrypted_data)

        logs = load_logs(self.LOGS_PATH, self.key)
        self.assertIn(f"{timestamp}.txt", logs)
        self.assertEqual(logs[f"{timestamp}.txt"], data)
        self.assertEqual(len(logs), 2)
        

# Esegui i test
if __name__ == '__main__':
    unittest.main()
