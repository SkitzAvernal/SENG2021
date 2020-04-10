from bs4 import BeautifulSoup
import requests

class Web_scraper():
  def __init__(self, landmark):
    self.landmark = landmark
    self.url = "https://www.eventbrite.com.au/d/" + landmark + "/" + landmark
    print(self.url)

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
      print(result_dict)
      result.append(result_dict)
    return result