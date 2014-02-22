import xml.etree.ElementTree as ET

#Import the XML file
tree = ET.parse('en_product6.xml')
#get the root element
root = tree.getroot()

#get the root tag
rootTag = root.tag

#get the attributes of an element
rootAtt = root.attrib
#get the child tags and attributes of the root
#for child in root:
#    print(child.tag, child.attrib)

#recursively iterate through all childs of the root with the tag 'Name' and print their values
#for name in root.iter('Name'):
#    print(name.text)

#get all the names of the genes
for disorderlist in root.findall('DisorderList'):
    for disorder in disorderlist.findall('Disorder'):
        for disordergeneassociationlist in disorder.findall('DisorderGeneAssociationList'):
            for disordergeneassociation in disordergeneassociationlist.findall('DisorderGeneAssociation'):
                for gene in disordergeneassociation.findall('Gene'):
                    name = gene.find('Name').text
                    print(name)
