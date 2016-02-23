import os
import xml.etree.ElementTree as ET
import xml.dom.minidom

class Node(object):
    def __init__(self, name):
        self._name = name
        self._parent = None
        self._children = []

    def getName(self):
        return self._name

    def getParent(self):
        return self._parent

    def addChild(self, node):
        self._children.append(node)

    def numChildren(self):
        return len(self._children)

    def getChildAt(self, index):
        return self._children[index]

    def setParent(self, node):
        self._parent = node
        self._parent.addChild(self)

def create_default_scenegraph():

    dirName = os.path.dirname(os.path.realpath(__file__))
    xmlPath = os.path.join(dirName, r'scenegraph.xml')

    if not os.path.isfile(xmlPath):
        print('The xml file does not exist: {}'.format(xmlPath))
        return

    tree = ET.parse(xmlPath)
    root = tree.getroot()

    for childNode in root:
        create_scenegraph_recurse(childNode)

def create_scenegraph_recurse(xmlNode, parent_list=None):

    if parent_list is None:
        parent_list = []

    name = xmlNode.get('name')
    parent_list.append(name)
    full_path = ' | '.join(parent_list)
    print full_path

    xmlChildren = xmlNode.getchildren()

    if xmlChildren:

        for xmlChild in xmlChildren:

            create_scenegraph_recurse(xmlChild, parent_list)

    parent_list.pop()


def create_dummy_node_recurse(xmlNode, parent=None):

    name = xmlNode.get('name')
    node = Node(name)

    if parent:
        node.setParent(parent)

    xmlChildren = xmlNode.getchildren()

    if xmlChildren:

        for xmlChild in xmlChildren:

            create_dummy_node_recurse(xmlChild, node)


def create_dummy_scenegraph():

    dirName = os.path.dirname(os.path.realpath(__file__))
    xmlPath = os.path.join(dirName, r'scenegraph.xml')

    if not os.path.isfile(xmlPath):
        print('The xml file does not exist: {}'.format(xmlPath))
        return

    tree = ET.parse(xmlPath)
    root = tree.getroot()

    root_node = Node('Root')

    for childNode in root:
        create_dummy_node_recurse(childNode, root_node)

    return root_node


def inspect_dummy_scenegraph(node, depth=0):
    
    print '{} {}'.format('- '*depth, node.getName())
    depth = depth + 1

    num_children = node.numChildren()
    for index in range(num_children):

        child = node.getChildAt(index)
        inspect_dummy_scenegraph(child, depth)

    depth = depth -1


def main():
    
    create_default_scenegraph()
    root_node = create_dummy_scenegraph()
    #print root_node
    inspect_dummy_scenegraph(root_node)


if __name__ == '__main__':
    main()







