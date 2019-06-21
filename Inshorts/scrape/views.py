from django.shortcuts import render, HttpResponse
import json
from datetime import date
from scrape.news_scrape_temp import scrape
# Create your views here.

#dated = str(datetime.date.today())
def flagging(news):
    for index,i in enumerate(news):
        b = eval(i)
        b['flag'] = 1
        news[index] = str(b)
    return news

def choose_date(request):
    if request.method == 'POST':
        dated = request.POST.get('dated')
        articles = scrape(str(dated))
    else:
        articles = scrape()

    global national_news, asia_news, world_news, sports_news
    national_news = articles['national']
    asia_news = articles['asia']
    world_news = articles['world']
    sports_news = articles['sports']
    return render(request, 'scrape/form.html', {'national': national_news,
                                                'asia': asia_news,
                                                'world': world_news,
                                                'sports': sports_news})
    
def store(request):
    if request.method == 'POST':
        national = flagging(request.POST.getlist('national'))
        asia = flagging(request.POST.getlist('asia'))
        world = flagging(request.POST.getlist('world'))
        sports = flagging(request.POST.getlist('sports'))

        yes_list = {"India News": national, "Asia News": asia, "World News": world, "Sports News": sports}
        with open('write_yes.json','r') as outfile:
            list1 = json.load(outfile)
            if list1 == []:
                with open('write_yes.json', 'w') as out:
                    json.dump(yes_list, out, indent=2)

            else:
                list1['India News'] += yes_list['India News']
                list1['Asia News'] += yes_list['Asia News']
                list1['World News'] += yes_list['World News']
                list1['Sports News'] += yes_list['Sports News']
                with open('write_yes.json', 'w') as out:
                    json.dump(list1, out, indent=2)


        def make_no_list(cat):
            temp = []
            for article in cat:
                if article['flag'] == 0:
                    temp.append(article)
            return temp
        
        no_list = {"India News": make_no_list(national_news), 
                   "Asia News": make_no_list(asia_news), 
                   "World News": make_no_list(world_news), 
                   "Sports News": make_no_list(sports_news)}

        with open('write_no.json','r') as outfile:
            list1 = json.load(outfile)
            if list1 == []:
                with open('write_no.json', 'w') as out:
                    json.dump(no_list, out, indent=2)

            else:
                list1['India News'] += no_list['India News']
                list1['Asia News'] += no_list['Asia News']
                list1['World News'] += no_list['World News']
                list1['Sports News'] += no_list['Sports News']
                with open('write_no.json', 'w') as out:
                    json.dump(list1, out, indent=2)
            
        return HttpResponse('<center><h2> Submitted Successfully!</h2></center>')

        



        
