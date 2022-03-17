# -*- coding: utf-8 -*-
"""Web Scrapping.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YZE80-JQVbHvaGLC5GGbNePCrk8tHCX7
"""

from bs4 import BeautifulSoup
import requests
import csv

def sum1(l):
    from itertools import accumulate
    return list(accumulate(l))

#create the heading row
heading=[0]*51
heading[0]="Player Name"
heading[1]="Nationality"
for i in range(49):
    heading[i+2]=1971+i
    
#open csv files
# csv_file=open('C://Users//TUF GAMING//Desktop//Scrapping.csv','w')
csv_file = open('/content/test.csv', 'w') 
csv_writer=csv.writer(csv_file)
csv_writer.writerow(heading)
source=requests.get('http://www.espncricinfo.com/ci/content/player/index.html').text
result=BeautifulSoup(source,'lxml')
# print(result.prettify())
country_list=[None]*8
content=result.find('ul',class_="navbar-nav w-100 justify-content-between")
r=0
count=0
#print(content.prettify())
for link in content.find_all('li'):
    if link.a['href']=='/player':
        continue
    if count==8:
        break
    link=link.a['href']
    if not link=='/':
        country_list[count]=link
        count+=1
country_list=set(country_list)
country_list=list(country_list)    
#print(country_list)
for link in country_list:
    country_id=link.split('/')[3]
    source=requests.get('https://www.espncricinfo.com/player/team/{}'.format(country_id) ).text
    result=BeautifulSoup(source,'lxml')
    if result.head.title.text.split()[2] == 'cricket':
      country_name=result.head.title.text.split()[1]
    else:
      country_name=result.head.title.text.split()[1]+" "+result.head.title.text.split()[2]

    
    A_to_Z=[None]*26
    count=0
    index=result.find('div',class_="d-flex pr-2 pt-2 pb-2 overflow-auto justify-content-between hide-scrollbar pl-4")
    for link1 in index.find_all('a'):
         if link1['data-hover']=="Active Players":
           continue
         link1=link1.get('href')
         if not link1=='/':
            A_to_Z[count]=link1
            count+=1
    A_to_Z=set(A_to_Z)
    A_to_Z=list(A_to_Z)
    for link2 in A_to_Z:
      if link2==None:
        continue
      alpha_id=link2.split('/')[4]
      source_player=requests.get('https://www.espncricinfo.com/player/team/{}/{}'.format(country_id,alpha_id)).text
      result_player=BeautifulSoup(source_player,'lxml')
      player_index_grid=result_player.find('div',class_="player-index-grid w-100")
      player_index_list=player_index_grid.find_all('div',class_="pl-3")
      for player_link in player_index_list:
        player_link=player_link.find('a')['href']

        code=player_link.split('/')[2].split('-')[-1]
        if len(player_link.split('/')[2].split('-')) == 3:
          player_name=player_link.split('/')[2].split('-')[0] + " " + player_link.split('/')[2].split('-')[1]
        if len(player_link.split('/')[2].split('-')) == 2:
          player_name=player_link.split('/')[2].split('-')[0]
        if len(player_link.split('/')[2].split('-')) == 4:
          player_name=player_link.split('/')[2].split('-')[0] + " " + player_link.split('/')[2].split('-')[1]+player_link.split('/')[2].split('-')[2]
       # player_name=player_link.split('/')[2].split('-')[0] + " " + player_link.split('/')[2].split('-')[1]
        details_page_source=requests.get('https://stats.espncricinfo.com/ci/engine/player/{}.html?class=2;template=results;type=batting'.format(code)).text
        details_page=BeautifulSoup(details_page_source,'lxml')
        if len(details_page.find_all('tbody')) < 5:
          continue
        player_score = details_page.find_all('tbody')[5].find_all('tr', class_="data1")
        player_score.pop(0)
        a = [0] * 51
        a[0] = player_name
        a[1] = country_name
        # print(player_grid)
        for year in player_score:
         res=year.find_all('td')
         try:
            
              curr_yr=int(res[0].b.string.split(" ")[1])
              if res[5].string=='-':
                 runs_in_yr=0
              else:
                 runs_in_yr=int(res[5].string)
                 a[curr_yr - 1971 + 2 ]=runs_in_yr
         except Exception as e:
                pass 
        a=sum1(a[2:])        
        a.insert(0,player_name)
        a.insert(1,country_name)
        print('{} : {} {}'.format(r,a[0],a[1]))
        r+=1
        csv_writer.writerow(a)
    csv_writer.writerow([None] * 51)

csv_file.close()  
      
          
          
          # res=year.find_all('td')
          # curr_yr=res[0].b.string.split(" ")[1]
          # curr_sc=res[5].string
