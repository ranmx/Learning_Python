import xml.etree.ElementTree as ET
from collections import OrderedDict


class XMLPaser(object):
    def __init__(self, path):
        self.path = path
        self.tree = ET.parse(self.path)
        self.name = self.path.split('/')[-1].split('.')[0].title()
        self.root = self.tree.getroot()
        self.result_list = []

    def _deep_first_travel(self, node, result_dict, child_limit):
        if node.text and len(node.text.strip()) > 0:
            return node.text
        else:
            result_dict[node.tag] = OrderedDict()
            for child in node:
                if child_limit:
                    if child.tag in child_limit:
                        result_dict[node.tag][child.tag] = \
                            self._deep_first_travel(child, result_dict[node.tag], child_limit)
                else:
                    result_dict[node.tag][child.tag] = \
                        self._deep_first_travel(child, result_dict[node.tag], child_limit)

    def display(self, display_limit=None, search_limit=None):
        for node in self.root:
            result_dict = OrderedDict()
            self._deep_first_travel(node, result_dict, display_limit)
            n = 1
            if search_limit:
                if search_limit != 'diy':
                    self._select_display(result_dict, search_limit, n)
                else:
                    self._select_handler()
            else:
                self.result_list.append(result_dict[self.name])
        if not self.result_list or len(self.result_list) == 0:
            print "no result"
        if isinstance(self.result_list[0], str):
            for element in sorted(set(self.result_list)):
                print element
        else:
            for element in self.result_list:
                print element

    def _select_display(self, result_dict, child_limit, n):
        if n < len(child_limit)-1:
            temp_dict = result_dict[child_limit[n]]
            self._select_display(temp_dict, child_limit, n+1)
        else:
            self.result_list.append(result_dict[child_limit[n]])

    def _select_handler(self):
        pass


# xmlparser = XMLPaser('/home/alfred/Downloads/451_Metadata.xml')
# xmlparser.display(['root', 'Field', 'SystemName'], ['root', 'Field', 'SystemName'])

# xmlparser = XMLPaser('/home/alfred/Downloads/501/njgsmls/residential.xml')
# xmlparser.display()

