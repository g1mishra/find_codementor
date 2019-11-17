from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from .models import Search
import datetime 
Base_Mentor_Url="https://www.codementor.io/experts?q={}"
Base_Post_Url = "https://www.codementor.io{}"

def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    final_postings = []
    if not search:
        error="Error!"
    else:
        error=""
        current_time = datetime.datetime.now() 
        obj=Search(search=search,created=current_time)
        obj.save()
        final_url = Base_Mentor_Url.format(quote_plus(search))
        response = requests.get(final_url)
        data = response.text
        soup=BeautifulSoup(data,"html.parser")

        post_list = soup.find_all('div', {'class': 'resultBlock'})
        for i in post_list:
            post_listings=i.find_all('div', {'class': 'row-fluid mentor-item-row'})
        
        for post in post_listings:
            x=post.find(class_="span9 mentor-details")
            post_title=x.find(class_='name').text
            post_title=post_title.strip()

            post_url=Base_Post_Url.format(x.find(class_='name').get('href'))
            
            y=post.find(class_="span3 text-center mentor-info")

            if y.find(class_="rate").text :
                post_price=y.find(class_="rate").text
                post_price = post_price.strip()
            if not post_price:
                post_price="N/A"
            
            if y.find(class_="img-circle headImg").get('src'):
                post_img_src=y.find(class_="img-circle headImg").get('src')
            else :
                post_img_src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSqI-ITDXkGbI5GGDeLUJKKgvv_wEehtglCuJUyuWtqqvDeLCnz3Q&s"
            tup=(post_title, post_url, post_price, post_img_src)
            final_postings.append(tup)
            if final_postings[0][0] == "{{item['display_name']}}":
                error="Error!"
                break
    search_for_frontend={
        'search':search,
        'final_postings': final_postings[:-1],
        'error':error,
    }
    return render(request,'my_app/new_search.html',search_for_frontend)