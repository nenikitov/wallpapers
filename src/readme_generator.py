import csv
import glob
import os
import re

from path import from_root

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
    return ' '.join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', text)).split())
def readme_save():
    with open(from_root('README.md'), 'w') as readme_file:
        readme_file.write('\n'.join(readme_text))
#endregion


#region Read info file, generate readme
#region Note
readme('# Note')
readme('')
readme('The wast majority of these wallpapers are taken from random web-sites all over the internet and other repositories like this with wallpapers, I did not create them. ')
readme('The only modifications that I have done are cropping / color correction, etc. ')
readme('')
readme('I tried finding the sources for every image in this wallpaper pack, but it is hard. If you are the original creator and you would like me to remove your wallpaper or I gave incorrect credit, please let me know by creating a new issue.')
readme('')
readme('')
readme('')
readme('')
readme('# Wallpapers')
readme('')
#endregion

#region Wallpapers
with open(info_file_path) as info_file:
    info = csv.DictReader(info_file)

    for img in info:
        file = glob.glob(from_root('img_source', f'{img["name"]}.*'))
        if len(file) != 1:
            print(f'!!! Image with {img["name"]} was not found')
        else:
            # Get info
            file  = os.path.basename(file[0])
            name  = split_camel(img['name'])
            size  = img['size']
            style = img['style']
            note  = img['note']
            link  = img['link']

            # Write to readme
            readme(f'## {name}')
            readme('')
            readme(f'### Image')
            readme(f'![{name}](img_source/{file})')
            readme('')
            readme('')
            readme('### Details')
            readme('')
            readme(f'* **File name**: {file}')
            readme(f'* **Size**: {size.capitalize()}')
            readme(f'* **Style tag**: {style.capitalize()}')
            readme(f'* **Source**: [link]({file})')
            if note:
                readme(f'* **Notes**: {note}')
            readme('')
            readme('')
            readme('')

            # Tag and copy the file
            # TODO
#endregion
#endregion


#region Save readme
readme_save()
#endregion
