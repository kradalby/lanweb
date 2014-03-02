# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from apps.event.models import LanEvent
from apps.compo.models import Game, Tournament, Participant, Team
from django.contrib import messages
from forms import RegisterTeamForm, ChallongeForm
import challonge
import re
from datetime import date


challonge.set_credentials('dfektlan', 'EmOkMBJWRbH1Ouf2dwvY5rm6MJMuIkTubWQfDK6f')
LATEST_EVENT = LanEvent.objects.filter(current=True)[0]


def overview(request):
    all_games = Game.objects.all()
    all_tournaments = Tournament.objects.filter(event=LATEST_EVENT)
    tournament_dict = {}
    for g in all_games:
        tournament_dict[g] = all_tournaments.filter(game=g)
        for t in tournament_dict[g]:
            t.set_status()
    return render(request, 'compo/overview.html', {'tournaments':tournament_dict, 'all_games':all_games})


def tournament(request, tournament_id=None):
    tour = get_object_or_404(Tournament, pk=tournament_id)
    try:
        challonge_image = challonge.tournaments.show(tour.challonge_id)['live-image-url']
        challonge_url = challonge.tournaments.show(tour.challonge_id)['full-challonge-url']
    except:
        print "Shit got excepted"
        challonge_image = ""
        challonge_url = ""
    participants = tour.get_participants()
    is_participant = has_participant(tour, request.user)
    #should move is_teamleader to SiteUser PS. verdens styggeste if-setning?
    is_teamleader = False
    if request.user.is_authenticated() and not request.user.is_anonymous() and tour.use_teams:
                is_teamleader = request.user.is_teamleader.filter(participant__tournament=tour)
    if request.POST:
        team_form = RegisterTeamForm(request.POST, tour=tour, request=request)
        if team_form.is_valid():
            #intention is to just say form.save() here and remove make_team_participant()
            make_team_participant(request, team_form, tour)
            return redirect('tournament', tournament_id)
    else:
        team_form = RegisterTeamForm(tour=tour, request=request)
    #challonge_form = ChallongeForm(request)
    return render(request, 'compo/tournament.html', {'tournament': tour,
                                                     'participants': participants,
                                                     'team_form': team_form,
                                                     'is_participant': is_participant,
                                                     'is_teamleader': is_teamleader,
                                                     'challonge_image': challonge_image,
                                                     'challonge_url': challonge_url})


def register_to_tournament(request, tournament_id=None):
    tour = get_object_or_404(Tournament, pk=tournament_id)
    if not request.user.is_authenticated():
        messages.error(request, u'You must log in to register for a tournament')
    elif has_participant(tour, request.user):
        messages.error(request, u'You are already signed up for this tournament')
    else:
        make_participant(request.user, tour)
        messages.success(request, u'You have successfully register for this tournament')

    return redirect('tournament', tournament_id)


def has_participant(tour, user):
    participants = tour.get_participants()
    if tour.use_teams:
        for p in participants:
            if user in p.members.all():
                return True
    else:
        for p in participants:
            if user == p:
                return True
    return False


def make_participant(user, tour):
    p = Participant()
    p.user = user
    p.tournament = tour
    p.save()


def make_team_participant(request, form, tour):
    team = Team()
    participant = Participant()
    # Unike teamtitle? not working.. -_- required for Challonge!
    #if form.cleaned_data['title'] in Participant.objects.filter(tournament=tour):
    #    messages.error(request, u'This teamname is already taken')
    team.title = form.cleaned_data['title']
    team.teamleader = request.user
    team.save()
    for user in form.cleaned_data['members']:
        team.members.add(user)
    team.save()
    participant.team = team
    participant.tournament = tour
    participant.save()
    messages.success(request, u'You have successfully registered your team for this tournament')


def check_user(request, tournament_id=None):
    if not request.user.is_authenticated():
        messages.error(request, u'You must log in to register for a tournament')
    return redirect('tournament', tournament_id)


def remove_participant(request, tournament_id=None):
    tour = get_object_or_404(Tournament, pk=tournament_id)
    participants = tour.get_participants()
    if tour.use_teams:
        for team in participants:
            if request.user in team.members.all():
                team.members.remove(request.user)
                messages.success(request, u'You were removed from the team "' + team.title +'"')
        if request.user.is_teamleader.filter(participant__tournament=tour):
            for team in request.user.is_teamleader.filter(participant__tournament=tour):
                #promt "are you sure you want to delete the team..?"
                team.delete()
                messages.success(request, u'You have deleted the team "' + team.title + '"')

    else:
        participant = Participant.objects.get(user=request.user, tournament=tournament_id)
        participant.delete()
        messages.success(request, u'You were unregistered from this tournament')
    return redirect('tournament', tournament_id)


def create_tournament(request, tournament_id=None):
    tour = get_object_or_404(Tournament, pk=tournament_id)
    slug = "dfektLAN_" + (str(date.today()) + "_" + re.sub(r"[^a-zA-Z0-9_-]", '', tour.title)).replace('-', '_')
    try:
        tour.challonge_id = str(challonge.tournaments.create(tour.title, slug, tournament_type=str(tour.get_challonge_type_display()))['id'])
        tour.save()
        messages.success(request, u'Challonge!-tournament successfully created')
        for p in tour.get_participants():
            challonge.participants.create(tour.challonge_id, p)
    except:
        messages.error(request, u'OPS! Challonge!-tournament was not created..')
    return redirect('tournament', tournament_id)


def start_tournament(request, tournament_id=None):
    tour = get_object_or_404(Tournament, pk=tournament_id)
    try:
        challonge.tournaments.start(tour.challonge_id)
        messages.success(request, u'Challonge!-tournament successfully started')
    except:
        messages.error(request, u'OPS! Have you created the Challonge!-tournament?')
    return redirect('tournament', tournament_id)


def destroy_tournament(request, tournament_id=None):
    tour = get_object_or_404(Tournament, pk=tournament_id)
    try:
        challonge.tournaments.destroy(tour.challonge_id)
        messages.success(request, u'Challonge!-tournament successfully destroyed')
    except:
        messages.error(request, u'OPS! Have you created the Challonge!-tournament?')
    return redirect('tournament', tournament_id)