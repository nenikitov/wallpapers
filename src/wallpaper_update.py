import csv
import glob
import os
import shutil
import sys

from fancy_print import FancyPrint, MessageType
from image_tags import ImageTags
from path import ProjectPath as ProjectPath


#region Parse arguments
argv = sys.argv[1::]
if (len(argv) > 1):
    print('Usage: "python wallpaper_update" or "python wallpaper_update MODE"')
    print('Try "python wallpaper_update --help" for more information.')
    sys.exit(2)

mode = ''
save_readme = True
save_tag    = True
if (len(argv) == 0):
    mode = '-b'
else:
    mode = argv[0]

if mode == '-h' or mode == '--help':
    print('Usage: python wallpaper_update MODE')
    print('Regenerate README from csv file / tag and save images.')
    print('')
    print('Modes:')
    print('  -h, --help')
    print('     Display this help message and exit')
    print('  -b, --both')
    print('     Regenerate README and tag and save images (Default mode)')
    print('  -r, --readme')
    print('     Regenerate README only')
    print('  -t, --tag')
    print('     Tag and save images only')
    sys.exit()
elif mode == '-r' or mode == '--readme':
    save_readme = True
    save_tag    = False
elif mode == '-t' or mode == '--tag':
    save_readme = False
    save_tag    = True
elif mode == '-b' or mode == '--both':
    save_readme = True
    save_tag    = True
else:
    print('Usage: "python wallpaper_update" or "python wallpaper_update MODE"')
    print('Try "python wallpaper_update --help" for more information.')
    sys.exit(2)
#endregion

#region Set up
# Paths
img_source_name  = 'img_source'
img_tag_name     = 'img_tag'
img_source_path  = ProjectPath(img_source_name)
img_tag_path     = ProjectPath(img_tag_name)
info_file_path   = ProjectPath('info.csv')
readme_file_path = ProjectPath('README.md')
# Readme file
readme_text = []
def readme(line):
    readme_text.append(line)
def readme_save():
    with open(readme_file_path, 'w') as readme_file:
        readme_file.write('\n'.join(readme_text))
# Printer
fp = FancyPrint()
#endregion


fp.put('Image tagger and README generator', MessageType.HEADER)


#region Read info file, generate readme
#region Note
if save_readme:
    readme('# Note')
    readme('')
    readme('The wast majority of these wallpapers are taken from random web-sites all over the internet and other repositories with wallpapers, I did not create them.')
    readme('The only modifications that I have done are cropping, color correction, noise reduction, upscaling, etc.')
    readme('')
    readme('I tried finding the sources for every image in this wallpaper pack, but it is hard.')
    readme('If you are the original creator and you would like me to remove your wallpaper from the repository or I gave incorrect credit, please let me know by creating a new issue.')
    readme('')
    readme('')
    readme('')
    readme('')
    readme('')
    readme('# Usage')
    readme('')
    readme('Run the python script `wallpaper_update.py` to regenerate the `README.md` file and tag all the images.')
    readme('* Use `-r` option if you only want to regenerate the `README.md`')
    readme('* Use `-t` option if you only want to tag and save images')
    readme('* Use `-h` option if you are not sure how to use it')
    readme('')
    readme('')
    readme('')
    readme('')
    readme('')
    readme('# Wallpapers')
    readme('')
#endregion


#region Clean tagged directory
if save_tag:
    shutil.rmtree(img_tag_path, ignore_errors=True)
    os.mkdir(img_tag_path)
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
        file = glob.glob(img_source_path + f'{name}.*')
        if len(file) != 1:
            # File not found
            wallpapers_missing.append(name)
            fp.put(f'{name} was not found or matched multiple files, skipping', MessageType.ERROR, 1)
        else:
            # File was found
            fp.put(f'{name} was found', MessageType.SUCCESS, 1)
            file = file[0]
            file_name = os.path.basename(file)
            wallpapers_found.append(file_name)

            # Get info
            fp.put('Getting tags', MessageType.INFO, 2)
            tags = ImageTags(file, img)
            extension = os.path.splitext(file_name)[1]
            tag_name = f'{tags.file_name}_{tags.combined}{extension}'

            # Write to readme
            if save_readme:
                fp.put('Writing to readme', MessageType.INFO, 2)
                readme(f'## {tags.name}')
                readme('')
                readme('### Image')
                readme('')
                readme(f'![{tags.name}]({img_source_name}/{file_name})')
                readme('')
                readme('')
                readme('### Details')
                readme('')
                readme(f'* **File name**: `{file_name}`')
                readme(f'* **Tagged name**: `{tag_name}`')
                readme(f'* **Size**: {tags.ratio}')
                readme(f'* **Style**: {tags.style}')
                readme(f'* **Source**: [link]({tags.link})')
                if len(tags.note) != 0:
                    readme(f'* **Notes**: {tags.note}')
                readme('')
                readme('')
                readme('')
                readme('')

            # TODO Tag and copy the file
            if save_tag:
                fp.put(f'Saving the tagged file as {tag_name}', MessageType.INFO, 2)
                shutil.copy2(file, img_tag_path + tag_name)
#endregion
#endregion


#region Save readme
if save_readme:
    readme_text = readme_text[:-3]
    readme_save()
#endregion

#region Find files that have no tags
img_sources = os.listdir((img_source_path))
wallpapers_unknown = set(wallpapers_found) ^ set(img_sources)
#endregion

#region End report
fp.put('Report', MessageType.HEADER)
if len(wallpapers_missing) != 0:
    fp.put('Files in info file not found', MessageType.ERROR, 1)
    for missing in wallpapers_missing:
        fp.put(f'* {missing}', MessageType.NORMAL, 1)
if len(wallpapers_unknown) != 0:
    fp.put('Files not in the info file', MessageType.WARNING, 1)
    for unknown in wallpapers_unknown:
        fp.put(f'* {unknown}', MessageType.NORMAL, 1)
if len(wallpapers_missing) == 0 and len(wallpapers_unknown) == 0:
    fp.put('All good', MessageType.SUCCESS, 1)
#endregion
