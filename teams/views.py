from rest_framework.views import APIView, Request, Response, status
from django.forms.models import model_to_dict

from utils import data_processing
from exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError
from .models import Team


class TeamView(APIView):
    def post(self, req: Request) -> Response:
        team_payload = req.data

        try:
            data_processing(team_payload)
        except (
            ImpossibleTitlesError,
            InvalidYearCupError,
            NegativeTitlesError,
        ) as error:
            return Response({"error": error.message}, status.HTTP_400_BAD_REQUEST)

        new_team: Team = Team.objects.create(**team_payload)

        team_response: dict = model_to_dict(new_team)

        return Response(team_response, status.HTTP_201_CREATED)

    def get(self, _: Request) -> Response:
        teams = Team.objects.all()
        teams_list: list[dict] = [model_to_dict(team) for team in teams]

        return Response(teams_list)
