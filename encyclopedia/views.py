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