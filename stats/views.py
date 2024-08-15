import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
#pip3 install BeautifulSoup,requests

def format_event_name(event_name,date_str):
    formatted_name=event_name.strip().lower().replace(' ','-').replace(':','')
    if 'ufc-fight-night' in formatted_name:
        formatted_name = re.sub(r'ufc-fight-night.*', 'ufc-fight-night-', formatted_name)
        try:
            date_obj=datetime.strptime(date_str.strip(),'%B %d, %Y')
            formatted_date=date_obj.strftime('%B-%d-%Y').lower()
        except ValueError:
            formatted_date='unknown date'
        formatted_name=f"{formatted_name}{formatted_date}"
    else:
        parts=formatted_name.split('-',2)
        if len(parts)>1:
            formatted_name='-'.join(parts[:2])
        else:
            formatted_name=parts[0]
    return formatted_name

def all_events():
    base_url = "http://www.ufcstats.com/statistics/events/completed"
    events_data = []
    page = 1
    
    while True:
        url = f"{base_url}?page={page}"
        html = requests.get(url)

        if html.status_code != 200:
            continue
        
        s = BeautifulSoup(html.content, "html.parser")
        results = s.find(class_='b-statistics__table-events')
        if not results:
            break

        events = results.find_all('a', class_='b-link b-link_style_black')
        dates = results.find_all('span', class_='b-statistics__date')
        locations = results.find_all('td', class_="b-statistics__table-col b-statistics__table-col_style_big-top-padding")
        if not events:
            break

        for event, date, location in zip(events, dates, locations):
            events_data.append({
                "name": event.text.strip(),
                "date": date.text.strip(),
                "location": location.text.strip()
            })

        page += 1
    
    return events_data

def all_fighters():
    base_url="http://www.ufcstats.com/statistics/fighters?char={char}&page=all"
    fighters=[]
    for char in range(ord('a'),ord('z')+1):
        char = chr(char)
        url=base_url.format(char=char)
        html=requests.get(url)
        if(html.status_code!=200):
            continue
        s=BeautifulSoup(html.content,"html.parser")
        results=s.find_all(class_='b-statistics__table-row')
        if not results:
            continue

        for result in results:
            links=result.find_all('a',class_="b-link b-link_style_black")
            if len(links) >=3:
                first_name=links[0].text.strip()
                last_name=links[1].text.strip()
                nickname=links[2].text.strip()

                fighters.append({
                    'first_name':first_name,
                    'last_name':last_name,
                    'nickname':nickname,
                })
    return fighters

def scrape_upcoming_events():
    url="http://www.ufcstats.com/statistics/events/upcoming?page=all"      
    html=requests.get(url)
    s=BeautifulSoup(html.content,"html.parser")
    results=s.find(class_='b-statistics__entry')
    events=results.find_all('a',class_="b-link b-link_style_black")
    dates=results.find_all('span',class_="b-statistics__date")
    locations=results.find_all('td',class_="b-statistics__table-col b-statistics__table-col_style_big-top-padding")
    
    upcoming_fights=[]
    for event,date,location in zip(events,dates,locations):
        formatted_event=format_event_name(event.text,date.text)
        link_url=f"https://www.ufc.com/event/{formatted_event}"
        fight={
            'event':event.text.strip(),
            'date':date.text.strip(),
            'location':location.text.strip(),
            'link':link_url,
        }
        upcoming_fights.append(fight)
    return upcoming_fights

def search_fighter(request):
    query=request.GET.get('query','')
    if not query:
        return HttpResponse('Query parameter missing.', status=400)
    fighters=all_fighters()
    search_terms=query.lower().split()
    results=[f for f in fighters if any(term in f['first_name'].lower() or term in f['last_name'].lower() or term in f['nickname'].lower() for term in search_terms)]
    if not results:
        return HttpResponse("Fighter not found.",status=404)

    for fighter in results:
        fighter_name=f"{fighter['first_name'].lower()}-{fighter['last_name'].lower()}"
        fighter['ufc_url']=f"https://www.ufc.com/athlete/{fighter_name}"

    return render(request,"stats/search_results.html",{'fighters':results,'query':query})

