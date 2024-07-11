from hypothesis import given, settings, strategies as st
import unittest
from maidiary.maidiary import calculate_quality


class TestCalculateQuality(unittest.TestCase):

    @given(
        satisfaction_level=st.floats(min_value=0, max_value=10),
        mood_level=st.floats(min_value=0, max_value=10),
        stress_level=st.floats(min_value=0, max_value=10),
        physical_activity=st.floats(min_value=0, max_value=10),
        social_relations=st.floats(min_value=0, max_value=10)
    )
    @settings(max_examples=100)
    def test_calculate_quality_property(self, satisfaction_level, mood_level, stress_level, physical_activity, social_relations):
        # Calcolo la qualità della giornata
        quality = calculate_quality(satisfaction_level, mood_level, stress_level, physical_activity, social_relations)

        # Verifico che la qualità sia un valore tra 0 e 1
        self.assertGreaterEqual(quality, 0)
        self.assertLessEqual(quality, 10)



if __name__ == '__main__':
    unittest.main()