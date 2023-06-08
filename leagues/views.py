from django.shortcuts import render, redirect
from django.db.models import Count
from .models import League, Team, Player
from . import team_maker


def index(request):
    # Query 1: All teams in the Atlantic Soccer Conference
    atlantic_soccer_teams = Team.objects.filter(league__name='Atlantic Soccer Conference')

    # Query 2: All (current) players on the Boston Penguins
    boston_penguins_players = Player.objects.filter(curr_team__team_name='Boston Penguins')

    # Query 3: All (current) players in the International Collegiate Baseball Conference
    int_baseball_players = Player.objects.filter(curr_team__league__name='International Collegiate Baseball Conference')

    # Query 4: All (current) players in the American Conference of Amateur Football with last name "Lopez"
    am_football_lopez_players = Player.objects.filter(curr_team__league__name='American Conference of Amateur Football', last_name='Lopez')

    # Query 5: All football players
    football_players = Player.objects.filter(curr_team__league__sport='Football')

    # Query 6: All teams with a (current) player named "Sophia"
    sophia_teams = Team.objects.filter(curr_players__first_name='Sophia')

    # Query 7: All leagues with a (current) player named "Sophia"
    sophia_leagues = League.objects.filter(teams__curr_players__first_name='Sophia')

    # Query 8: Everyone with the last name "Flores" who DOESN'T (currently) play for the Washington Roughriders
    flores_players = Player.objects.filter(last_name='Flores').exclude(curr_team__team_name='Washington Roughriders')

    # Query 9: All teams, past and present, that Samuel Evans has played with
    samuel_teams = Team.objects.filter(all_players__first_name='Samuel', all_players__last_name='Evans')

    # Query 10: All players, past and present, with the Manitoba Tiger-Cats
    manitoba_players = Player.objects.filter(all_teams__team_name='Manitoba Tiger-Cats')

    # Query 11: All players who were formerly (but aren't currently) with the Wichita Vikings
    wichita_ex_players = Player.objects.filter(all_teams__team_name='Wichita Vikings').exclude(curr_team__team_name='Wichita Vikings')

    # Query 12: Every team that Jacob Gray played for before he joined the Oregon Colts
    jacob_teams = Team.objects.filter(all_players__first_name='Jacob', all_players__last_name='Gray').exclude(curr_players__first_name='Jacob', curr_players__last_name='Gray')

    # Query 13: Everyone named "Joshua" who has ever played in the Atlantic Federation of Amateur Baseball Players
    atlantic_joshuas = Player.objects.filter(first_name='Joshua', all_teams__league__name='Atlantic Federation of Amateur Baseball Players')

    # Query 14: All teams that have had 12 or more players, past and present
    teams_with_12_players = Team.objects.annotate(player_count=Count('all_players')).filter(player_count__gte=12)

    # Query 15: All players and count of teams played for, sorted by the number of teams they've played for
    players_with_team_count = Player.objects.annotate(team_count=Count('all_teams')).order_by('team_count')


    context = {
        'sophia_leagues': sophia_leagues,

        'atlantic_soccer_teams': atlantic_soccer_teams,
        'sophia_teams': sophia_teams,
        'samuel_teams': samuel_teams,
        'jacob_teams': jacob_teams,
        'teams_with_12_players': teams_with_12_players,

        'boston_penguins_players': boston_penguins_players,
        'int_baseball_players': int_baseball_players,
        'am_football_lopez_players': am_football_lopez_players,
        'football_players': football_players,
        'flores_players': flores_players,
        'manitoba_players': manitoba_players,
        'wichita_ex_players': wichita_ex_players,
        'atlantic_joshuas': atlantic_joshuas,
        'players_with_team_count': players_with_team_count
    }
    return render(request, "leagues/index.html", context)


def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")