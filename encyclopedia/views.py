from django.shortcuts import render, redirect
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
    
def search(request):
    entries = util.list_entries()
    q = request.GET.get("q", "")
    if q in entries:
        return redirect("entry", title=q)
    else:
        list = []
        for entry in entries:
            if q.lower() in entry.lower():
                list.append(entry)
        return render(request, "encyclopedia/search.html", {
            "entries": list,
            "title": q
        })



    # if q in util.list_entries():
    #     return render(request, "encyclopedia/entry.html", {
    #         "text": mk.convert(util.get_entry(q)),
    #         "title": q
    #     })
    # else:
    #     list = []
    #     for i in util.list_entries():
    #         if q in i:
    #             list.append(i)
    #     return render(request, "encyclopedia/search.html", {
    #         "entres": list,
    #         "text": mk.convert(util.get_entry(q)),
    #         "title": q
    #     })