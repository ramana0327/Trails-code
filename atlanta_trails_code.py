# make sure to install these packages before running:
# pip install requests
# pip install bs4
# pip install json

import requests  #requests module is used to fetch the HTML code from a webpage
from bs4 import BeautifulSoup  #beautiful soup is a module used to parse HTML code using its various functions
import json  #json is a module used to convert the python dictionary into a JSON string that can be written into a file



trail_data = []

#Here is creating a function for all the trails data in the city or state

#the variable url inthe url_from_trail(plc_name) function gives the links of all the trails.
#that links are used in this function
def get_data_from_url(url):
    page = requests.get(url)
    #The HTML of the website formed by the url is retrieved by the get function and stored in page
    
    #Then we use the python library BeautifulSoup to parse the HTML code, by creating a soup of the contents of the retrieved HTML codes of the webpage
    soup = BeautifulSoup(page.text, 'html.parser')
    #print (soup)
    
    
    #print (soup.find_all('div', {'class': 'small-12 medium-4 columns facts'})) #Used to retrieve all the HTML lines of code having the <div> class=small-12 medium-4 columns facts tag and it is assinged to the variable ddd
    ddd = soup.find_all('div', {'class': 'small-12 medium-4 columns facts'})
    
    #these codes are used to retrieve the trail facts such as counties,states,length,trail_end_points,trail_surfaces,trail_category and trail_activities
    ex = {str(i.text.replace(":","").strip()): str(j.text.strip()) for i,j in zip(ddd[0].find_all('strong'),ddd[0].find_all('span'))}
  
    ex2 = {str(i.text.replace(":","").strip()): str(j.text.strip()) for i,j in zip(ddd[1].find_all('strong'),ddd[1].find_all('span'))}
    
    ex3 = {str(ddd[1].find_all('strong')[-1].text).replace(":","").strip() : [str(i.text) for i in ddd[1].find_all('a')]}
  
    return ex, ex2 ,ex3


#In the website all the links are same ,but the city or state name is change at the end of the link
#Here is creating a function that replaces the link by required data of city or state name

def url_from_trail(plc_name):
    
    #https://www.traillink.com/trailsearch/?mmloc="+plc_name -Is the webpage i'm parsing in this script
     
    
    url = "https://www.traillink.com/trailsearch/?mmloc="+plc_name
    
    page = requests.get(url)
    #The HTML of the website formed by the url is retrieved by the get function and stored in page
    
    #Then we use the python library BeautifulSoup to parse the HTML code, by creating a soup of the contents of the retrieved HTML codes of the webpage
    soup = BeautifulSoup(page.text, 'html.parser')
    
    #print (soup)
    
    #print (soup.find('div', {'class': 'trails'})) #Used to retrieve all the HTML lines of code having the <div> class = trails tag and it is assinged to the variable soup_div_trails
    
    soup_div_trails = soup.find('div', {'class': 'trails'})
  
    #print (soup_div_trails.find_all("a")) #Used to retrieve all the HTML lines of code having the <a> tag in the variable soup_div_trails and it assigned to the variable url
    
    #It gives the all the trail links and the link concatinate with the base url - https://www.traillink.com
    url = ["https://www.traillink.com"+str(i['href']) for i in soup_div_trails.find_all('a', href=True)]
    
    #print soup_div_trails.find_all('div', {'class': 'row collapse trail'}) #Used to retrieve all the HTML lines of code having the <div> class=row collapse trail tag in the variable soup_div_trails and it assigned to the variable desc
    
    #It gives title ,lat and lng
    desc = [json.loads(i.get("data-map-marker")) for i in soup_div_trails.find_all('div', {'class': 'row collapse trail'})]
    
    #NOTE: Here I have used a for loop because to itetate the data of variables url and desc
    
    for u,d in zip(url,desc):
        new = dict()   #Create a empty dictionary name as new for storing the data in required formate
        new['title'] = d['title']
        new['lat'] = d['lat']
        new['lng'] = d['lng']
        ex,ex2,ex3 = get_data_from_url(u)
        new['counties'] = ex['Counties']
        new['states'] = ex['States']
        new['length'] = ex['Length']
        new['trail_end_points'] = ex['Trail end points']
        new['trail_surfaces'] = ex2['Trail surfaces']
        new['trail_category'] = ex2['Trail category']
        new['trail_activities'] = ex3['Trail activities']
        
        trail_data.append(new)  #Append the new dictionary to a empty list trail_data
    

url_from_trail('atlanta')   #Tthis is how to call function by giving the name of required city or state trail data


#An empty file created for the purpose of storing data; data.txt stores information about our source website. The title, URL, the description, date of creation and the no of videos on the page is stored.
#file created for the purpose of storing data; atlanta_trail_data.json stores trails data of atlanta

file = open("atlanta_trail_data.json","w")

json.dump(trail_data,file)  #dumps the trails_data ny using json.dumps function
file.close()  #closes the file
