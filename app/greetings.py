import webapp2

main_html = """
    <html>
        <head>
            <title> Greetings Page </title>
        </head>
        <body>
            <p> Hello Google App Engine World </p>
        </body>
    </html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(main_html)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
