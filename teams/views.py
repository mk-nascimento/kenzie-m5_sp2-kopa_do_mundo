from rest_framework.views import APIView, Request, Response, status
from django.forms.models import model_to_dict

from utils import data_processing
from exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError
from .models import Team


class TeamView(APIView):
    def post(self, req: Request) -> Response:
        try:
            data_processing(req.data)
        except (
            ImpossibleTitlesError,
            InvalidYearCupError,
            NegativeTitlesError,
        ) as error:
            return Response({"error": error.message}, status.HTTP_400_BAD_REQUEST)

        new_team: Team = Team.objects.create(**req.data)
        team_response: dict = model_to_dict(new_team)

        return Response(team_response, status.HTTP_201_CREATED)

    def get(self, _: Request) -> Response:
        teams = Team.objects.all()
        teams_list: list[dict] = [model_to_dict(team) for team in teams]

        return Response(teams_list)


class TeamDetailView(APIView):
    def get(self, _: Request, team_id: int) -> Response:
        try:
            team: Team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team_response: dict = model_to_dict(team)

        return Response(team_response)

    def patch(self, req: Request, team_id: int) -> Response:
        try:
            team: Team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        for key, value in req.data.items():
            setattr(team, key, value)
        team.save()

        team_response: dict = model_to_dict(team)

        return Response(team_response)

    def delete(self, _: Request, team_id: int) -> Response:
        try:
            Team.objects.get(pk=team_id).delete()
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
