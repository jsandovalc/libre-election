import pytz
from delorean import Delorean
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Voter, VotingJury, List
from . import models


def to_localtime(dt):
    local_tz = pytz.timezone('America/Bogota')
    return dt.replace(tzinfo=pytz.utc).astimezone(local_tz).replace(tzinfo=None)


class Index(LoginRequiredMixin, View):
    """Form to login with document. No password required."""
    def get(self, request):
        if request.user.is_superuser:
            return redirect('report')

        return render(request, 'index.html')

    def post(self, request):
        document = request.POST.get(
            'document').replace(' ', '').replace('.', '').replace(',', '')

        try:
            election = VotingJury.objects.get(user=self.request.user).polling_station.election

            if not(election.start_date < Delorean().datetime < election.end_date):
                context = dict(message=f'La elección no se encuentra habilitada')
                return render(request, 'index.html',
                              context=context)

            voter = Voter.objects.get(
                document=document,
                election=election)

            try:
                if voter.vote:

                    voter.vote.created = to_localtime(voter.vote.created)
                    context = dict(
                        message=f'La cédula {document} ya votó en la '
                        f'{voter.vote.polling_station.name} el {voter.vote.created}')
                    return render(request, 'index.html',
                                  context=context)
            except models.Vote.DoesNotExist:
                pass

        except Voter.DoesNotExist:
            context = dict(message=f'La cédula {document} no está registrada para esta elección')
            return render(request, 'index.html',
                          context=context)

        return redirect('poll', document=document)


class Poll(LoginRequiredMixin, View):
    """View to vote."""
    def get(self, request, document):
        polling_station = VotingJury.objects.get(
            user=self.request.user).polling_station
        election = polling_station.election
        lists = List.objects.filter(election=election).order_by('?')
        for list_ in lists:
            list_.description_list = list_.description.split('\n')

        context = dict(
            election=election,
            lists=lists,
            polling_station=polling_station,
            document=document
        )
        return render(request, 'poll.html', context=context)


class Vote(LoginRequiredMixin, View):
    def get(self, request, document):
        polling_station = self.request.user.votingjury.polling_station

        election = polling_station.election
        if not (election.start_date < Delorean().datetime < election.end_date):
            return JsonResponse({
                'message': f'La votación no se encuentra activa.'},
                status=400)

        try:
            voter = Voter.objects.get(
                document=document,
                election=polling_station.election)
        except Voter.DoesNotExist:
            return JsonResponse({
                'message': f'La cédula {document} no se encuentra registrada.'},
                status=400)

        try:
            try:
                list_ = models.List.objects.get(pk=int(request.GET.get('list')))
            except models.List.DoesNotExist:
                return JsonResponse({'message': 'La lista no existe', },
                                    status=400)

            vote = models.Vote.objects.create(
                voter=voter,
                list_choice=list_,
                polling_station=polling_station)
        except IntegrityError:
            vote = models.Vote.objects.get(voter=voter)

            return JsonResponse({
                'message': (f'Usted ya había votado en la '
                            f'{vote.polling_station.name} en {vote.created}')},
                                status=400)

        return JsonResponse({
            'message': (f'Voto realizado por {document} en la {vote.polling_station.name} por {list_.short_description} '
                        f'el {to_localtime(vote.created)}')})


class Report(UserPassesTestMixin, ListView):
    model = models.Election
    template_name = 'report.html'

    def test_func(self):
        return self.request.user.is_superuser


class ElectionDetail(UserPassesTestMixin, DetailView):
    model = models.Election
    template_name = 'election.html'

    context_object_name = 'election'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lists = list(self.object.list_set.all())

        votes = [list_.vote_set.all().count() for list_ in lists]

        percentages = [int(vote/sum(votes)*100) if sum(votes) > 0 else 0
                       for vote
                       in votes]

        context['series'] = mark_safe(', '.join(str(vote) for vote in votes))
        context['table'] = sorted(zip(lists, votes, percentages),
                                  key=lambda l: l[0].order)
        context['labels'] = mark_safe(', '.join(
            repr(f'{list_.short_description} - {percentage}%')
            for list_, percentage in zip(lists, percentages)))

        return context


class PollingStationDetail(UserPassesTestMixin, DetailView):
    """A voting report per polling station."""
    model = models.PollingStation
    template_name = 'station.html'

    context_object_name = 'election'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lists = list(self.object.election.list_set.all())

        votes = [list_.vote_set.filter(polling_station=self.object).count()
                 for list_ in lists]

        percentages = [int(vote/sum(votes)*100) if sum(votes) > 0 else 0
                       for vote
                       in votes]

        context['series'] = mark_safe(', '.join(str(vote) for vote in votes))
        context['table'] = sorted(zip(lists, votes, percentages),
                                  key=lambda l: l[0].order)
        context['labels'] = mark_safe(', '.join(
            repr(f'{list_.short_description} - {percentage}%')
            for list_, percentage in zip(lists, percentages)))

        return context


class QueryVotesView(View):
    def get(self, request):
        return render(request, 'votes.html')

    def post(self, request):
        return redirect(
            'votes-report',
            document=request.POST.get('document').replace(
                '.', '').replace(',', '').replace(' ', ''))


class VoteReport(ListView):
    context_object_name = 'votes'
    template_name = 'user_votes.html'

    def get_queryset(self):
        return models.Vote.objects.filter(
            voter__document=self.kwargs['document'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document'] = self.kwargs['document']
        return context
