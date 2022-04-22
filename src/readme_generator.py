import csv
import glob
import os
import re
from image_tags import ImageTags

from path import from_root
from fancy_print import FancyPrint, MessageType


#region Set up
# Paths
img_source_path = from_root('img_source')
img_tag_path = from_root('img_tag')
info_file_path = from_root('info.csv')
# Readme file
readme_text = []
def readme(line):
    readme_text.append(line)
def split_camel(text):
    return ' '.join(re.sub('([A-Z0-9][a-z]+)', r' \1', re.sub('([A-Z0-9]+)', r' \1', text)).split())
def readme_save():
    with open(from_root('README.md'), 'w') as readme_file:
        readme_file.write('\n'.join(readme_text))
# Printer
fp = FancyPrint()
#endregion


fp.put('Image tagger and README generator', MessageType.HEADER)


#region Read info file, generate readme
#region Note
readme('# Note')
readme('')
readme('The wast majority of these wallpapers are taken from random web-sites all over the internet and other repositories like this with wallpapers, I did not create them. ')
readme('The only modifications that I have done are cropping, color correction, noise reduction, upscaling, etc. ')
readme('')
readme('I tried finding the sources for every image in this wallpaper pack, but it is hard. If you are the original creator and you would like me to remove your wallpaper or I gave incorrect credit, please let me know by creating a new issue.')
readme('')
readme('')
readme('')
readme('')
readme('')
readme('# Wallpapers')
readme('')
#endregion

#region Wallpapers
wallpapers_found = []
wallpapers_missing = []

with open(info_file_path) as info_file:
    info = csv.DictReader(info_file)

    for img in info:
        # Print header
        name = img['name']
        fp.put(name, MessageType.SECTION)

        # Find the file
        file = glob.glob(from_root('img_source', f'{name}.*'))
        if len(file) != 1:
            # File not found
            wallpapers_missing.append(name)
            fp.put(f'{name} was not found, skipping', MessageType.ERROR, 1)
        else:
            # File was found
            fp.put(f'{name} was found', MessageType.SUCCESS, 1)
            file = file[0]
            wallpapers_found.append(os.path.basename(file))

            # Get info
            fp.put(f'Getting tags', MessageType.INFO, 2)
            tags  = ImageTags(file)
            file  = os.path.basename(file)
            name  = split_camel(img['name'])
            ratio = tags.ratio
            # color = tags.color
            style = img['style']
            note  = img['note']
            link  = img['link']
            # print(tags.get_color())

            # Write to readme
            fp.put(f'Writing to readme', MessageType.INFO, 2)
            readme(f'## {name}')
            readme('')
            readme('### Image')
            readme('')
            readme(f'![{name}](img_source/{file})')
            readme('')
            readme('')
            readme('### Details')
            readme('')
            readme(f'* **File name**: {file}')
            readme(f'* **Size**: {ratio}')
            readme(f'* **Style tag**: {style.capitalize()}')
            readme(f'* **Source**: [link]({link})')
            if note:
                readme(f'* **Notes**: {note}')
            readme('')
            readme('')
            readme('')
            readme('')

            # Tag and copy the file
            # TODO
            fp.put(f'Saving the tagged file as {"TODO"}', MessageType.INFO, 2)
#endregion
#endregion


#region Save readme
readme_text = readme_text[:-3]
readme_save()
#endregion

#region Find files that have no tags
wallpapers_unknown = set(wallpapers_found).symmetric_difference(set(os.listdir(img_source_path)))
#endregion

#region End report
fp.put('Report', MessageType.HEADER)
if len(wallpapers_missing):
    fp.put('Files in info file not found', MessageType.ERROR, 1)
    for missing in wallpapers_missing:
        fp.put(f'* {missing}', MessageType.NORMAL, 1)
if len(wallpapers_unknown):
    fp.put('Files not in the info file', MessageType.WARNING, 1)
    for unknown in wallpapers_unknown:
        fp.put(f'* {unknown}', MessageType.NORMAL, 1)
if not len(wallpapers_missing) and not len(wallpapers_unknown):
    fp.put('All good', MessageType.SUCCESS, 1)
#endregion
