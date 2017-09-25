from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Voter, VotingJury


class Index(LoginRequiredMixin, View):
    """Form to login with document. No password required."""
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        document = request.POST.get('document')

        try:
            voter = Voter.objects.get(
                document=document,
                election=VotingJury.objects.get(user=self.request.user).polling_station.election)
        except Voter.DoesNotExist:
            context = dict(message=f'La cédula {document} no está registrada para esta elección')
            return render(request, 'index.html',
                          context=context)

        return redirect('poll', document=document)


class Poll(LoginRequiredMixin, View):
    """View to vote."""
    def get(self, request, document):
        return render(request, 'poll.html')
