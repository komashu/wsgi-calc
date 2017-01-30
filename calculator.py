import re
import pprint
from wsgiref.simple_server import make_server


def resolve_path(path):
    urls = [(r'^$', index),
            (r'^multiply/(\d+)/(\d+)$', multi),
            (r'^add/(\d+)/(\d+)$', add),
            (r'^divide/(\d+)/(\d+)$', divide),
            (r'^subtract/(\d+)/(\d+)$', subtraction),
           # (r'^calc', calc) #?(x=\d)&(y=\d)&(math=\w*)
            ]
    matchpath = path.lstrip('/')
    for regexp, func in urls:
        match = re.match(regexp, matchpath)
        if match is None:
            continue
        args = match.groups([])
        return func, args
    raise NameError

def index():
    page = """
     <html>
    <head>
    <title>Math Calculator</title>
{style}
    </head>
    <body>
   <h1>Let's do some math!</h1>
   <h2>Because I could not get my spiffy form to work, you will just have to add the numbers into the URL like a heathen.</h2>
   You can only add, subtract, multiply and divide. Just add one of those words into the URL with each number separated
   with a '/'.<br><br>

   For instance if you wanted to add 5 to 5, your URL would look like <a href="add/5/5">http://localhost:8080/add/5/5</a><br>
   So...
   Addition: your URL would look like <a href="add/5/5">http://localhost:8080/add/5/5</a><br>
   Subtraction: your URL would look like <a href="subtract/10/5">http://localhost:8080/subtract/10/5</a><br>
   Multiplication: your URL would look like <a href="multiply/5/5">http://localhost:8080/multiply/5/5</a><br>
   Division: your URL would look like <a href="divide/25/5">http://localhost:8080/divide/25/5</a><br>

    """.format(style=style())
    return page

# To troubleshoot later why this doesn't work with calc()
#def index():
#    page = """
#    <html>
#    <head>
#    <title>Math Calculator</title>
#    </head>
#    <body>
#    <h1>Let's do some math!</h1>
#   <form action='/calc' method='get'>
#  First number: <input type='text' name='x'>
#  Second number: <input type='text' name='y'><br>
#  <input type="submit" value="Add" name='math'><input type="submit" value="Multiply" name='math'><input type="submit" \
#  value="Divide" name='math'><input type='submit' value='Subtract' name='math'>
#  </form>
#  </body>
#  </html>
#    """
#    return page

#def calc(environ):
#    values = environ.get('QUERY_STRING', None).split('&')
#    print(values)
#    math = values[2].strip('math=')
#    print(math)
#    x = values[0].strip('x=')
#    print(x)
#    y = values[1].strip('y=')
#    print(y)
#    if math == 'Add':
#        return add(x,y)
#    elif math == 'Multiply':
#        return multi(x,y)
#    elif math == 'Divide':
#        return divide(x,y)
#    elif math == 'Subtract':
#        return subtraction(x,y)
#    else:
#        return index()

def style():
    style = """
        <style type="text/css">
    body,td,th {
	font-family: "American Typewriter", "American Typewriter Condensed", "American Typewriter Condensed Light", "American Typewriter Light";
	color: #000;
    }
    body {
	    background-color: #FFF;
    }
    a:link {
	    color: #F09;
    }
    a:visited {
	    color: #F6C;
    }
    a:hover {
	    color: #FCF;
    }
    a:active {
	    color: #F69;
    }
    </style>
    """
    return style


def multi(x,y):
    page = """
    <html>
    <head>
    <title>Math Calculator</title>
    {style}
    </head>
    <body>
     <h1>The answer to {x} x {y} is:</h1>
     <h2>{z}</h2>
     <a href='/'>Back to the index page</a>
     </body>
  </html>
    """.format(style=style(),x=x, y=y, z=float(x)*float(y))
    return page


def divide(x,y):
    page = """
        <html>
        <head>
        <title>Math Calculator</title>
        {style}
        </head>
        <body>
         <h1>The answer to {x} / {y} is:</h1>
         <h2>{z}</h2>
         <a href='/'>Back to the index page</a>
         </body>
      </html>
        """.format(style=style(), x=x, y=y, z=float(x)/float(y))
    return page


def add(x,y):
    page = """
        <html>
        <head>
        <title>Math Calculator</title>
        {style}
        </head>
        <body>
         <h1>The answer to {x} + {y} is:</h1>
         <h2>{z}</h2>
         <a href='/'>Back to the index page</a>
         </body>
      </html>
        """.format(style=style(), x=x, y=y, z=float(x)+float(y))
    return page

def subtraction(x,y):
    page = """
        <html>
        <head>
        <title>Math Calculator</title>
        {style}
        </head>
        <body>
         <h1>The answer to {x} + {y} is:</h1>
         <h2>{z}</h2>
         <a href='/'>Back to the index page</a>
         </body>
      </html>
        """.format(style=style(), x=x, y=y, z=float(x)-float(y))
    return page


def application(environ, start_response):
    pprint.pprint(environ)
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "Only Chuck Norris can divide by zero"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
