import os
from xml.etree import ElementTree as ET

# Define the namespace and register it to avoid ns0 prefix
namespace = 'http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('', namespace)

# Define the directory where your XML files are stored
directory_path = 'full scan'

# Create an XML element which will act as the root of your combined XML
root = ET.Element('urlset', xmlns=namespace)

# Define the keywords that should trigger removal
keywords = ['jpg', 'setCurrencyId', 'cart.php', 'sort', 'productimage.php']

# Loop through each file in the directory
for filename in os.listdir(directory_path):
    if not filename.endswith('.xml'):
        continue  # Skip non-XML files
    
    # Construct the full file path
    file_path = os.path.join(directory_path, filename)
    
    # Parse the XML file
    tree = ET.parse(file_path)
    
    # Get the root element (in this case 'urlset')
    file_root = tree.getroot()
    
    # Find all 'url' elements and add them to the root element
    for url in file_root.findall('{%s}url' % namespace):
        root.append(url)

# Use XPath to select all <url> elements
for url_element in root.xpath('//xmlns:url', namespaces={'xmlns': "http://www.sitemaps.org/schemas/sitemap/0.9"}):
    loc_element = url_element.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
    # Check if any keyword is present in the <loc> text
    if any(keyword in loc_element.text for keyword in keywords):
        # Remove the <url> element from the root
        root.remove(url_element)

# Once all files have been processed, write the result to a new XML file
tree = ET.ElementTree(root)
with open('merged_sitemap.xml', 'wb') as merged_file:
    tree.write(merged_file, encoding='utf-8', xml_declaration=True)

print(f"Updated XML has been saved to merged_sitemap.xml.")
