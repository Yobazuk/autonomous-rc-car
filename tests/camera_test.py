from components.camera import Camera


def main():
    cam = Camera()

    while True:
        cam.get_frame(preview=True)


if __name__ == '__main__':
    main()
