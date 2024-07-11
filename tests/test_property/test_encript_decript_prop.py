from hypothesis import given, settings, strategies as st
import unittest
from maidiary.maidiary import generate_key, encrypt_data, decrypt_data, calculate_quality

# Strategia per generare stringhe binarie
encoded_text_strategy = st.text().map(lambda x: x.encode())

class TestEncriptionDecriptionProperty(unittest.TestCase):
    
    @given(st.text(), encoded_text_strategy, st.text())
    @settings(max_examples=5)
    def test_encrypt_decrypt_data_property(self, password, salt, data):
        key = generate_key(password, salt)
        encrypted_data = encrypt_data(data, key)
        decrypted_data = decrypt_data(encrypted_data, key)
        self.assertEqual(data, decrypted_data)



if __name__ == '__main__':
    unittest.main()
