from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .models import Breed, Cat
from django.urls import reverse_lazy


class CatList(View):
    def get(self, request):
        breed_count = Breed.objects.all().count()
        cat_list = Cat.objects.all()
        context = {'breed_count': breed_count, 'cat_list': cat_list}
        return render(request, 'cats/cat_list.html', context)


class BreedList(View):
    def get(self, request):
        breed_list = Breed.objects.all()
        context = {'breed_list': breed_list}
        return render(request, 'cats/breed_list.html', context)


class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')

class CatUpdate(UpdateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')

class CatDelete(DeleteView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')


class BreedCreate(CreateView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:all')

class BreedUpdate(UpdateView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:all')

class BreedDelete(DeleteView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:all')
