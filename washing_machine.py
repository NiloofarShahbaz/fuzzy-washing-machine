import scipy.integrate as integrate
import numpy as np
import math

WEIGHT_MAX = 16
DIRT_MAX = 100
RPM_MAX = 20000
SIGMA = 0.4


def fuzzy(weight, dirt):
    weight_members = fire_weight(weight)
    dirt_members = fire_dirt(dirt)
    print(weight_members)
    print(dirt_members)
    expert_rule = get_expert_rule(weight_members, dirt_members)

    for rule in expert_rule:
        print('rule:', rule)

    for rule in expert_rule:
        if rule[2] is 0:  # VVVVL
            mean = 4
            a = rule[3]
            if a == 0.0:
                rule[4] = 0
            else:
                xa = gaussian_reverse(mean, x=a, left=False)

                k1 = integrate.quad(lambda x: a * x, 0, xa) + integrate.quad(lambda x: gaussian(mean, x) * x, xa,
                                                                             np.inf)
                k2 = integrate.quad(lambda x: a, 0, xa) + integrate.quad(lambda x: gaussian(mean, x), xa, np.inf)
                print('k1', k1, xa, a)
                rule[4] = k1[0] / k2[0]

        elif rule[2] is 1:  # VVVL
            mean = 1670
            rule[4] = mean  # VVL
        elif rule[2] is 2:
            mean = 3336
            rule[4] = mean
        elif rule[2] is 3:  # VL
            mean = 5002
            rule[4] = mean
        elif rule[2] is 4:  # L
            mean = 6668
            rule[4] = mean
        elif rule[2] is 5:  # LM
            mean = 8334
            rule[4] = mean
        elif rule[2] is 6:  # M
            mean = 10000
            rule[4] = mean
        elif rule[2] is 7:  # HM
            mean = 11666
            rule[4] = mean
        elif rule[2] is 8:  # H
            mean = 13332
            rule[4] = mean
        elif rule[2] is 9:  # VH
            mean = 14998
            rule[4] = mean
        elif rule[2] is 10:  # VVH
            mean = 16664
            rule[4] = mean
        elif rule[2] is 11:  # VVVH
            mean = 18330
            rule[4] = mean
        elif rule[2] is 12:  # VVVVH
            mean = 19996
            a = rule[3]
            if a == 0:
                rule[4] = 0
            else:
                xa = gaussian_reverse(mean, x=a, left=True)

                k1 = integrate.quad(lambda x: gaussian(mean, x) * x, -np.inf, xa) + integrate.quad(lambda x: a * x, xa,
                                                                                                   RPM_MAX)
                k2 = integrate.quad(lambda x: gaussian(mean, x), -np.inf, xa) + integrate.quad(lambda x: a, xa, RPM_MAX)
                rule[4] = k1[0] / k2[0]

    for rule in expert_rule:
        print('ruleeeeeeeee:', rule)

    sum1 = 0
    sum2 = 0

    for rule in expert_rule:
        sum1 = sum1 + rule[3] * rule[4]
        sum2 = sum2 + rule[3]

    rms_star = sum1 / sum2
    return rms_star


def fire_weight(x):
    weight_members = [0.0 for i in range(0, 7)]
    if x > WEIGHT_MAX:
        x = WEIGHT_MAX

    if x <= 2:
        mean = 2
        weight_members[0] = gaussian(mean, mean)
    elif not weight_members[0]:
        mean = 2
        weight_members[0] = gaussian(mean, x)

    mean = 4
    weight_members[1] = gaussian(mean, x)

    mean = 6
    weight_members[2] = gaussian(mean, x)

    mean = 8
    weight_members[3] = gaussian(mean, x)

    mean = 10
    weight_members[4] = gaussian(mean, x)

    mean = 12
    weight_members[5] = gaussian(mean, x)

    if x >= 14:
        mean = 14
        weight_members[6] = gaussian(mean, mean)
    elif not weight_members[6]:
        mean = 14
        weight_members[6] = gaussian(mean, x)

    return weight_members


def fire_dirt(x):
    dirt_members = [0.0 for i in range(0, 7)]
    if x > DIRT_MAX:
        x = DIRT_MAX

    if x <= 8:
        mean = 8
        dirt_members[0] = gaussian(mean, mean)
    elif not dirt_members[0]:
        mean = 8
        dirt_members[0] = gaussian(mean, x)

    mean = 22
    dirt_members[1] = gaussian(mean, x)

    mean = 36
    dirt_members[2] = gaussian(mean, x)

    mean = 50
    dirt_members[3] = gaussian(mean, x)

    mean = 64
    dirt_members[4] = gaussian(mean, x)

    mean = 78
    dirt_members[5] = gaussian(mean, x)

    if x >= 92:
        mean = 92
        dirt_members[6] = gaussian(mean, mean)
    elif not dirt_members[6]:
        mean = 92
        dirt_members[6] = gaussian(mean, x)

    return dirt_members


