import math

def calc():
    fov_x = 42.2
    fov_y = 62.1
    width = 1280
    height = 720

    focal_len_x = (width * 0.5) / math.tan(fov_x * 0.5 * math.pi/180)
    focal_len_y = (height * 0.5) / math.tan(fov_y * 0.5 * math.pi/180)

    print("fx:{}, fy:{}".format(focal_len_x, focal_len_y))

if __name__ == "__main__":
    calc()