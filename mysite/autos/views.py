from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .models import Make, Auto
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class MainView(LoginRequiredMixin, View):
    def get(self, request):
        make_objs_count = Make.objects.all().count()
        auto_list = Auto.objects.all()
        context = {'make_count': make_objs_count, 'auto_list': auto_list}
        return render(request, 'autos/auto_list.html', context)

class MakeView(LoginRequiredMixin, View):
    def get(self, request):
        make_list = Make.objects.all()
        context = {'make_list': make_list}
        return render(request, 'autos/make_list.html', context)

class MakeCreate(LoginRequiredMixin, CreateView):
    model = Make
    fields = '__all__'
    success_url = reverse_lazy('autos:all')

class MakeUpdate(LoginRequiredMixin, UpdateView):
    model = Make
    fields = '__all__'
    success_url = reverse_lazy('autos:all')

class MakeDelete(LoginRequiredMixin, DeleteView):
    model = Make
    fields = '__all__'
    success_url = reverse_lazy('autos:all')

class AutoCreate(LoginRequiredMixin, CreateView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos:all')

class AutoUpdate(LoginRequiredMixin, UpdateView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos:all')

class AutoDelete(LoginRequiredMixin, DeleteView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos:all')
