# c 2024-04-01
# m 2024-04-01

import os

from PIL import Image


def main() -> None:
    for root, dirs, files in os.walk('images'):
        # print(root, dirs, files)

        for file in files:
            if file == 'desktop.ini':
                continue

            path: str = os.path.abspath(os.path.join(root, file))

            with Image.open(path) as image:
                if image.size == (3840, 2160):
                    new = image.resize((1280, 720))
                    new.save(os.path.abspath(os.path.join(root, file)))
                    print(f'resized {path}')


if __name__ == '__main__':
    main()
