from django.core.files.base import ContentFile
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse
from . import util
import encyclopedia
import random


class SearchForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control'}))


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}))


class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


def get_page(request, title):
    # Render the entry page with the requested title.

    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/title.html", {
            "content": entry,
            "title": title,
            "form": SearchForm()
        })
    else:
        raise Http404("Error:Page Not Found.")


def search_entry(request):
    # search wiki entries by entering an keyword. If it matches, redirect to the entry page. If not, show
    # results that contain this keyword. It should be case insensitive

    if request.method == "GET":
        form = SearchForm(request.GET)
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

                # generate a result page if its a subtring
                return render(request, "encyclopedia/searchResults.html", {
                    "searchResutls": search_results,
                    "query": query,
                    "form": SearchForm()
                })

    return render(request, "encyclopedia/index.html", {
        "form": SearchForm()
    })


def new_page(request):
    # To create a new entry

    # get the new title and verify it
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data['title']
            entries = util.list_entries()

            for entry in entries:
                # if this entry already exists, display an error message and the create new page view
                if new_title.lower() == entry.lower():
                    error = "Creating a new page failed. This entry already exists."
                    return render(request, "encyclopedia/new.html", {
                        "error": error,
                        "new_page_form": NewPageForm()
                    })

                # otherwise save the new entry and redirect to the new entry page.
                else:
                    content = form.cleaned_data['content']
                    util.save_entry(new_title, content)
                    return HttpResponseRedirect(reverse('encyclopedia:title', args=[new_title]))

    return render(request, "encyclopedia/new.html", {
        "new_page_form": NewPageForm(),
        "form": SearchForm()
    })


def edit_page(request, title):
    # To edit an entry

    if request.method == "POST":
        # get data from the "Edit" action
        content = util.get_entry(title)

        # pre-populate the textarea
        edit_form = EditPageForm(
            initial={'title': title, 'content': content})

        # Return the page with exisitng entry data

        return render(request, "encyclopedia/edit.html", {
            "editpageform": edit_form,
            "title": title,
            "form": SearchForm()
        })

    else:
        edit_form = EditPageForm()
        return render(request, 'encyclopedia/edit.html', {
            'editpageform': edit_form,
            "form": SearchForm()
        })


def submit_edit(request, title):

    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
        # verify and clean the data
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('encyclopedia:title', args=[title]))

    else:
        edit_form = EditPageForm()
        return render(request, 'encyclopedia/edit.html', {
            'editpageform': edit_form,
            "form": SearchForm()
        })


def random_page(request):
    # generate random entry pages

    entries = util.list_entries()
    random_entry = random.choice(entries)
    return HttpResponseRedirect(reverse('encyclopedia:title', args=[random_entry]))
