from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# Create your views here.
def home(request):
    return render(request, "base.html")

def new_search(request):

    search = request.POST.get("search")
    URL="http://weather.ba/vremenska-prognoza/{}"
    page = requests.get(URL.format(str(search).lower()))
    soup = BeautifulSoup(page.content, "html.parser")
    forecast = soup.find(id="main-content")
    temp_low=[temp.getText() for temp in forecast.findAll("td", {"class": "min"})]
    temp_high=[temp.getText() for temp in forecast.findAll("td", {"class": "red"})]
    forecast=soup.find("table", {"class": "meteo-tabela"})
    day=[temp.getText() for temp in forecast.findAll("th")]
    forecast=soup.find("tr", {"class": "odd padavine"})
    padaline=[temp.getText() for temp in forecast.findAll("td")]
    forecast=soup.find("tr", {"class": "even vetar"})
    vjetar=[temp.getText() for temp in forecast.findAll("span", {"class": "ver-middle"})]
    img_urls=[temp["src"] for temp in forecast.findAll("img")]
    grad=str(search).title()
    all_data=list(zip(temp_low,temp_high,day[1:],padaline[1:],vjetar,img_urls))

    front_end={
        "datas":all_data,
        "grad":grad

    }
    return render(request,"my_app/new_search.html",front_end)