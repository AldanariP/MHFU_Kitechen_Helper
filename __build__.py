import shutil

import PyInstaller.__main__

if __name__ == '__main__':
    output_path = "dist"

    PyInstaller.__main__.run([
        'app.py',
        '--name=MHFUKitchenHelper',
        '--onefile',
        f'--distpath=./{output_path}',
        '--windowed',
        '--clean',
    ])

    shutil.copytree("lang", f"{output_path}/lang", dirs_exist_ok=True)
