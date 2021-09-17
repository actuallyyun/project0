from django.core.files.base import ContentFile
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse
from . import util
import encyclopedia
import random


class SearchForm(forms.Form):
    query = forms.CharField(label="New Query")


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)


class EditPageForm(forms.Form):
    newcontent = forms.CharField(widget=forms.Textarea, label="Make changes")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


def get_page(request, title):
    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/title.html", {
            "content": entry,
            "title": title
        })
    else:
        return HttpResponse("Error:Page Not Found")


def search_entry(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            # receieve a query and handle it
            entry = util.get_entry(query)
            # if query matchs, redirect to the entry page
            if entry:
                return HttpResponseRedirect(reverse('encyclopedia:title', args=[query]))

            # if not, show a search results page that displays a
            #  list of all the entries
            else:
                search_results = []
                entries = util.list_entries()
                for entry in entries:
                    if query.lower() in entry.lower():
                        search_results.append(entry)

                # TODO generate a result page if its a subtring
                return render(request, "encyclopedia/searchResults.html", {
                    "searchResutls": search_results,
                    "query": query
                })

    return render(request, "encyclopedia/index.html", {
        "form": SearchForm()
    })


def new_page(request):
    # get the new title and verify it
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data['title']
            entries = util.list_entries()
            if (new_title in entries):
                return HttpResponse("This entry already exists.")

            else:
                content = form.cleaned_data['content']
                util.save_entry(new_title, content)
                return HttpResponseRedirect(reverse('encyclopedia:title', args=[new_title]))

        else:
            return HttpResponse("form not valid")

    return render(request, "encyclopedia/new.html", {
        "newpageform": NewPageForm()
    })


def edit_page(request, title):
    if request.method == "POST":
        # get data from the "Edit" action
        content = util.get_entry(title)
        # pre-populate the textarea
        f = EditPageForm(initial={'content': content})
        # Return the page with exisitng entry data
        return render(request, "encyclopedia/edit.html", {
            "editpageform": f,
            "entry": content,
            "title": title

        })


def submit_edit(request, title):
    if request.method == "POST":
        # Get data from the form
        form = EditPageForm(request.POST)
        # verify and clean the data
        if form.is_valid():
            new_content = form.cleaned_data['newcontent']
            util.save_entry(title, new_content)
            return HttpResponseRedirect(reverse('encyclopedia:title', args=[title]))

    return None


def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    random_content = util.get_entry(random_entry)
    return render(request, "encyclopedia/title.html", {
        "content": random_content,
        "title": random_entry
    })
