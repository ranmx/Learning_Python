class HTML(object):

    def __init__(self):
        self.body = ''

    class Table(object):
        def __init__(self, attrs=None):
            self.table = ''
            self.attr_len = 0
            if attrs is not None:
                self.table_create(attrs)

        def __str__(self):
            return self.table + '</table>'

        def table_create(self, attrs):
            self.table = '<table style="width:100%">'
            self.attr_len = len(attrs)
            self._table_add_item(attrs, head=True)

        def table_add(self, attrs):
            self._table_add_item(attrs)

        def _table_add_item(self, attrs, head=False):
            if len(attrs) == self.attr_len:
                pass
            else:
                raise TypeError('Attribution of the table is not correct')

            if isinstance(attrs, list):
                self.table += '<tr>'
                for item in attrs:
                    if head:
                        self.table += '<th>{0}</th>'.format(str(item))
                    else:
                        self.table += '<td>{0}</td>'.format(str(item))
                self.table += '</tr>'
            elif isinstance(attrs, str):
                self.table += '<tr>'
                if head:
                    self.table += '<th>{0}</th>'.format(str(attrs))
                else:
                    self.table += '<td>{0}</td>'.format(str(attrs))
                self.table += '</tr>'
            else:
                raise TypeError('Attribution of the table is not correct')

    def __repr__(self):
        return '<html>' + '<head>' + self.style() + '</head>' + \
            '<body>' + self.body + '</body>' + '<html>'

    @staticmethod
    def title(text):
        return '<h1>{0}</h1>'.format(str(text))

    @staticmethod
    def _table_type(tp=None):
        if tp is not None:
            table_type = tp
        else:
            table_type = 'table, th, td {border: 1px solid black;}'
        return table_type

    def add(self, text):
        self.body += '<p>{0}</p>'.format(str(text))

    def style(self, tp='', table_type=None):
        return '<style>' + tp + self._table_type(table_type) + '</style>'


html = HTML()
title1 = html.title('This is a test table')
html.add(title1)
html.add('Do not tell anybody!')
table = html.Table(['name', 'age', 'gender'])
table.table_add(['Alfred', '27', 'M'])
html.add(table)

print str(html)
