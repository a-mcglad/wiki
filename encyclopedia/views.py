from django.shortcuts import render, redirect
from markdown import Markdown
from random import randrange

from . import util

mk = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def edit(request, title):
    if request.method == "GET":
         print("title is ", title)
         return render(request, "encyclopedia/edit.html", {
            "text": util.get_entry(title),
            "title": title
        })
    else:
        title = request.POST.get("title", "")
        text = request.POST.get("text", "").replace("\r\n", "\n").replace("\r", "\n")
        f = open(f"entries/{title}.md", "w")
        f.write(text)
        f.close
        return redirect("entry", title=title)


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

    
def new(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
            "message": "Page already exists",
            "title": title
        })
        content = request.POST.get("text", "")
        f = open(f"entries/{title}.md", "x")
        f.write(content)
        f.close()
        return redirect("index")
    else:
        return render(request, "encyclopedia/new.html")

def random_page(request):
    entries = util.list_entries()
    choice = entries[randrange(0, len(entries))]
    return redirect(entry, title=choice)
    
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