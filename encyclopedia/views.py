from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import util
import random
from markdown2 import Markdown

class NewWikiEntry(forms.Form):
    entry = forms.CharField(label="New Entry")
    content = forms.CharField(widget=forms.Textarea())

# class EditNewWikiEnrty(forms.form):

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    print(f"title: {title}")
    print(util.get_entry(title))
    markdowner = Markdown()
    return render(request, "encyclopedia/wiki.html", {"content": markdowner.convert(util.get_entry(title)),  "title": title})

def add(request):
    if request.method == "POST":
        form = NewWikiEntry(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            content = form.cleaned_data["content"]
# cleaned_data returns dictionary validated entry field and its values
            #if until.get_entry checks title of entry and title exists
                # then display page already exists
            if util.get_entry(entry) != None:
                return render(request, "encyclopedia/add.html", {
                    "form": form, "error": "Error: page by that name already exists"
                    })
            
            util.save_entry(entry, content)
            return HttpResponseRedirect(f"/wiki/{entry}")
        else: 
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    return render(request, "encyclopedia/add.html", {
        "form": NewWikiEntry()
    })

def edit(request, title):
    if request.method == "POST":
        form = NewWikiEntry(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            content = form.cleaned_data["content"]
            
            util.save_entry(entry, content)
            return HttpResponseRedirect(f"/wiki/{entry}")
        else: 
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "form": NewWikiEntry({"entry": title, "content": content}), "title": title
    })

def search(request):
    wikis = []
    markdowner = Markdown()
    print(request.POST)
    entry = request.POST["q"]
    print(entry)
    if util.get_entry(entry) != None:
        return render(request, "encyclopedia/wiki.html", {"content": markdowner.convert(util.get_entry(entry)),  "title": entry})
    for list_item in util.list_entries():
        if entry in list_item:
            wikis.append(list_item)
    return render(request, "encyclopedia/search.html", {
        "entries": wikis, 
    })

    
def random_page(request):
    markdowner = Markdown()
    random_choice = random.choice(util.list_entries())
    print(random_choice)
    return render(request, "encyclopedia/wiki.html", {"content": markdowner.convert(util.get_entry(random_choice)),  "title": random_choice})
    



