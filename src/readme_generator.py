import os
from path import from_root


#region Generate readme
readme_text = []
img_dir = from_root('img')
def readme(line):
    readme_text.append(line)
for file in os.listdir(img_dir):
    img_file = from_root('img', file)
    # Header with the name of the file
    readme('<details>')
    readme(f'   <summary>{file}</summary>')
    readme('')
    readme(f'   ![{file}](img/{file})')
    readme('</details>')
    readme('')
    readme('')
#endregion


#region Save to file
with open(from_root('README.md'), 'w') as readme_file:
    readme_file.write('\n'.join(readme_text))
#endregion