def get_expert_rule(weight_members, dirt_members):
    return [
        [weight_members[0], dirt_members[0], 0, weight_members[0] * dirt_members[0], 0],
        [weight_members[0], dirt_members[1], 1, weight_members[0] * dirt_members[1], 0],
        [weight_members[0], dirt_members[2], 2, weight_members[0] * dirt_members[2], 0],
        [weight_members[0], dirt_members[3], 3, weight_members[0] * dirt_members[3], 0],
        [weight_members[0], dirt_members[4], 4, weight_members[0] * dirt_members[4], 0],
        [weight_members[0], dirt_members[5], 5, weight_members[0] * dirt_members[5], 0],
        [weight_members[0], dirt_members[6], 6, weight_members[0] * dirt_members[6], 0],

        [weight_members[1], dirt_members[0], 1, weight_members[1] * dirt_members[0], 0],
        [weight_members[1], dirt_members[1], 2, weight_members[1] * dirt_members[1], 0],
        [weight_members[1], dirt_members[2], 3, weight_members[1] * dirt_members[2], 0],
        [weight_members[1], dirt_members[3], 4, weight_members[1] * dirt_members[3], 0],
        [weight_members[1], dirt_members[4], 5, weight_members[1] * dirt_members[4], 0],
        [weight_members[1], dirt_members[5], 6, weight_members[1] * dirt_members[5], 0],
        [weight_members[1], dirt_members[6], 7, weight_members[1] * dirt_members[6], 0],

        [weight_members[2], dirt_members[0], 2, weight_members[2] * dirt_members[0], 0],
        [weight_members[2], dirt_members[1], 3, weight_members[2] * dirt_members[1], 0],
        [weight_members[2], dirt_members[2], 4, weight_members[2] * dirt_members[2], 0],
        [weight_members[2], dirt_members[3], 5, weight_members[2] * dirt_members[3], 0],
        [weight_members[2], dirt_members[4], 6, weight_members[2] * dirt_members[4], 0],
        [weight_members[2], dirt_members[5], 7, weight_members[2] * dirt_members[5], 0],
        [weight_members[2], dirt_members[6], 8, weight_members[2] * dirt_members[6], 0],

        [weight_members[3], dirt_members[0], 3, weight_members[3] * dirt_members[0], 0],
        [weight_members[3], dirt_members[1], 4, weight_members[3] * dirt_members[1], 0],
        [weight_members[3], dirt_members[2], 5, weight_members[3] * dirt_members[2], 0],
        [weight_members[3], dirt_members[3], 6, weight_members[3] * dirt_members[3], 0],
        [weight_members[3], dirt_members[4], 7, weight_members[3] * dirt_members[4], 0],
        [weight_members[3], dirt_members[5], 8, weight_members[3] * dirt_members[5], 0],
        [weight_members[3], dirt_members[6], 9, weight_members[3] * dirt_members[6], 0],

        [weight_members[4], dirt_members[0], 4, weight_members[4] * dirt_members[0], 0],
        [weight_members[4], dirt_members[1], 5, weight_members[4] * dirt_members[1], 0],
        [weight_members[4], dirt_members[2], 6, weight_members[4] * dirt_members[2], 0],
        [weight_members[4], dirt_members[3], 7, weight_members[4] * dirt_members[3], 0],
        [weight_members[4], dirt_members[4], 8, weight_members[4] * dirt_members[4], 0],
        [weight_members[4], dirt_members[5], 9, weight_members[4] * dirt_members[5], 0],
        [weight_members[4], dirt_members[6], 10, weight_members[4] * dirt_members[6], 0],

        [weight_members[5], dirt_members[0], 5, weight_members[5] * dirt_members[0], 0],
        [weight_members[5], dirt_members[1], 6, weight_members[5] * dirt_members[1], 0],
        [weight_members[5], dirt_members[2], 7, weight_members[5] * dirt_members[2], 0],
        [weight_members[5], dirt_members[3], 8, weight_members[5] * dirt_members[3], 0],
        [weight_members[5], dirt_members[4], 9, weight_members[5] * dirt_members[4], 0],
        [weight_members[5], dirt_members[5], 10, weight_members[5] * dirt_members[5], 0],
        [weight_members[5], dirt_members[6], 11, weight_members[5] * dirt_members[6], 0],

        [weight_members[6], dirt_members[0], 6, weight_members[6] * dirt_members[0], 0],
        [weight_members[6], dirt_members[1], 7, weight_members[6] * dirt_members[1], 0],
        [weight_members[6], dirt_members[2], 8, weight_members[6] * dirt_members[2], 0],
        [weight_members[6], dirt_members[3], 9, weight_members[6] * dirt_members[3], 0],
        [weight_members[6], dirt_members[4], 10, weight_members[6] * dirt_members[4], 0],
        [weight_members[6], dirt_members[5], 11, weight_members[6] * dirt_members[5], 0],
        [weight_members[6], dirt_members[6], 12, weight_members[6] * dirt_members[6], 0],
    ]


def gaussian(mean, x):
    return (1 / math.sqrt(2 * math.pi * (SIGMA ** 2))) * math.exp(-((x - mean) ** 2) / (2 * (SIGMA ** 2)))


def gaussian_reverse(mean, x, left):
    if left:
        return -math.sqrt(-2 * (SIGMA ** 2) * math.log(math.sqrt(2 * math.pi * (SIGMA ** 2)) * x, math.e)) + mean
    else:
        return math.sqrt(-2 * (SIGMA ** 2) * math.log(math.sqrt(2 * math.pi * (SIGMA ** 2)) * x, math.e)) + mean


print(fuzzy(weight=15, dirt=30))
