import tornado.ioloop
import tornado.web
import tornado.httpserver
import os

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        print "Arguments %s" % self.request.arguments
        if self.request.arguments:
            print "got some arguments"
        print "Headers %s" % self.request.headers
        print "path %s" % self.request.path
        
        
    def get_current_user(self):
        print "user: %s" % self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self):
        print "main page"
        items = ["Item 1", "next!", "And the last"]
        self.render("template.html", title="jaysPage", items=items)

class NextPageHandler(BaseHandler):
    def get(self):
        print "next page 1"
        self.write("word nextpage")
        if not self.get_argument("text", None):
            self.html_stuff("no argument passed")
        else:
            self.html_stuff(self.get_argument("text"))
        
    #def get(self, stuff):
    #    print "next page"
    #    self.write("you made it!")
    #    self.htmlStuff(stuff)

    def html_stuff(self, stuff):
        self.write("<br><head>WEIRD %s</head><br><br>More stuff</head>" % stuff)

class StoryHandler(BaseHandler):
    def get(self, story_id):
        print "story page"
        self.write("You requested the story " + story_id)

class HuhHandler(BaseHandler):
    def get(self, stuff):
        print "in HUH! %s" % stuff
        self.redirect('/nextpage', permanent=True)
        #self.write("HUH!")

class PostHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/post/" method="post">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        #self.set_header("Content-Type", "text/plain")
        self.write("""
                    <html>
                        <body>
                            <form action="/post/" method="post">
                               <input type="text" name="message">
                               <input type="submit" value="Submit">
                           </form>
                           You Wrote %s
                        </body>
                    </html>""" % self.get_argument("message"))
                   #"You wrote " + self.get_argument("message"))
        
class RedirectHandler(BaseHandler):
    def get(self):
        self.redirect("/")
                   
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/story/([0-9]+)", StoryHandler),
    (r"/huh/(.*)", HuhHandler),
    (r"/nextpage", NextPageHandler),
    (r"/post/", PostHandler),
    (r"/redirect", RedirectHandler),
    (r"/static/test.tar", tornado.web.RedirectHandler,
     dict(url="http://github.com/downloads/facebook/tornado/tornado-0.2.tar.gz")),
    ])

if __name__ == "__main__":
    #application.listen(5000)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(os.environ.get("PORT", 5000))
    tornado.ioloop.IOLoop.instance().start()
