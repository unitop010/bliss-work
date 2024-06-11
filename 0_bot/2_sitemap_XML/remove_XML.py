import xml.etree.ElementTree as ET

# List of keywords to filter out (assuming these are part of URL and would help identify elements to remove)
keywords = {'jpg', 'setCurrencyId', 'cart.php', 'sort', 'productimage.php'}

# Load and parse the XML file into an element tree
tree = ET.parse('merged_sitemap.xml')
root = tree.getroot()

# Define the namespace map for the XML document
ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

# Iterate over <url> elements and remove those with certain keywords
index = 0
while index < len(root):
    elem = root[index]
    loc_elem = elem.find("sm:loc", ns)
    if any(keyword in loc_elem.text for keyword in keywords):
        # Remove the element with matching condition
        root.remove(elem)
    else:
        # Only move to the next element if we did not remove one,
        # because removal shifts subsequent elements to the left.
        index += 1

# Save the modified XML to a new file
tree.write("filtered_sitemap.xml", encoding='utf-8', xml_declaration=True)
