import os
from googletrans import Translator
from bs4 import BeautifulSoup, Comment
import warnings

# ignoring useless bs4 warnings  
warnings.filterwarnings(action='ignore', module='bs4')

# building Translator() object
translator = Translator()

# getting current dir path
current_dir = os.getcwd()

# empty list to which htmlfiles' names will be appended 
htmls = []

# getting all the htmls which are in the folder and all subfolders of the website
for root, dirs, files in os.walk(current_dir):
    for file in files:
        if file.endswith('.html'):
            file_name = os.path.join(root, file)
            htmls.append(file_name)

# print number of html files found
print(f"There are {len(htmls)} HTML files.")

count = 0
# creating the soup and parsing it to translate all text
for html in htmls:
    htmlopen = open(html, 'r', encoding='utf-8')
    htmlcontents = htmlopen.read()
    soup = BeautifulSoup(htmlcontents, 'lxml')
    
    # translate search area placeholders
    for input in soup.find_all('input'):
        if 'placeholder' in input.attrs:
            input['placeholder'] = translator.translate(input['placeholder'], dest='hi').text
    
    # translate all other text except style, script, tags, and comments
    for element in soup.find_all():
        if (element.name not in ['style', 'script']):
            for content in element.contents:
                if (content not in soup.find_all()) and (content not in [" ", None, "\n"]) and (content not in soup.find_all(string=lambda text: isinstance(text, Comment))):
                    try:
                        t = translator.translate(content, dest='hi').text
                        content.replace_with(t)
                    except:
                        # to know if there are some sentences that are not translated
                        print(f"\"{content.strip()}\" in \n\"{html}\" \n\t---> Translation Issue!")                
    
    count += 1
    print(count)

    # writing translated content to each html
    with open(html, 'w', encoding='utf-8') as final:
        final.write(str(soup))
