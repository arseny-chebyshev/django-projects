from django.shortcuts import render
# Create your views here.
def sessionview(request):
    template = "user_sessions/main.html"
    visits = request.session.get('visits', 0) + 1
    request.session['visits'] = visits
    if visits > 2:
        del(request.session['visits'])
    old_cookie = request.COOKIES.get('dj4e_cookie')
    ctx = {'old_cookie': old_cookie, 'visits': visits}
    resp = render(request, template, ctx)
    resp.set_cookie('dj4e_cookie', '63c94b74', max_age=10)
    return resp
