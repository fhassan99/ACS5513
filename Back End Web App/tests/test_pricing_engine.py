import unittest
from app.services.pricing_engine import PricingEngine

class TestPricingEngine(unittest.TestCase):

    def setUp(self):
        self.engine = PricingEngine()

    def test_train_model(self):
        # Assuming we have some training data
        training_data = {
            'feature1': [1, 2, 3],
            'feature2': [4, 5, 6],
            'price': [100000, 150000, 200000]
        }
        self.engine.train_model(training_data)
        self.assertIsNotNone(self.engine.model)

    def test_predict_price(self):
        # Assuming the model has been trained
        training_data = {
            'feature1': [1, 2, 3],
            'feature2': [4, 5, 6],
            'price': [100000, 150000, 200000]
        }
        self.engine.train_model(training_data)
        prediction = self.engine.predict_price({'feature1': 2, 'feature2': 5})
        self.assertIsInstance(prediction, float)

if __name__ == '__main__':
    unittest.main()