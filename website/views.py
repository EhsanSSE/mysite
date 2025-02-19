from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from website.forms import NameForm, ContactForm, NewsletterForm
from django.contrib import messages


def index_view(request):
    return render(request, "website/index.html")

def about_view(request):
    return render(request, "website/about.html")

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.name = 'UNKNOWN'
            ticket.save()
            messages.add_message(request, messages.SUCCESS, 'Your Ticket submitted Successfully :)')
        else:
            messages.add_message(request, messages.ERROR, 'Your Ticket Didnt submitted')
    form = ContactForm()
    return render(request, "website/contact.html", {'form': form})

def newsletter_view(requset):
    if requset.method == 'POST':
        form = NewsletterForm(requset.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def test(requset):
    if requset.method == 'POST':
        form = ContactForm(requset.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('done')
        else:
            return HttpResponse('not valid')
    form = ContactForm()
    return render(requset, 'test2.html', {'form': form })