def scrape_fighter_stats(ufc_url):
    html = requests.get(ufc_url)
    s = BeautifulSoup(html.content, "html.parser")
    results = s.find(class_="c-bio__info-details")
    stats = {}

    # Parsing bio1
    bio1 = results.find_all('div', class_="c-bio__row--1col")
    for row in bio1:
        label = row.find('div', class_='c-bio__label').text.strip()
        value = row.find('div', class_='c-bio__text').text.strip()
        key = label.lower().replace(' ', '_')
        stats[key] = value

    # Parsing bio2
    bio2 = results.find_all('div', class_="c-bio__row--2col")
    for row in bio2:
        fields = row.find_all('div', class_="c-bio__field c-bio__field--border-bottom-small-screens")
        for field in fields:
            label = field.find('div', class_="c-bio__label").text.strip()
            value = field.find('div', class_="c-bio__text").text.strip()
            key = label.lower().replace(' ', '_')
            stats[key] = value

    # Parsing bio3
    bio3 = results.find_all('div', class_="c-bio__row--3col")
    for row in bio3:
        fields = row.find_all('div', class_="c-bio__field")
        for field in fields:
            label = field.find('div', class_="c-bio__label").text.strip()
            value = field.find('div', class_="c-bio__text").text.strip()
            nested_value = field.find('div', class_="field__item")
            if nested_value:
                value = nested_value.text.strip()
            key = label.lower().replace(' ', '_')
            stats[key] = value

    results_list = s.find_all("div", class_="stats-records stats-records--two-column")

    for results2 in results_list:
        # Get striking accuracy and significant strikes stats (previous code)
        accuracy_svg = results2.find("svg", class_="e-chart-circle")
        if accuracy_svg:
            accuracy_text = accuracy_svg.find("text", class_="e-chart-circle__percent").text.strip()
            stats['striking_accuracy'] = accuracy_text

        stat_items = results2.find_all("dl", class_="c-overlap__stats")
        for item in stat_items:
            label = item.find("dt", class_="c-overlap__stats-text").text.strip()
            value = item.find("dd", class_="c-overlap__stats-value").text.strip()
            key = label.lower().replace('.', '').replace(' ', '_')
            stats[key] = value
        
        # Get additional stats from 'c-stat-compare' elements
        compare_stats = results2.find_all("div", class_="c-stat-compare")
        for compare in compare_stats:
            groups = compare.find_all("div", class_="c-stat-compare__group")
            for group in groups:
                number = group.find("div", class_="c-stat-compare__number").text.strip().replace('\n',' ').replace(' ','')
                label = group.find("div", class_="c-stat-compare__label").text.strip()
                suffix = group.find("div", class_="c-stat-compare__label-suffix")
                
                key = label.lower().replace('.', '').replace(' ', '_')
                value = number
                if suffix:
                    value += f" {suffix.text.strip()}"
                
                stats[key] = value

    
    print(stats)  
    return stats

def fighter_detail(request, first_name, last_name):
    fighters = all_fighters()
    fighter = next((f for f in fighters if f['first_name'].lower() == first_name.lower() and f['last_name'].lower() == last_name.lower()), None)
    if not fighter:
        return HttpResponse("Fighter not found.", status=404)
    
    ufc_name = f"{first_name.lower()}-{last_name.lower()}"
    ufc_url = f"https://www.ufc.com/athlete/{ufc_name}"

    fighter_stats = scrape_fighter_stats(ufc_url)
    fighter.update(fighter_stats)

    
    print(fighter)  

    return render(request, "stats/fighter_detail.html", {'fighter': fighter})

def display_events(request):
    events = all_events()
    return render(request, 'stats/all_events.html', {'events': events})

def home(request):
    upcoming_fights=scrape_upcoming_events()
    return render(request,"stats/home.html",{
        'upcoming_fights':upcoming_fights
    })
