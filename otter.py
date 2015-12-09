class Otter():
    def __init__(self, filename, title):
        self.reportfile= open(filename,"w")
        self.title = title
        self.write_preamble()
        
    def _write(self, text):
        self.reportfile.write(text)
        
    def write_preamble(self):
        html_str = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
        <meta name="description" content="">
        <meta name="author" content="">
        <link rel="icon" href="../../favicon.ico">
        """
        self._write(html_str)

        html_str="""
        <title>{}</title>

        <!-- Bootstrap core CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn3uZzapT0u7EYsXMjQV+0En5r" crossorigin="anonymous">
        
        </head>
        <body>
        <div class="container">
        """.format(self.title)
        self._write(html_str)

    def write_footer(self):
        html_str="""
        </div> <!-- close the whole container -->
        </body>
        </html>
        
        """
        self._write(html_str)
        self.reportfile.close()


    def write_page_header(self):
        
        html_str = """
        <div class="row">

        <div class="page-header">
           <h1>{} <small>Subtext for header</small></h1>
        </div>
        """.format(self.title)
        self._write(html_str)

    def write_row(self, text):
        html_str= """
        <div class="row">
          {}
        </div>
        """.format(text)
        self._write(html_str)


# <table class="table">
#      <tr>
#        <th>Number</th>
#        <th>Square</th>
#      </tr>
#      <indent>

#        <tr>
#          <td><%= i %></td>
#          <td><%= i**2 %></td>
#        </tr>
#      </indent>
# </table>
# </div>
# </div>
# """
# html_file.write(html_str)

# html_str = """
#   </body>
# </html>
# """


report = Otter('newtest.html', "Test Report")
report.write_page_header()
report.write_row("Hello world.")
report.write_footer()