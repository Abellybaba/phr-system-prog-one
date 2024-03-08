import unittest
from app.services import health_record_service

class TestHealthRecordService(unittest.TestCase):

    def test_add_health_record(self):
        record_id = health_record_service.add_health_record(1, 'General Checkup', 'Summary of the checkup', 'http://example.com/details', 1)
        self.assertIsNotNone(record_id)

    # Adding more tests for update, delete, and retrieval of health records

if __name__ == '__main__':
    unittest.main()
