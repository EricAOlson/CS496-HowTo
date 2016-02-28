#Code leveraged from Google App Engine Tutorial, and lectures, and updated to meet requirements.
import webapp2
import jinja2
import os
import urllib, urllib2
import json
from google.appengine.api import urlfetch
import cgi

#Setup of Jinja environment, and location of templates folder.
JINJA_ENV = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True
)

class Home(webapp2.RequestHandler):
  def get(self):
    page = JINJA_ENV.get_template('index.html')
    self.response.write(page.render())

class Pre_Req(webapp2.RequestHandler):
  def get(self):
    page = JINJA_ENV.get_template('pre-req.html')
    self.response.write(page.render())

class Key(webapp2.RequestHandler):
  def get(self):
    page = JINJA_ENV.get_template('key.html')
    self.response.write(page.render())

class Engine(webapp2.RequestHandler):
  def get(self):
    page = JINJA_ENV.get_template('engine.html')
    self.response.write(page.render())

class API(webapp2.RequestHandler):
  def get(self):
    page = JINJA_ENV.get_template('api.html')
    self.response.write(page.render())

class Exp(webapp2.RequestHandler):
  def get(self):
    page = JINJA_ENV.get_template('exp.html')
    self.response.write(page.render())

  def post(self):
    #Get data from passed From data:
    search_text = urllib.quote_plus(self.request.get('search_text'))
    limit_time = self.request.get('time')
    num_resp = self.request.get('limit')
    #Set num_resp to 5 if not passed.
    if num_resp == "":
      num_resp = 5

    #Display generated request URL to How-To user:
    request_url = "https://www.googleapis.com/customsearch/v1?cx=<EngineID>&key=<APIKey>&q=" + search_text
    if limit_time != "n":
      request_url = request_url + "&dateRestrict=" + limit_time + "5"
    template_vars = {}
    template_vars['url'] = request_url
    general_results = []

    #Process Request for general search:
    #API Key = AIzaSyAaqv3P9TVkvN1FzGw0nWThCOqzWvB1cdk
    #Engine ID = 003235365699361770251:codtcbpklya
    url_index = 0
    general_results = []
    while(int(url_index) < int(num_resp)):  #num_resp previously set to desired # of responses.
      request_url = "https://www.googleapis.com/customsearch/v1?cx=003235365699361770251:codtcbpklya&key=AIzaSyAaqv3P9TVkvN1FzGw0nWThCOqzWvB1cdk&q=" + search_text
      if limit_time != "n":
        request_url = request_url + "&dateRestrict=" + limit_time + "5"
      #If this is not the first API call we need to add start parameter.
      if url_index != 0:
        request_url = request_url + "&start=" + str(url_index + 1)
      response = urlfetch.fetch(request_url)
      if response.status_code == 200:
        findings = json.loads(response.content)
        #ensure we found enough pages to fullfill request
        if long(findings['searchInformation']['totalResults']) < int(num_resp):
          num_resp = findings['searchInformation']['totalResults']
        #identify how many results we can pull from this API response.
        to_pull = min(int(num_resp) - int(url_index), 10) 
        #cycle through results, adding responses to 'general_results'
        for x in range (0, to_pull):
          result_page = {}
          result_page['title'] = findings['items'][x]['title']
          result_page['link'] = findings['items'][x]['link']
          result_page['snippet'] =findings['items'][x]['snippet']
          general_results.append(result_page)
          url_index = int(url_index) + 1 #used to track how many URLs we have already pulled.
      else:
        template_vars['gen_error'] = "True"
    #once all results have been identified, add to template_vars
    template_vars['general_results'] = [{'title':x['title'], 'link':x['link'], 'snippet':x['snippet']} for x in general_results]

    #Process Request for .edu search:
    #API Key = AIzaSyAaqv3P9TVkvN1FzGw0nWThCOqzWvB1cdk
    #Engine ID = 003235365699361770251:omqzs7ytd0u
    url_index = 0
    general_results = []
    while(int(url_index) < int(num_resp)):  #num_resp previously set to desired # of responses.
      request_url = "https://www.googleapis.com/customsearch/v1?cx=003235365699361770251:omqzs7ytd0u&key=AIzaSyAaqv3P9TVkvN1FzGw0nWThCOqzWvB1cdk&q=" + search_text
      if limit_time != "n":
        request_url = request_url + "&dateRestrict=" + limit_time + "5"
      #If this is not the first API call we need to add start parameter.
      if url_index != 0:
        request_url = request_url + "&start=" + str(url_index + 1)
      response = urlfetch.fetch(request_url)
      if response.status_code == 200:
        findings = json.loads(response.content)
        #ensure we found enough pages to fullfill request
        if long(findings['searchInformation']['totalResults']) < int(num_resp):
          num_resp = findings['searchInformation']['totalResults']
        #identify how many results we can pull from this API response.
        to_pull = min(int(num_resp) - int(url_index), 10) 
        #cycle through results, adding responses to 'general_results'
        for x in range (0, to_pull):
          result_page = {}
          result_page['title'] = findings['items'][x]['title']
          result_page['link'] = findings['items'][x]['link']
          #result_page['snippet'] = cgi.escape(findings['items'][x]['snippet']).encode('ascii', 'xmlcharrefreplace')
          result_page['snippet'] =findings['items'][x]['snippet']
          general_results.append(result_page)
          url_index = int(url_index) + 1 #used to track how many URLs we have already pulled.
      else:
        template_vars['edu_error'] = "True"
    #once all results have been identified, add to template_vars
    template_vars['edu_results'] = [{'title':x['title'], 'link':x['link'], 'snippet':x['snippet']} for x in general_results] 
    

    #Process Request for oregonstate.edu search:
    #API Key = AIzaSyAaqv3P9TVkvN1FzGw0nWThCOqzWvB1cdk
    #Engine ID = 003235365699361770251:khsgvzzoekq
    url_index = 0
    general_results = []
    while(int(url_index) < int(num_resp)):  #num_resp previously set to desired # of responses.
      request_url = "https://www.googleapis.com/customsearch/v1?cx=003235365699361770251:khsgvzzoekq&key=AIzaSyAaqv3P9TVkvN1FzGw0nWThCOqzWvB1cdk&q=" + search_text
      if limit_time != "n":
        request_url = request_url + "&dateRestrict=" + limit_time + "5"
      #If this is not the first API call we need to add start parameter.
      if url_index != 0:
        request_url = request_url + "&start=" + str(url_index + 1)
      response = urlfetch.fetch(request_url)
      if response.status_code == 200:
        findings = json.loads(response.content)
        #ensure we found enough pages to fullfill request
        if long(findings['searchInformation']['totalResults']) < int(num_resp):
          num_resp = findings['searchInformation']['totalResults']
        #identify how many results we can pull from this API response.
        to_pull = min(int(num_resp) - int(url_index), 10) 
        #cycle through results, adding responses to 'general_results'
        for x in range (0, to_pull):
          result_page = {}
          result_page['title'] = findings['items'][x]['title']
          result_page['link'] = findings['items'][x]['link']
          #result_page['snippet'] = cgi.escape(findings['items'][x]['snippet']).encode('ascii', 'xmlcharrefreplace')
          result_page['snippet'] =findings['items'][x]['snippet']
          general_results.append(result_page)
          url_index = int(url_index) + 1 #used to track how many URLs we have already pulled.
      else:
        template_vars['osu_error'] = "True"
    template_vars['osu_results'] = [{'title':x['title'], 'link':x['link'], 'snippet':x['snippet']} for x in general_results]
    
    page = JINJA_ENV.get_template('exp.html')
    self.response.write(page.render(template_vars))


class More(webapp2.RequestHandler):
  def get(self):
    page = JINJA_ENV.get_template('more.html')
    self.response.write(page.render())