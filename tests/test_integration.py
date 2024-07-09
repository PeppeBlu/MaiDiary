import shutil
import tempfile
import unittest
import os
import datetime
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


class TestRefreshLogs(unittest.TestCase):
    def setUp(self):
        self.LOGS_PATH = "path/to/logs"
        self.key = "encryption_key"
        self.logs = {"log1": "Decrypted content of log1"}

    def test_refresh_logs(self):

        left_frame = MagicMock()
        
        # Chiamata alla funzione da testare con i mock
        refresh_logs(self.logs, left_frame, self.LOGS_PATH, self.key)

        # Verifica che il frame sinistro non sia vuoto
        self.assertNotEqual(len(left_frame.winfo_children()), 0)
        # Verifica che per ogni log nel dizionario sia stato aggiunto un frame e un textbox con il contenuto corretto
        for widget in self.left_frame.winfo_children():
            print("widget aaaaa")
            if isinstance(widget, ctk.CTkFrame):
                self.assertTrue(any(log_frame.winfo_children() for log_frame in widget.winfo_children() if isinstance(log_frame, ctk.CTkTextbox)))

 

# Esegui i test
if __name__ == '__main__':
    unittest.main()
