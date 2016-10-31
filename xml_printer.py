import xml.etree.ElementTree as ET
from collections import OrderedDict


class XMLPaser(object):
    def __init__(self, path):
        self.path = path
        self.tree = ET.parse(self.path)
        self.root = self.tree.getroot()
        self.result_list = []

    def _deep_first_travel(self, node, result_dict, child_limit):
        if node.text and len(node.text.strip()) > 0:
            return node.text
        else:
            result_dict[node.tag] = OrderedDict()
            for child in node:
                if child_limit and child.tag not in child_limit:
                        continue
                result_dict[node.tag][child.tag] = self._deep_first_travel(child, result_dict[node.tag], child_limit)

    def fetchall(self, display_limit=None, search_limit=None, *args, **kwargs):
        for selected_content in self.fetchone(display_limit, search_limit, *args, **kwargs):
            self._select_result_list(selected_content)
        if not self.result_list or len(self.result_list) == 0:
            print "no result"
        print_files = self._fetch()
        if print_files:
            return print_files

    def fetchone(self, display_limit=None, search_limit=None, *args, **kwargs):
        for result_dict in self._get_xml_result_dict(search_limit):
            selected_content = self._select_content(result_dict, display_limit, *args, **kwargs)
            yield selected_content

    def _get_xml_result_dict(self, search_limit):
        for node in self.root:
            result_dict = OrderedDict()
            self._deep_first_travel(node, result_dict, search_limit)
            yield result_dict

    def _fetch(self):
        return self.result_list

    def _select_result_list(self, selected_content):
        self.result_list.append(selected_content)

    def _select_content(self, result_dict, display_limit, *args, **kwargs):
        return result_dict

    def _select_display(self, result_dict, child_limit, n):
        if n < len(child_limit) - 1:
            temp_dict = result_dict[child_limit[n]]
            return self._select_display(temp_dict, child_limit, n+1)
        else:
            content = result_dict[child_limit[n]]
            return content


class MetadataParser(XMLPaser):
    def __init__(self, path):
        super(MetadataParser, self).__init__(path)

    def _fetch(self):
        if isinstance(self.result_list[0], str):
            return sorted(set(self.result_list))

    def _select_content(self, result_dict, display_limit, *args, **kwargs):
        result_dict = self._select_display(result_dict, display_limit, 0)
        return result_dict


class MLSXMLPaser(XMLPaser):
    def __init__(self, path):
        super(MLSXMLPaser, self).__init__(path)
        self.name = self.path.split('/')[-1].split('.')[0].title()
        self.result_list = set()

    def _select_result_list(self, result_dict):
        self.result_list = self.result_list.union(set(result_dict[self.name].keys()))

    def _fetch(self):
        return sorted(set(self.result_list))


class MLSPaser(XMLPaser):
    def __init__(self, path):
        super(MLSPaser, self).__init__(path)
        self.name = self.path.split('/')[-1].split('.')[0].title()

    def _select_result_list(self, result_dict):
        self.result_list.append(result_dict[self.name])

    def _fetch(self):
        return self.result_list


class TestXMLParser(object):
    @staticmethod
    def compare_metadata():
        metadata_parser = MetadataParser('/home/alfred/Downloads/451_Metadata.xml')
        metadata_field = metadata_parser.fetchall(search_limit=['root', 'Field', 'SystemName'],
                                                  display_limit=['Field', 'SystemName'])

        listing_parser = MLSXMLPaser('/home/alfred/Downloads/501/njgsmls/residential.xml')
        listing_field = listing_parser.fetchall()

        metadata_field_big = set(map(lambda x: x.upper(), metadata_field))
        print "metadata_big:"
        print metadata_field_big
        listing_field_big = set(map(lambda x: x.upper().replace('_', ''), listing_field))
        print 'listing_field_big'
        print listing_field_big
        print 'intersection'
        intersection = list(metadata_field_big.intersection(listing_field_big))
        print intersection

    @staticmethod
    def yield_lines():
        listing_parser = XMLPaser('/home/alfred/Downloads/501/njgsmls/business.xml')
        for line in listing_parser.fetchone():
            yield line

