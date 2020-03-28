from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from accounts.models import CustomUser
from content.models import Note, Course


class SearchNoteView(ListView):
    template_name = 'search/view.html'
    model = Note

    def get_context_data(self, **kwargs):
        context = super(SearchNoteView, self).get_context_data(**kwargs)
        request = self.request
        print(request.GET)
        query = request.GET.get('q', 'None')
        if query is not None:
            lookups = Q(title__icontains=query) | Q(course__title__icontains=query) | Q(subject__title__icontains=query)
            note = Note.objects.filter(lookups).distinct()
            lstatus = []
            providers = []
            for n in note:
                prv = CustomUser.objects.get(id=n.user_id)
                providers.append(prv.username)
                if n.upvotes.filter(id=request.user.id).exists():
                    lstatus.append(True)
                else:
                    lstatus.append(False)
            context['data'] = zip(note, lstatus, providers)
            return context
        return Note.objects.none()
