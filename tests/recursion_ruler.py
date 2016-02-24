class GridPrinter(object):
    def __init__(self, length, label=None):
        self.length = length
        self.label = label
        self.line = self._create_line()
        self.grid = self._create_label()
        self._print_grid()

    def _create_line(self):
        try:
            line = "-" * self.length
            return line
        except (TypeError,ValueError):
            print "'length' must be an integal number"

    def _create_label(self):
        if self.label:
            try:
                grid = self.line + self.label
            except TypeError:
                print "'label' type error"
                raise
        else:
            grid = self.line
        return grid

    def _print_grid(self):
        print self.grid


class Length(object):
    def __init__(self, max_length):
        self._print_length(max_length)

    def _print_length(self, length):
        if length > 1:
            Length(length-1)
            GridPrinter(length)
            Length(length-1)
        elif length == 1:
            GridPrinter(length)


class Ruler(object):
    def __init__(self):
        self.str_length = raw_input('type in the maximum length')
        self.int_length = int(self.str_length)
        self.str_label = raw_input('type in the maximum label')
        self.int_label = int(self.str_label)
        self._print_ruler()

    def _print_ruler(self):
        for label in range(self.int_label):
            GridPrinter(self.int_length, str(label))
            Length(self.int_length-1)

        GridPrinter(self.int_length, self.str_label)

Ruler()










