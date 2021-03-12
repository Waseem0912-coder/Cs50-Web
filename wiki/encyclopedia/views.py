
from django.shortcuts  import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from random import choice
from markdown2 import Markdown
from . import util


class SearchForm(forms.Form):
    query = forms.CharField(label="Search Encyclopedia", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8'}))

class CreateForm(forms.Form):
    title = forms.CharField(label="Type in the title of the entry", widget=forms.TextInput(attrs={'class' : 'form-control col-md-4 col-lg-4'}))
    content = forms.CharField(label="Type in content of your entry", widget=forms.Textarea(attrs={'class': 'form-control'}))

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()     })

def page_view(request, title):
    entry = util.get_entry(title)
    if entry==None:
        return render(request, "encyclopedia/error.html", {
            "content":"No entry with such title, please try the search bar"
        })
    else:
        html_content = Markdown().convert(entry)
        #encyclopedia
        return render(request, "encyclopedia/page_view.html", {
            "content":html_content, "title":title })


def search(request):
    search = request.GET.get('q')
    found = []
    for find in util.list_entries():
        if search.lower() == find.lower():
            return HttpResponseRedirect(reverse("encyclopedia:page_view", kwargs={"title": find}
))

        if search.lower() in find.lower():
            found.append(find)
    return render(request, "encyclopedia/search.html", {
        "entries": found
    })

def create(request):
    if request.method =="POST":
       create =  CreateForm(request.POST)
       if create.is_valid():
            title =  create.cleaned_data["title"]
            content = create.cleaned_data["content"]
            if(util.get_entry(title) is None):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:page_view", kwargs={"title": title}
                ))
            if(util.get_entry(title)) is not None:
                return HttpResponseRedirect(reverse("encyclopedia:page_view", kwargs={"title": title}))
    else:
        return  render(request, "encyclopedia/create.html", {
            "creation":CreateForm()
        } )


def edit(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)

        context = {
            'edit': Edit(initial={'textarea': page}),
            'title': title
        }

        return render(request, "encyclopedia/edit.html", context)
    else:
        form = Edit(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title,textarea)
            return HttpResponseRedirect(reverse("encyclopedia:page_view", kwargs={"title": title}))


def random_page(request):
      return page_view(request,choice( util.list_entries()))

