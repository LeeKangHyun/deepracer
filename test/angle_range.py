import math

MAX_ANGLE = 5

allow = math.radians(MAX_ANGLE)


def diff_angle(yaw, guide):
    diff = (yaw - guide) % (2.0 * math.pi)

    if diff >= math.pi:
        diff -= 2.0 * math.pi

    return abs(diff)


for a in range(-180, 180, 2):
    print("")
    for b in range(-180, 180):
        yaw = math.radians(a)
        guide = math.radians(b)

        diff = diff_angle(yaw, guide)

        if diff < allow:
            print("{}\t{}\t{}\t{}\t{}\t{}".format(yaw, allow, guide, a, b, diff))
