from jinja2 import Markup


class momentjs(object):

    def __init__(self,timestamp):
        self.timestamp = timestamp

    def render(self, form):
        return Markup("<script>\ndocument.write(moment(\'%s\').%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), form))

    def format(self,style):
        return self.render("format(\'%s\')" % (style))

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")


    
