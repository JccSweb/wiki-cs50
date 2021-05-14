import re
import random
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown

from . import util

class AddEntry(forms.Form):
    title = forms.CharField(label = "Insert entry title", max_length=50)
    content = forms.CharField(label = "insert content", widget=forms.Textarea)

    def __init__(self,*args,**kwargs):
        super(AddEntry, self).__init__(*args, **kwargs)
        if self.initial:
            self.fields["title"].widget.attrs['readonly'] = True

def newPage(request):
    if request.method == "POST":
        form = AddEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # preventing different case from creating duplicating pages
            list_of_possibilities = util.list_entries()
            for possibility in list_of_possibilities:
                if possibility.lower() == title.lower():
                    print("false")
                    return render(request, "encyclopedia/new_entry.html", {
                        "form":form,
                        "message": "There is already an entry with that name"
                         })
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=(title,)))
    else:
        form = AddEntry()
        return render(request, "encyclopedia/new_entry.html",{"form":form})

def edit(request, title):
    if request.method == "POST":
        form = AddEntry(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            print("saved")
            return HttpResponseRedirect(reverse("encyclopedia:index"))
    else:
        initial = {
            "content":util.get_entry(title)
        }
        form = AddEntry(initial={"title":title, "content":util.get_entry(title)})
        return render(request, "encyclopedia/edit.html",{
            "form":form,
            "title":title
        })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })


def entry(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return render(request, "encyclopedia/errors.html",{
        "message": "The requested entry does not exist!",
        })
    else:
        markdowner = Markdown()
        entry = markdowner.convert(entry)
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "any":entry
        })

def results(request):
    form = request.POST
    value = form['q']
    lower_value = value.lower()
    list_entries = util.list_entries()
    for entry in list_entries:
        if lower_value == entry.lower():
            print(entry)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=(entry,)))
    else:
        pattern = re.compile(lower_value)
        new_list_of_possible_entries = []
        for possible in list_entries:
            possible_lower = possible.lower()
            if (pattern.search(possible_lower)) is not None:
                new_list_of_possible_entries.append(possible)
        return render(request, "encyclopedia/results.html",{
        "entries":new_list_of_possible_entries,
        "search":value
        })


        
def randomEntry(request):
    list_of_entries = util.list_entries()
    number_of_entries = len(list_of_entries)
    random_number = random.randint(0,(number_of_entries-1))
    entry_name = list_of_entries[random_number]
    return HttpResponseRedirect(reverse("encyclopedia:entry", args=(entry_name,)))