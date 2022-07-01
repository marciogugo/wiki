import os
import re
import random

from string import ascii_lowercase
from xml.etree.ElementInclude import default_loader
from markdown import markdown
from encyclopedia.forms import EntryForm, EditEntryForm
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage, FileSystemStorage
from .import util
 
from markdown import markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search_view(request):
    _, filenames = default_storage.listdir("entries")

    Myarg = request.GET.get('query')

    entries_found = [MySearch[:-3] for MySearch in filenames if Myarg.lower() in MySearch.lower()]

    if len(entries_found) > 1:
        return render(request, "index.html", {"entries": entries_found})
    else:
        res = [x for x in entries_found if re.search(Myarg, x.lower())]

        if len(res) > 0:
            return render(request, "index.html", {"entries": entries_found})
        else:
            entry_document = util.get_entry(Myarg)

            if entry_document == None:
                entry_document = '\n#'+ Myarg +'\n#### The requested **entry** was not found.\nPlease, try again using *different* ***keywords***.'
                return render(request, "404.html", {"title": "404 Not found", "error_body": entry_document })
            else:    
                return render(request, "entry.html", {"title": Myarg, "body": entry_document })

@csrf_protect
def new_entry_view(request):
    if request.method == "GET":
        context = {}
        context['entry_form'] = EntryForm()
        return render(request, "new_entry.html", context=context)
    else:
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('index'))
        else:
            context = {}
            context['entry_form'] = EntryForm()

            title = request.POST.get('formTitle')
            content = request.POST.get('formContent')

            if (title != "") & (content != ""):
                DEFAULT_FILE_STORAGE = os.path.join(settings.BASE_DIR, 'entries\\')

                fs = FileSystemStorage(location=DEFAULT_FILE_STORAGE,file_permissions_mode=None,directory_permissions_mode=None)

                file_to_save = DEFAULT_FILE_STORAGE + title + ".md"

                if fs.exists(file_to_save):
                    content = '\n# Error\n#### The requested **Entry** already exists.\nPlease, choose another ***title*** for the entry.'
                    return render(request,"error.html",  {"title": "Error", "error_body": content})
                else:
                    fs.save(file_to_save, ContentFile(content))
                    return render(request,"entry.html",  {"title": title, "body": content})
            else:
                content = '\n# Error\n#### You must inform the **Entry** title and content.\nPlease, fill out the ***title*** and ***content*** for the entry.'
                return render(request,"error.html",  {"title": "Error", "body": content})

@csrf_protect
def edit_entry_view(request, entry):
    if ('back' in request.POST) or ('cancel' in request.POST):
        return HttpResponseRedirect(reverse('index'))
    else:
        if ('save' in request.POST):
            newTitle = request.POST.get('formTitle')
            newContent = request.POST.get('formContent')

            if (newTitle != "") & (newContent != ""):
                newTitle = request.POST.get('formTitle').split()[0]
                DEFAULT_FILE_STORAGE = os.path.join(settings.BASE_DIR, 'entries\\')

                fs = FileSystemStorage(location=DEFAULT_FILE_STORAGE,file_permissions_mode=None,directory_permissions_mode=None)

                file_to_save = DEFAULT_FILE_STORAGE + newTitle + ".md"

                if fs.exists(file_to_save):
                    fs.delete(file_to_save)
                else:
                    if entry != newTitle:       
                        file_to_delete = DEFAULT_FILE_STORAGE + entry + ".md"
                        fs.delete(file_to_delete)

                print(newContent)
                
                fs.save(file_to_save, ContentFile(newContent))

                return HttpResponseRedirect(reverse('get-entry', args=[newTitle]))
            else:
                content = '\n# Error\n#### You must inform the **Entry** title and content.\nPlease, fill out the ***title*** and ***content*** for the entry.'
                return render(request,"error.html",  {"title": "Error", "body": content})
        else:
            content = util.get_entry(entry)

            edit_data = {'formTitle': entry,
                         'formContent': content
                        }

            Entryform = EditEntryForm(request.POST or None, initial = edit_data)

            context = {
                'edit_entry_form': Entryform,
                'formContent': content
            }        
            return render(request, "edit_entry.html", context)

def random_view(request):
    myEntries = os.listdir("entries")
    newList = []

    for index in range(len(myEntries)):
        newList.append(myEntries[index][:-3])

    name = random.choice(newList)

    return render(request, "entry.html", {"title": name, "body": util.get_entry(name)})

def get_entry_view(request, entry):
    if 'back' in request.POST:
        return HttpResponseRedirect(reverse('index'))
    else:
        content = util.get_entry(entry)
        if content == None:
            content = '\n#'+ entry +'\n#### The requested **entry** was not found.\nPlease, try again using *different* ***keywords***.'
            return render(request, "404.html", {"title": "404 Not found", "error_body": content})
        else:
            return render(request,"entry.html", {"title": entry, "body": util.get_entry(entry)})

def error_404_view(request, exception):
    entry_document = '\n# Error 404\n#### The requested **URL** was not found.\nPlease, try again using a *different* ***URL***.'
    return render(request, "404.html", {"title": "Error 404", "error_body": entry_document})

def error_500_view(request):
    entry_document = '\n# Error 500\n#### The requested **page** does not exist.\nPlease, contact our ***technical support*** or'
    return render(request, "500.html", {"title": "Error 500", "error_body": entry_document})    
