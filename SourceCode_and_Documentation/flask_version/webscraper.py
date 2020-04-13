from bs4 import BeautifulSoup
import requests
import base64
import json

class Web_scraper():
  def __init__(self, landmark):
    self.landmark = landmark
   
class Events_scraper(Web_scraper):
  def __init__(self, landmark):
    super().__init__(landmark)
    self.url = "https://www.eventbrite.com.au/d/" + landmark + "/" + landmark

  def get_events(self):
    result = []
    page = requests.get(self.url).text
    soup = BeautifulSoup(page, 'lxml')
    for article in soup.find_all('article', class_="eds-l-pad-all-4 eds-media-card-content eds-media-card-content--list eds-media-card-content--mini eds-media-card-content--square eds-l-pad-vert-3"):
      event_image_src = article.aside.a['href']
      content = article.find('div', class_="eds-media-card-content__content__principal")
      try:
        event_date = content.div.div.text
      except:
        event_date = "NA"
      try:
        event_title = content.div.a.h3.div.div.text
      except:
        event_title = "NA"
      try:
        event_url = content.div.a['href']
      except:
        event_url = "NA"
      content = article.find('div', class_="card-text--truncated__one")
      try:
        event_address = content.text
      except:
        event_address = "NA"
      result_dict = {
        'title' :  event_title,
        'date' : event_date,
        'addr' : event_address,
        'url' : event_url
      }
      result.append(result_dict)
    return result

class Info_scraper(Web_scraper):
  def __init__(self, landmark):
    query= landmark.split()
    query='+'.join(query)
    super().__init__(landmark)
    self.url_img = "https://www.bing.com/images/search?q="+query+"&FORM=HDRSC2"
    self.url_desc = f"https://google.com/search?q={query}"

  def get_image(self):

    page = requests.get(self.url_img,headers={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}).text
    soup = BeautifulSoup(page, 'lxml')
    base_url = soup.find('a', "iusc").div.img['src']
    print(base_url)
    return base_url


  def get_description(self):
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent" : USER_AGENT}
    page = requests.get(self.url_desc, headers=headers).text
    desc = ""
    try:
      soup = BeautifulSoup(page, 'lxml')
      desc = soup.find('div', class_="kno-rdesc").div.span.text
    except:
      desc = "No Info about this landmark"
    return desc


if __name__ == "__main__":
  scraper = Info_scraper("Sydney")
  print(scraper.get_description())
  print(scraper.get_image())
  
