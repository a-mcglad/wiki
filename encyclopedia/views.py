from django.shortcuts import render
from markdown import Markdown

from . import util

mk = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if title in util.list_entries():
        return render(request, "encyclopedia/entry.html", {
            "text": mk.convert(util.get_entry(title)),
            "title": title
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Page does not exist",
            "title": title
        })