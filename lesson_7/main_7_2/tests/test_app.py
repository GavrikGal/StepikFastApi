import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

from ..main import app, some_logic, get_db


client = TestClient(app)

mock_db = [{'username': 'user3', 'password': 'pass1'},
           {'username': 'user2', 'password': 'pass2'}]


def mock_get_db():
    return mock_db


# Подмена зависимостей
app.dependency_overrides[get_db] = mock_get_db


class TestMain(unittest.TestCase):

    def test_get_user(self):
        """ Тестирование получения доступа к БД """

        response = client.get('/users/user3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            mock_db[0]
        )

    @patch('lesson_7.main_7_2.main.some_logic')
    def test_some_logic(self, mock_some_logic):
        """ Тестирование логики """

        mock_some_logic.return_value = 3

        response = client.get('/logic?a=1&b=2')

        mock_some_logic.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {'result': 3}
        )
