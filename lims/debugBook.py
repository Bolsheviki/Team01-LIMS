import urllib2
from xml.dom import minidom

apikey = '002bdcc12fb16e8a008396438f144b9e'
isbnURL = 'http://api.douban.com/book/subject/isbn/'


def get_attrvalue(node, attrname):
    return node.getAttribute(attrname) if node else ''

def get_nodevalue(node, index = 0):
    return node.childNodes[index].nodeValue if node else ''

def get_xmlnode(node,name):
    return node.getElementsByTagName(name) if node else []

def xml_to_string(filename='user.xml'):
    doc = minidom.parse(filename)
    return doc.toxml('UTF-8')


def infoBook(isbn):
    res = urllib2.urlopen(isbnURL + isbn + '?apikey=' + apikey)
    xmldoc = minidom.parse(res)
    entry = xmldoc.documentElement
    
    book = {}
    
    nodes_summary = get_xmlnode(entry, 'summary')
    if nodes_summary:
        book['summary'] = get_nodevalue(nodes_summary[0])

    nodes_link = get_xmlnode(entry, 'link')
    for node in nodes_link:
        if get_attrvalue(node, 'rel') == 'image':
            book['image'] = get_attrvalue(node, 'href')
            break

    nodes_attribute = get_xmlnode(entry, 'db:attribute')
    for node in nodes_attribute:
        book[get_attrvalue(node, 'name')] = get_nodevalue(node)
    return book
    


print infoBook('9787111298854')['title']
print infoBook('9787111298854')['author']
print infoBook('9787111298854')['translator']
print infoBook('9787111298854')['summary']

