from datetime import date
from rest_framework.test import APITestCase
from teams.models import Team
from rest_framework.views import status


class CreateTeamTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/teams/"

    def test_if_a_team_can_be_created(self):

        team_data = {
            "name": "Brasil",
            "titles": 5,
            "top_scorer": "Pelé",
            "fifa_code": "BRA",
            "first_cup": "1904-06-08",
        }
        response = self.client.post(self.BASE_URL, data=team_data, format="json")

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

        expected_data = {
            "id": 1,
            "name": "Brasil",
            "titles": 5,
            "top_scorer": "Pelé",
            "fifa_code": "BRA",
            "first_cup": "1904-06-08",
        }
        result_data = response.json()
        msg = (
            "Verifique as informações da seleção retornada no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertEqual(expected_data, result_data, msg)

    def test_if_a_team_negative_titles(self):
        team_data = {
            "name": "Brasil",
            "titles": -5,
            "top_scorer": "Pelé",
            "fifa_code": "BRA",
            "first_cup": "1914-06-08",
        }
        response = self.client.post(self.BASE_URL, data=team_data, format="json")

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

        expected_data = {"error": "You cannot put a negative value"}
        result_data = response.json()
        msg = (
            "Verifique as informações da seleção retornada no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertEqual(expected_data, result_data, msg)

    def test_first_valid_cup(self):
        team_data = {
            "name": "Brasil",
            "titles": 5,
            "top_scorer": "Pelé",
            "fifa_code": "BRA",
            "first_cup": "2003-08-18",
        }
        response = self.client.post(self.BASE_URL, data=team_data, format="json")

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

        expected_data = {"error": "Informed date there was no cup"}
        result_data = response.json()
        msg = (
            "Verifique as informações da seleção retornada no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertEqual(expected_data, result_data, msg)

    def test_validation_of_possible_cup_titles(self):
        team_data = {
            "name": "Brasil",
            "titles": 4,
            "top_scorer": "Pelé",
            "fifa_code": "BRA",
            "first_cup": "2016-08-18",
        }
        response = self.client.post(self.BASE_URL, data=team_data, format="json")

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

        expected_data = {"error": "Impossible to have more titles than disputed cups"}
        result_data = response.json()
        msg = (
            "Verifique as informações da seleção retornada no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertEqual(expected_data, result_data, msg)


class ListTeamTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/teams/"

    def test_if_teams_can_be_listed(self):
        team_1_data = {
            "name": "Brasil",
            "titles": 5,
            "top_scorer": "Pelé",
            "fifa_code": "BRA",
            "first_cup": "1914-06-08",
        }
        team_2_data = {
            "name": "Argentina",
            "titles": 2,
            "top_scorer": "Lionel Messi",
            "fifa_code": "ARG",
            "first_cup": "1800-02-21",
        }

        # Criando time 1
        Team.objects.create(**team_1_data)
        # Criando time 2
        Team.objects.create(**team_2_data)

        response = self.client.get(self.BASE_URL)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

        team_1_return = {**team_1_data, "id": 1}
        team_2_return = {**team_2_data, "id": 2}

        expected_data = [team_1_return, team_2_return]
        result_data = response.json()
        msg = (
            "Verifique as informações das seleções listatas no GET "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertEqual(expected_data, result_data, msg)
