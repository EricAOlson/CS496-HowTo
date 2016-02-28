#Code leveraged from Google App Engine Tutorial, and lectures, and updated to meet requirements.
import webapp2

app = webapp2.WSGIApplication([
    ('/', 'pages.Home'),
    ('/index.html', 'pages.Home'),
    ('/pre-req.html', 'pages.Pre_Req'),
    ('/key.html', 'pages.Key'),
    ('/engine.html', 'pages.Engine'),
    ('/api.html', 'pages.API'),
    ('/exp.html', 'pages.Exp'),
    ('/more.html', 'pages.More'),
], debug=True)