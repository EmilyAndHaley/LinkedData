import sys
import xml.etree.ElementTree as ET

# This script takes a thesaurus of clinical signs (such as
# http://www.orphadata.org/data/xml/en_product5.xml) and dumps the symptom lists
# along with ID number to stdout, with blank lines between each report.  This
# format is expected by the Python xapian index building example, and can
# therefore be piped into that script to create an example index database.

# This function takes an XML element, finds any clinical signs in the file and
# prints them out (along with their IDs), and recurses along any children sign
# lists.  The "seen" set prevents duplicates from being printed out.
def dump_signs(elem, seen=set()):
    # Look through the children for "ClinicalSign" tags.
    for sign in filter(lambda  x: x.tag == "ClinicalSign", elem):
        sign_id = sign.attrib["id"]
        name = None
        children = None
        for c in sign:
            if c.tag == "Name":
                if name is not None:
                    print >>sys.stderr, "fatal error: duplicate Name tag in sign with id %s" % (sign_id)
                    sys.exit(1)
                name = c.text
            elif c.tag == "ClinicalSignChildList":
                if children is not None:
                    print >>sys.stderr, "fatal error: duplicate ClinicalSignChildList tag in sign with id %s" % (sign_id)
                    sys.exit(1)
                children = c

        if name is None:
            print >>sys.stderr, "warning: no Name tag in sign with id %s" % (sign_id)
        elif sign_id in seen:
            print >>sys.stderr, "warning: duplicate sign_id %s" % (sign_id)
        else:
            seen.add(sign_id)
            print name, sign_id
            print

        if children is not None:
            dump_signs(children, seen)


def main():
    if len(sys.argv) < 2:
        print >>sys.stderr, "usage: parse-symptoms.py <synonyms xml file>"
        sys.exit(1)

    synfile = sys.argv[1]

    # Parse the XML file.
    sys.stderr.write("Parsing xml...")
    sys.stderr.flush()
    tree = ET.parse(synfile)
    print >>sys.stderr, "done"

    # Extract the root element.
    root = tree.getroot()

    # Print out the clinical signs along with their ids, in the order they
    # appear in the file.
    dump_signs(root[0])

if __name__ == "__main__":
    main()
