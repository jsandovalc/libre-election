from delorean import Delorean
from django import template
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Voter, VotingJury, List


class Index(LoginRequiredMixin, View):
    """Form to login with document. No password required."""
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        document = request.POST.get('document')

        try:
            election = VotingJury.objects.get(user=self.request.user).polling_station.election

            if not(election.start_date < Delorean().datetime < election.end_date):
                context = dict(message=f'La elección no se encuentra habilitada')
                return render(request, 'index.html',
                              context=context)

            voter = Voter.objects.get(
                document=document,
                election=election)
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
        lists = List.objects.filter(election=election)
        for list_ in lists:
            list_.description_list = list_.description.split()

        context = dict(
            election=election,
            lists=lists,
            polling_station=polling_station
        )
        return render(request, 'poll.html', context=context)
