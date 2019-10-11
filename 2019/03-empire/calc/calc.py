import math

MIN_SIGHT = 2
MAX_SIGHT = 4

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

    fn = "calc-{}-{}.csv".format(MIN_SIGHT, MAX_SIGHT)

    f = open(fn, "w")
    f.write(",x,y,angle\n")

    count = len(waypoints)

    for i in range(count):
        next0 = waypoints[(i + 1) % count]
        next1 = waypoints[(i + 1 + MIN_SIGHT) % count]
        next2 = waypoints[(i + 1 + MAX_SIGHT) % count]

        # diff angle
        diff_angle = get_diff_angle(next0, next1, next2)

        f.write("{},{},{},{}\n".format(i, next0[0], next0[1], diff_angle))

    f.close()


def get_waypoints():
    waypoints = []

    waypoints.append([4.29757, 0.53973])
    waypoints.append([4.42614, 0.53247])
    waypoints.append([4.55440, 0.52152])
    waypoints.append([4.68255, 0.50931])
    waypoints.append([4.81076, 0.49753])
    waypoints.append([4.93902, 0.48632])
    waypoints.append([5.06732, 0.47571])
    waypoints.append([5.19568, 0.46577])
    waypoints.append([5.32410, 0.45666])
    waypoints.append([5.45258, 0.44845])
    waypoints.append([5.58111, 0.44097])
    waypoints.append([5.70968, 0.43433])
    waypoints.append([5.83831, 0.42892])
    waypoints.append([5.96700, 0.42527])
    waypoints.append([6.09574, 0.42402])
    waypoints.append([6.22446, 0.42610])
    waypoints.append([6.35299, 0.43310])
    waypoints.append([6.48093, 0.44746])
    waypoints.append([6.60721, 0.47210])
    waypoints.append([6.73026, 0.50985])
    waypoints.append([6.84771, 0.56229])
    waypoints.append([6.95729, 0.62972])
    waypoints.append([7.05709, 0.71091])
    waypoints.append([7.14522, 0.80459])
    waypoints.append([7.21964, 0.90958])
    waypoints.append([7.27739, 1.02443])
    waypoints.append([7.31626, 1.14706])
    waypoints.append([7.33643, 1.27409])
    waypoints.append([7.33996, 1.40272])
    waypoints.append([7.33038, 1.53106])
    waypoints.append([7.31111, 1.65834])
    waypoints.append([7.28630, 1.78468])
    waypoints.append([7.26243, 1.91117])
    waypoints.append([7.24352, 2.03850])
    waypoints.append([7.22990, 2.16652])
    waypoints.append([7.22151, 2.29499])
    waypoints.append([7.21789, 2.42367])
    waypoints.append([7.21700, 2.55241])
    waypoints.append([7.21725, 2.68114])
    waypoints.append([7.21859, 2.80990])
    waypoints.append([7.22332, 2.93855])
    waypoints.append([7.23470, 3.06674])
    waypoints.append([7.25224, 3.19430])
    waypoints.append([7.27431, 3.32113])
    waypoints.append([7.29969, 3.44734])
    waypoints.append([7.32449, 3.57365])
    waypoints.append([7.34222, 3.70119])
    waypoints.append([7.34671, 3.82968])
    waypoints.append([7.33317, 3.95766])
    waypoints.append([7.30027, 4.08198])
    waypoints.append([7.24865, 4.19979])
    waypoints.append([7.18078, 4.30905])
    waypoints.append([7.09890, 4.40830])
    waypoints.append([7.00491, 4.49618])
    waypoints.append([6.90023, 4.57090])
    waypoints.append([6.78647, 4.63101])
    waypoints.append([6.66588, 4.67586])
    waypoints.append([6.54074, 4.70590])
    waypoints.append([6.41317, 4.72247])
    waypoints.append([6.28454, 4.72782])
    waypoints.append([6.15587, 4.72355])
    waypoints.append([6.02801, 4.70921])
    waypoints.append([5.90147, 4.68558])
    waypoints.append([5.77643, 4.65489])
    waypoints.append([5.65291, 4.61862])
    waypoints.append([5.53080, 4.57797])
    waypoints.append([5.40964, 4.53432])
    waypoints.append([5.28814, 4.49173])
    waypoints.append([5.16417, 4.45730])
    waypoints.append([5.03747, 4.43480])
    waypoints.append([4.90908, 4.42564])
    waypoints.append([4.78046, 4.43003])
    waypoints.append([4.65305, 4.44776])
    waypoints.append([4.52803, 4.47835])
    waypoints.append([4.40652, 4.52091])
    waypoints.append([4.28918, 4.57365])
    waypoints.append([4.17427, 4.63179])
    waypoints.append([4.05905, 4.68919])
    waypoints.append([3.94041, 4.73902])
    waypoints.append([3.81737, 4.77690])
    waypoints.append([3.69110, 4.80143])
    waypoints.append([3.56305, 4.81469])
    waypoints.append([3.43444, 4.82025])
    waypoints.append([3.30570, 4.82139])
    waypoints.append([3.17696, 4.82089])
    waypoints.append([3.04822, 4.82066])
    waypoints.append([3.04822, 4.82066])
    waypoints.append([2.91947, 4.82088])
    waypoints.append([2.79073, 4.82110])
    waypoints.append([2.66198, 4.82131])
    waypoints.append([2.53324, 4.82150])
    waypoints.append([2.40449, 4.82145])
    waypoints.append([2.27575, 4.82131])
    waypoints.append([2.14701, 4.82143])
    waypoints.append([2.01827, 4.82151])
    waypoints.append([1.88952, 4.82135])
    waypoints.append([1.76078, 4.82139])
    waypoints.append([1.63204, 4.82160])
    waypoints.append([1.50328, 4.82145])
    waypoints.append([1.37454, 4.82129])
    waypoints.append([1.24582, 4.82164])
    waypoints.append([1.11706, 4.82249])
    waypoints.append([0.98829, 4.82279])
    waypoints.append([0.85963, 4.82043])
    waypoints.append([0.73102, 4.81482])
    waypoints.append([0.60254, 4.80519])
    waypoints.append([0.47533, 4.78623])
    waypoints.append([0.35086, 4.75376])
    waypoints.append([0.23074, 4.70744])
    waypoints.append([0.11731, 4.64677])
    waypoints.append([0.01320, 4.57125])
    waypoints.append([-0.08005, 4.48258])
    waypoints.append([-0.16162, 4.38309])
    waypoints.append([-0.23145, 4.27499])
    waypoints.append([-0.28916, 4.15999])
    waypoints.append([-0.33396, 4.03934])
    waypoints.append([-0.36492, 3.91447])
    waypoints.append([-0.38200, 3.78692])
    waypoints.append([-0.38788, 3.65831])
    waypoints.append([-0.38691, 3.52942])
    waypoints.append([-0.37823, 3.40084])
    waypoints.append([-0.36202, 3.27309])
    waypoints.append([-0.33430, 3.14754])
    waypoints.append([-0.29150, 3.02637])
    waypoints.append([-0.23256, 2.91201])
    waypoints.append([-0.15929, 2.80587])
    waypoints.append([-0.07488, 2.70853])
    waypoints.append([0.01953, 2.62104])
    waypoints.append([0.12386, 2.54597])
    waypoints.append([0.23814, 2.48707])
    waypoints.append([0.35908, 2.44313])
    waypoints.append([0.48372, 2.41084])
    waypoints.append([0.61002, 2.38583])
    waypoints.append([0.73711, 2.36546])
    waypoints.append([0.86442, 2.34660])
    waypoints.append([0.99091, 2.32244])
    waypoints.append([1.11453, 2.28664])
    waypoints.append([1.23210, 2.23466])
    waypoints.append([1.34058, 2.16554])
    waypoints.append([1.43733, 2.08071])
    waypoints.append([1.52092, 1.98292])
    waypoints.append([1.59099, 1.87510])
    waypoints.append([1.64848, 1.75994])
    waypoints.append([1.69455, 1.63970])
    waypoints.append([1.73034, 1.51615])
    waypoints.append([1.75658, 1.39016])
    waypoints.append([1.77663, 1.26284])
    waypoints.append([1.79973, 1.13631])
    waypoints.append([1.82957, 1.01122])
    waypoints.append([1.86440, 0.88700])
    waypoints.append([1.90882, 0.76627])
    waypoints.append([1.96812, 0.65233])
    waypoints.append([2.04087, 0.54618])
    waypoints.append([2.12507, 0.44870])
    waypoints.append([2.21965, 0.36139])
    waypoints.append([2.32488, 0.28790])
    waypoints.append([2.44086, 0.23215])
    waypoints.append([2.56395, 0.19401])
    waypoints.append([2.69066, 0.17272])
    waypoints.append([2.81917, 0.16817])
    waypoints.append([2.94743, 0.17985])
    waypoints.append([3.07323, 0.20677])
    waypoints.append([3.19543, 0.24696])
    waypoints.append([3.31378, 0.29762])
    waypoints.append([3.42923, 0.35467])
    waypoints.append([3.54434, 0.41216])
    waypoints.append([3.66280, 0.46268])
    waypoints.append([3.78561, 0.50091])
    waypoints.append([3.91208, 0.52447])
    waypoints.append([4.04028, 0.53699])
    waypoints.append([4.16887, 0.54167])
    waypoints.append([4.29757, 0.53973])

    return waypoints


if __name__ == "__main__":
    calc()
