import os
import platform

import PyInstaller.__main__

if __name__ == '__main__':
    args = [
        'app.py',
        '--name=MHFUKitchenHelper',
        '--onefile',
        '--clean',
        '--optimize=2',
    ]

    for lang_file in os.scandir(os.path.join(os.getcwd(), 'lang')):
        args.append(f'--add-data={lang_file.path}:lang')

    if platform.system() != 'Windows':
        args.append('--strip')

    PyInstaller.__main__.run(args)
