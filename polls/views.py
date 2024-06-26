import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import Session, Wine
from .forms import WineScoreForm, UploadFileForm
from .utils import add_score_excel, create_workbook, handle_new_wines
from VoyageDuVin import settings


def index(request, session):
    if request.method == "POST":
        form = WineScoreForm([], request.POST)
        if form.is_valid():
            add_score_excel(list(form.data.values())[1:])
            return HttpResponseRedirect("thanks")
        else:  # Probably submitted from the raw html page
            add_score_excel(list(form.data.values())[1:])
            return HttpResponseRedirect("thanks")

    # get wines
    wines_qs = Session.objects.filter(pk=session).first().wines.order_by('order').all() if Session.objects.filter(pk=session).first() is not None else []
    wines = list(wines_qs)
    wine_tags = ['name_dummy']
    for wine_qs in wines_qs:
        tags_qs = wine_qs.tags.all()
        wine_tags.append(list(tags_qs))

    # prepare context
    form = WineScoreForm(wines=wines)
    wines.insert(0, 'name_dummy')
    form_data = zip(form, wines, wine_tags)
    return render(request, "polls/index.html", {"form": form_data})


def thanks(request):
    return render(request, "polls/thanks.html", {})

def fuckyou(request):
    return render(request, "polls/fuckyou.html", {})

def secret(request):
    return render(request, "polls/secret.html", {})

def add_wines(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST)
        if form.is_valid:
            handle_new_wines(request.POST["files"])
            return HttpResponseRedirect("add")
    else:
        form = UploadFileForm()
    return render(request, "polls/secret_add.html", {})
    


def download_results(request):
    if not (os.path.isfile(os.path.join(settings.MEDIA_ROOT, "results.xlsx"))):
        create_workbook()

    file = open(os.path.join(settings.MEDIA_ROOT, "results.xlsx"), 'rb')
    response = HttpResponse(file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = "attachment; filename=results.xlsx"

    return response


def delete_results(request):
    if request.method == "POST":
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, "results.xlsx")):
            os.remove(os.path.join(settings.MEDIA_ROOT, "results.xlsx"))

        return render(request, "polls/secret_delete.html", {})

    return HttpResponseRedirect("fuckyou")  # You only get here if you're a bitch


def vins(request):
    return render(request, "polls/vins.html", {})