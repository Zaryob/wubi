'''
DESCRIPTION:
Simple metalink parser

USAGE:
metalink = Metalink(filename)
'''

import xml.etree.ElementTree as ElementTree
prefix = '{http://www.metalinker.org/}'

def get_text(element, tag, default=None):
    subelement = element.find(prefix + tag)
    if subelement is not None:
        return subelement.text
    return default

def get_subitems(element, tag, subtag):
    subelement = element.find(prefix + tag)
    if subelement is not None:
        return subelement.findall(prefix + subtag)
    else:
        return []


class Metalink(object):

    def __init__(self, metalink_file):
        tree = ElementTree.parse(metalink_file)
        root = tree.getroot()
        self.metalink_file = metalink_file
        self.version = get_text(root, 'version')
        self.description = get_text(root, 'description')
        self.files = {}
        for file in get_subitems(root, 'files', 'file'):
            file_name = file.get('name')
            self.files[file_name] = MetalinkFile(file)

    def __str__(self):
        return "Metalink(%s)" % self.metalink_file


class MetalinkFile(object):
    def __init__(self, file):
        self.name = file.get('name')
        self.size = long(get_text(file, 'size', 0))
        self.os = get_text(file, 'os')
        self.verification = {}
        for hash in get_subitems(file, 'verification', 'hash'):
            hash_type = hash.get('type')
            self.verification[hash_type] = hash.text
        self.resources = []
        for url in get_subitems(file, 'resources', 'url'):
            self.resources.append(MetalinkURL(url))

    def __str__(self):
        return "MetalinkFile(%s)" % self.name


class MetalinkURL(object):

    def __init__(self, url):
        self.type = url.get('type')
        self.location = url.get('location')
        self.preference = url.get('preference')
        self.url = url.text

    def __str__(self):
        return "MetalinkUrl(%s)" % self.url


m = Metalink('/tmp/kubuntu-8.04.1-desktop-i386.metalink')
