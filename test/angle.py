import math


def is_range(yaw, angle, allow):
    diff = (yaw - angle) % (2.0 * math.pi)

    if diff >= math.pi:
        diff -= 2.0 * math.pi

    if abs(diff) <= allow:
        return True

    return False


MAX_ANGLE = 10

allow = math.radians(MAX_ANGLE)

for a in range(-180, 180):
    print("")
    for b in range(-180, 180):
        yaw = math.radians(a)
        angle = math.radians(b)
        if is_range(yaw, angle, allow):
            print("{}\t{}\t{}\t{}".format(yaw, angle, a, b))
