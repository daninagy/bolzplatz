from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render, render_to_response, RequestContext
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.decorators import method_decorator

from users.models import Profile, Group


class ScoreHome(View):
    template_name = 'scores/scores_home.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        profiles = []
        if slug is not None:
            try:
                profiles = Profile.objects.filter(
                    group=Group.objects.get(slug=slug)).order_by('score').reverse()
                group = slug
            except:
                pass
        if not profiles:
            profiles = Profile.objects.all().order_by('score').reverse()
            group = 'All Groups'

        ranking = []
        rank = 0
        for profile in profiles:
            this_score = profile.score
            if rank > 0:
                if this_score != last_score:
                    rank += 1
                this_rank = rank
            else:
                rank = 1
                this_rank = 1
                last_score = this_score
            ranking.append((this_rank, str(profile.user), profile.score))

        # Build a list of groups containing members
        all_groups = Group.objects.all()
        active_groups = []
        for this_group in all_groups:
            if len(this_group.profile_set.all()):
                active_groups.append(this_group.slug)

        return render(
            request,
            self.template_name,
            {'ranking': ranking,
             'active_groups': active_groups,
             'group': group}
        )
