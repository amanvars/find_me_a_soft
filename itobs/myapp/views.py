# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django.views.generic import TemplateView


class MainPage(TemplateView):
    template_name = "index.html"

def dev_temp(request):
    return render(request, "dev.html", {})

from bs4 import BeautifulSoup
import requests


def get_info(request):
    name=""
    if 'ipt' in request.GET:
        i = request.GET['ipt']
        name=i[1:-1]
        print(name)
    else:
        name=None
        print("NO")

    url = "https://filehippo.com/search?q=" + name
    print(url)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    title = soup.find("span", {"class": "program-title-text"}).find("h2").text
    url = soup.find("div", {"class": "program-entry-header"}).find("a", href=True)
    url2 = "https://filehippo.com" + url["href"]
    r = requests.get(url2)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    description = soup.find("div", {"id": "fh-program-description-text-column"}).find_all("p")
    text = ""
    for d in description:
        text += (d.text)


    comp =  soup.find("div",{"id":"publisher-licence-details"}).text

    type =  soup.find("div",{"class":"col-md-8 nopadding"}).find("ul").find_all("li")
    tags = []
    i=0
    for t in type:
        if i!=0 and i!=len(type)-1:
            tags.append(t.text.strip())
        i+=1
    print(tags)

    rtd = soup.find_all("div",{"class":"related-program-entry"})
    related =[]

    for t in rtd:
        related.append(t.text)


    print(related)
    url3 = url2 + "history"
    r = requests.get(url3)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    ver = soup.find("ol", {"id": "program-history-list"})
    version = []
    for v in ver:
        if (v.find("a")) is not -1:
            version.append({"name": v.find("a").text, "date": v.find("span", {"class": "detailLine"}).text})
    #return i, text, version, tags
    print(version)
    desc ={}
    desc['name']= name
    desc['comp']= comp
    desc['text']= text
    desc['reld']= related
    desc['ver']= version
    desc['tag']= tags
    return JsonResponse(desc)



#name, text, version, tag = get_info("chrome")
#print(name)
