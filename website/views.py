from django.shortcuts import render
from django.http import HttpResponse
from website.forms import NameForm

def index_view(request):
    return render(request, "website/index.html")

def about_view(request):
    return render(request, "website/about.html")

def contact_view(request):
    return render(request, "website/contact.html")

def test(requset):
    if requset.method == 'POST':
        form = NameForm(requset.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            print(name, email, subject, message)
            return HttpResponse('done')
        else:
            return HttpResponse('not valid')
    form = NameForm()
    return render(requset, 'test2.html', {'form': form })