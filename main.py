#!/usr/bin/env python
import os
import jinja2
import webapp2

import random

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class OsnovaHandler(BaseHandler):
    def get(self):
        return self.render_template("base.html")

class RezultatHandler(BaseHandler):
    def post(self):
        besedilo = self.request.get("sporocilo")
        ime = self.request.get("ime")
        stevilka = self.request.get("stevilka")

        izzrebane = []
        for j in range (7):
            izzrebane.append(random.randint(1, 37))

        params = {"name": ime, "besedilo": besedilo, "izzrebane": izzrebane}

        return self.render_template("rezultat.html", params=params)


       #  odgovor = "Pozdravljeni " + ime + "vase sporocilo je: " + besedilo * int(stevilka)

      #  self.write(odgovor)

class AboutHandler(BaseHandler):
    def get(self):
        return self.render_template("about.html")

class ContactHandler(BaseHandler):
    def get(self):
        return self.render_template("contact.html")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/mywebsite.html', OsnovaHandler),
    webapp2.Route('/about', AboutHandler),
    webapp2.Route('/contact', ContactHandler)
], debug=True)
