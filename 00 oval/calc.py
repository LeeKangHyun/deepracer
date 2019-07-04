import math

MIN_SIGHT = 1
MAX_SIGHT = 2

MIN_ANGLE = 3.0


def get_angel(coor1, coor2):
    return math.atan2((coor2[1] - coor1[1]), (coor2[0] - coor1[0]))


def get_diff_angle(coor1, coor2, coor3):
    angle1 = get_angel(coor1, coor2)
    angle2 = get_angel(coor1, coor3)

    diff = (angle2 - angle1) % (2.0 * math.pi)

    if diff >= math.pi:
        diff -= 2.0 * math.pi

    return math.degrees(diff)


def calc():
    waypoints = get_waypoints()

    count = len(waypoints)

    f = open("calc.csv", 'w')
    f.write(',x,y,angle\n')

    for i in range(count):
        next0 = waypoints[(i + 1) % count]
        next1 = waypoints[(i + 1 + MIN_SIGHT) % count]
        next2 = waypoints[(i + 1 + MAX_SIGHT) % count]

        # diff angle
        diff_angle = get_diff_angle(next0, next1, next2)

        f.write('{},{},{},{}\n'.format(i, next0[0], next0[1], diff_angle))

    f.close()


def get_waypoints():
    waypoints = []

    waypoints.append([2.97313, 0.95872])
    waypoints.append([3.16866, 0.95797])
    waypoints.append([3.36416, 0.95750])
    waypoints.append([3.55965, 0.95717])
    waypoints.append([3.75514, 0.95691])
    waypoints.append([3.95063, 0.95670])
    waypoints.append([4.14611, 0.95653])
    waypoints.append([4.34159, 0.95640])
    waypoints.append([4.53707, 0.95630])
    waypoints.append([4.73256, 0.95623])
    waypoints.append([4.92804, 0.95620])
    waypoints.append([5.12352, 0.95618])
    waypoints.append([5.31900, 0.95621])
    waypoints.append([5.51449, 0.95625])
    waypoints.append([5.70997, 0.95633])
    waypoints.append([5.90546, 0.95646])
    waypoints.append([6.10096, 0.95664])
    waypoints.append([6.29647, 0.95685])
    waypoints.append([6.49200, 0.95698])
    waypoints.append([6.68758, 0.95673])
    waypoints.append([6.88326, 0.95578])
    waypoints.append([7.07913, 0.95387])
    waypoints.append([7.27522, 0.95432])
    waypoints.append([7.47050, 0.96804])
    waypoints.append([7.66216, 1.00507])
    waypoints.append([7.84524, 1.07150])
    waypoints.append([8.01445, 1.16843])
    waypoints.append([8.16542, 1.29246])
    waypoints.append([8.29412, 1.43980])
    waypoints.append([8.39758, 1.60561])
    waypoints.append([8.46935, 1.78603])
    waypoints.append([8.51177, 1.97638])
    waypoints.append([8.53075, 2.17097])
    waypoints.append([8.53596, 2.36720])
    waypoints.append([8.53876, 2.56341])
    waypoints.append([8.53781, 2.75964])
    waypoints.append([8.53257, 2.95569])
    waypoints.append([8.51481, 3.15056])
    waypoints.append([8.47549, 3.34141])
    waypoints.append([8.40798, 3.52476])
    waypoints.append([8.31106, 3.69388])
    waypoints.append([8.18650, 3.84417])
    waypoints.append([8.03713, 3.96950])
    waypoints.append([7.86814, 4.06660])
    waypoints.append([7.68516, 4.13450])
    waypoints.append([7.49413, 4.17570])
    waypoints.append([7.29955, 4.19534])
    waypoints.append([7.10359, 4.20124])
    waypoints.append([6.90761, 4.20125])
    waypoints.append([6.71178, 4.19992])
    waypoints.append([6.51615, 4.19930])
    waypoints.append([6.32059, 4.19912])
    waypoints.append([6.12506, 4.19922])
    waypoints.append([5.92955, 4.19939])
    waypoints.append([5.73406, 4.19956])
    waypoints.append([5.53857, 4.19968])
    waypoints.append([5.34308, 4.19976])
    waypoints.append([5.14760, 4.19980])
    waypoints.append([4.95211, 4.19982])
    waypoints.append([4.75663, 4.19980])
    waypoints.append([4.56115, 4.19976])
    waypoints.append([4.36566, 4.19969])
    waypoints.append([4.17018, 4.19958])
    waypoints.append([3.97470, 4.19944])
    waypoints.append([3.77922, 4.19926])
    waypoints.append([3.58374, 4.19901])
    waypoints.append([3.38811, 4.19860])
    waypoints.append([3.38811, 4.19860])
    waypoints.append([3.19270, 4.19824])
    waypoints.append([2.99726, 4.19774])
    waypoints.append([2.80179, 4.19713])
    waypoints.append([2.60630, 4.19569])
    waypoints.append([2.41080, 4.19096])
    waypoints.append([2.21508, 4.18356])
    waypoints.append([2.01905, 4.16967])
    waypoints.append([1.82555, 4.13816])
    waypoints.append([1.63991, 4.07782])
    waypoints.append([1.46842, 3.98581])
    waypoints.append([1.31656, 3.86357])
    waypoints.append([1.18829, 3.71644])
    waypoints.append([1.08718, 3.54951])
    waypoints.append([1.01596, 3.36846])
    waypoints.append([0.97341, 3.17815])
    waypoints.append([0.95349, 2.98341])
    waypoints.append([0.94442, 2.78720])
    waypoints.append([0.94051, 2.59073])
    waypoints.append([0.93970, 2.39423])
    waypoints.append([0.94714, 2.19805])
    waypoints.append([0.96674, 2.00333])
    waypoints.append([1.00864, 1.81291])
    waypoints.append([1.07774, 1.63100])
    waypoints.append([1.17467, 1.46086])
    waypoints.append([1.29935, 1.31053])
    waypoints.append([1.44854, 1.18512])
    waypoints.append([1.61828, 1.08988])
    waypoints.append([1.80268, 1.02696])
    waypoints.append([1.99501, 0.99237])
    waypoints.append([2.19022, 0.97529])
    waypoints.append([2.38601, 0.96666])
    waypoints.append([2.58180, 0.96216])
    waypoints.append([2.77752, 0.95991])
    waypoints.append([2.97313, 0.95872])

    return waypoints


if __name__ == '__main__':
    calc()
