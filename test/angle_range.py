import math


def is_range(yaw, angle, allow):
    diff = (yaw - angle) % (2.0 * math.pi)

    if diff >= math.pi:
        diff -= 2.0 * math.pi

    diff = abs(diff)

    if diff <= allow:
        return True, diff

    return False, diff


MAX_ANGLE = 10

allow = math.radians(MAX_ANGLE)

for a in range(-180, 180):
    print("")
    for b in range(-180, 180):
        yaw = math.radians(a)
        angle = math.radians(b)
        in_range, diff = is_range(yaw, angle, allow)

        if in_range:
            print("{}\t{}\t{}\t{}\t{}".format(yaw, angle, a, b, diff))
