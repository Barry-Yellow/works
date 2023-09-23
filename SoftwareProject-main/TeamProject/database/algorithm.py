def back_tracking(data):
    possible = []
    possible_time = []
    action = []
    counts = []
    time = []
    xy = []
    i = 0
    j = 0
    while True:
        if i < 0:
            break
        while j < len(data[i]):
            action.append(data[i][j].course_id)
            xy.append((i, j))
            count = 0
            for d in data[i]:
                if d.course_id == data[i][j].course_id:
                    time.append(d.time)
                    count += 1
            if check(time):
                j = 0
                counts.append(count)
                break
            else:
                j += 1
                action.pop()
                xy.pop()
                for c in range(count):
                    time.pop()
        if len(action) == 0:
            break
        if xy[-1][0] != i:
            i -= 1
            j = xy[-1][1] + 1
            action.pop()
            xy.pop()
            for c in range(counts[-1]):
                time.pop()
            counts.pop()
            continue
        if check(time) and len(action) == len(data):
            if action not in possible:
                possible.append(action.copy())
                possible_time.append(time.copy())
            j = xy[-1][1] + 1
            action.pop()
            xy.pop()
            for c in range(counts[-1]):
                time.pop()
            counts.pop()
            continue
        i = i+1
    features = []
    for plan in possible_time:
        feature = []
        noEarly = True
        noNight = True
        mon = True
        tue = True
        wed = True
        thur = True
        fri = True
        for time in plan:
            if '1-' in time:
                noEarly = False
            if '9-' in time:
                noNight = False
            if '星期一' in time:
                mon = False
            if '星期二' in time:
                tue = False
            if '星期三' in time:
                wed = False
            if '星期四' in time:
                thur = False
            if '星期五' in time:
                fri = False
        if noEarly:
            feature.append('没有早八！')
        if noNight:
            feature.append('没有晚课！')
        if mon:
            feature.append('星期一没课！')
        if tue:
            feature.append('星期二没课！')
        if wed:
            feature.append('星期三没课！')
        if thur:
            feature.append('星期四没课！')
        if fri:
            feature.append('星期五没课！')
        features.append(feature)
    return possible, features


def check(time):
    if len(time) != len(set(time)):
        return False
    return True


def satisfy(time, length):
    if check(time) and len(time) == length:
        return True
    return False
