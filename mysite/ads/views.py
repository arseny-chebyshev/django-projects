from django.http import HttpResponse
from django.views import View
from ads.models import Ad, Comment, Fav
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from ads.forms import CreateForm, CommentForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_deny
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError


class AdListView(OwnerListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    def get(self, request):
        search_query = request.GET.get("search", False)
        if search_query:
            query = Q(title__icontains=search_query)
            query.add(Q(text__icontains=search_query), Q.OR)
            query.add(Q(price__icontains=search_query), Q.OR)
            query.add(Q(tags__name__in=[search_query]), Q.OR)
            ad_list = Ad.objects.filter(query).select_related().distinct().order_by('-updated_at')[:10]
        else:
            ad_list = Ad.objects.all().order_by('updated_at')[:10]
        favorites = []
        if request.user.is_authenticated:
            rows = request.user.favorite_ads.values('id')
            favorites = [row['id'] for row in rows]
        ctx = {'favorites': favorites, 'ad_list': ad_list, 'search': search_query}
        return render(request, self.template_name, ctx)

class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id = pk)
        comments = Comment.objects.filter(ad=ad).order_by('-updated_at')
        comment_form = CommentForm()
        ctx = {'ad': ad, 'comments': comments, 'comment_form': comment_form}
        return render(request, self.template_name, ctx)

class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        #capitalize tags for uniforming purpose
        form.cleaned_data['tags'] = [tag.capitalize() for tag in form.cleaned_data['tags']]

        # Add owner to the model before saving
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()
        form.save_m2m()
        return redirect(self.success_url)

class AdUpdateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        #capitalize tags for uniforming purpose
        form.cleaned_data['tags'] = [tag.capitalize() for tag in form.cleaned_data['tags']]
        ad = form.save(commit=False)
        ad.save()
        form.save_m2m()
        return redirect(self.success_url)


class AdDeleteView(OwnerDeleteView):
    model = Ad


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=ad)
        comment.save()
        return redirect(reverse('ads:ad_detail', args = [pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = 'ads/comment_delete.html'
    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail', args=[ad.id])

""" These 2 methods exempt from CSRF tokens
    since they are involved in JQuery request
    and JS makes post requests to them """
@method_decorator(csrf_exempt, name="dispatch")
class AdFavorite(LoginRequiredMixin, View):
    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        fav = Fav(owner=request.user, ad=ad)
        try:
            fav.save()
        except IntegrityError:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name="dispatch")
class AdUnfavorite(LoginRequiredMixin, View):
    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        try:
            Fav.objects.get(owner=request.user, ad=ad).delete()
        except Fav.DoesNotExists:
            pass
        return HttpResponse()

# for the detailed view on the uploaded pictures
def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response
