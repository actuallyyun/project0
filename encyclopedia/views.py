from django.core.files.base import ContentFile
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse
from . import util
import encyclopedia


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
                    if query in entry:
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
                return render(request, "encyclopedia/new.html", {
                    "newpageform": form
                })
            else:
                content = form.cleaned_data['content']
                util.save_entry(new_title, content)
                return HttpResponseRedirect(reverse('encyclopedia:index'))

        else:
            return HttpResponse("form not valid")

    return render(request, "encyclopedia/new.html", {
        "newpageform": NewPageForm()
    })


def edit_page(request):

    return render(request, "encyclopedia/edit.html", {
        "editpageform": EditPageForm()
    })
