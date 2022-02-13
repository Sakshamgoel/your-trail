import random as r
import sys
import json
# [loc (x,y), length, climb, decent, h, m, s, difficulty]

# number of neighbors looked at
number_of_neighbors = 5

# average value of any number of points (xavg, yavg)
def avgPoint(vectors):
    Xs = 0
    Ys = 0
    for vec in vectors:
        Xs += vec[0][0]
        Ys += vec[0][1]

    return (Xs/len(vectors), Ys/len(vectors))

# vector form of numerical average
def avgNum(vectors):
    vals = [0 for _ in range(7)]

    for vec in vectors:
        for i in range(len(vals)):
            vals[i] += vec[i+1]

    return vals[0]/len(vectors), vals[1]/len(vectors), vals[2]/len(vectors), vals[3]/len(vectors), vals[4]/len(vectors), vals[5]/len(vectors), vals[6]/len(vectors)

# combining the point and num averages to get all feature averages
def avg(vectors):
    a = avgPoint(vectors)
    b, c, d, e, f, g, h = avgNum(vectors)

    #e = avgHike(vectors)
    #[loc, dist, climb, decent, h, m, s, diff]
    return [a,b,c,d,e,f,g,h]

# distance between any 2 points in the hyperplane
def distance(A, B):
    assert(len(A) == len(B))
    values = [0 for x in range(len(A))]

    for index in range(len(A)):

        if isinstance(A[index], tuple):
            values[index] = ((B[index][0]-A[index][0])**2+(B[index][1]-A[index][1])**2)**0.5

        elif isinstance(A[index], float):
            values[index] = abs(A[index]-B[index])

        elif isinstance(A[index], int):
            values[index] = abs(A[index]-B[index])

        else:
            values[index] =  0 if A[index] == B[index] else 1

    return round(sum(values)/(len(A)+1), ndigits = 5)

# normalize values to be between 0 and 1
def normalize(x, mn, mx):

    if isinstance(x, tuple):
        return (round((x[0]-mn[0])/max(1,mx[0]-mn[0]), ndigits = 5),round((x[1]-mn[1])/max(1, mx[1]-mn[1]), ndigits = 5))

    #elif isinstance(x, Hikes):
        #return round(int(x.value)/numClasses, ndigits = 5)

    else:
        return round((x-mn)/max(1,mx-mn), ndigits = 5)

# generates test data
def generateFrame():
    a = (r.random()*90,r.random()*180)
    b = r.random() * 20
    c = r.random() * 30
    d = r.random() * 30
    e = r.randrange(0,7)
    f = r.randrange(0,60)
    g = r.randrange(0,60)
    h = r.randint(0,5)
    return [a,b,c,d,e,f,g,h]


def minmaxArrs(data):
    mins = [(-90,-180), 0, 0, 0, 0, 0, 0, 0]
    maxs = [(90,180), 0, 0, 0, 0, 60, 60, 5]
    for x in range(len(data)):
        for i in range(1,5):
            if data[x][i] > maxs[i]:
                maxs[i] = data[x][i]
    return mins, maxs

def normalizeVector(vec, mins, maxs):
    result = []
    for item in range(len(vec)):
        result.append(normalize(vec[item], mins[item], maxs[item]))
    return result

def normAll(data, min, max):
    newData = []

    for item in data:
        newData.append(normalizeVector(item, min, max))

    return newData

def predict(frame, data, k= number_of_neighbors):
    #print('frame ',frame)
    #print('data ',data)
    keyframes = []
    for item in data:
        keyframes.append((distance(frame, item), item))
    keyframes.sort(key = lambda x: x[0])
    return keyframes[1:k+1]

def predictCentroid(frames, data, k = number_of_neighbors):
    return predict(avg(frames), data, k)

def multiPredict(frames, data, k = number_of_neighbors):
    if len(frames) == 1:
        return predict(frames[0])

    else:
        avgPredict = predictCentroid(frames, data, k)
        locPredict = []
        for x in range(len(frames)):
            locPredict.extend(predict(frames[x], data, k=10))
        final = []
        for item in avgPredict:
            if item in locPredict:
                final.append(item)

        if len(final) < 2:
            arr = r.sample(avgPredict, k= max(1,len(avgPredict)-2))
            arr.extend(r.sample(locPredict, k= max(1,len(locPredict)-2)))
            return arr[0:k]
        else:
            return final

def importData(vals = 0, filename = './cleanData.txt'):
    titles = []
    data = []
    raw = []
    with open(filename, 'r') as f:
        raw = f.readlines()
        f.close()

    if vals > 0:
        raw = raw[0:vals]

    for item in raw:
        parts = item.split(',')
        titles.append(str(parts[1]))
        data.append([(float(parts[2]),float(parts[3])), float(parts[4]), float(parts[5]), float(parts[6]), int(parts[7]), int(parts[8]), int(parts[9]), int(parts[10])])

    return titles, data

def lookupName(dataFrame, t, v):
    index = v.index(dataFrame)
    return t[index]


def lookupIndex(dataFrame, nv):
    return nv.index(dataFrame)

def fullPrediction(loc, dist, diff):
    og_titles, og_values = importData()
    illegal = []
    for index in range(len(og_values)):
        if og_values[index][7] > diff+1:
            illegal.append(index)

    #print(len(illegal), len(values))
    titles = []
    values = []
    for x in range(len(og_values)):
        if x in illegal:
            pass
        else:
            titles.append(og_titles[x])
            values.append(og_values[x])
    results = []
    minimum, maximum = minmaxArrs(values)
    norm_values = normAll(values, minimum, maximum)
    temp = [loc, dist, r.randrange(minimum[2], maximum[2]), r.randrange(minimum[3], maximum[3]), r.randrange(minimum[4], maximum[4]), r.randrange(minimum[5],maximum[5]), r.randrange(minimum[6],maximum[6]), diff]
    nearest = normalizeVector(temp, minimum, maximum)
    vals = predict(nearest, values, k =3)
    similarResult = r.sample(predict(nearest, values, k = 20), k = 10)
    similarResult = [res[1] for res in similarResult]
    centVals = predictCentroid(similarResult, values, k = 5)
    multiVals = multiPredict(similarResult, values, k = 5)

    results.extend(centVals)
    results.extend(multiVals)

    results = [lookupName(item[1], titles, values) for item in results]
    freqs = {item : 0 for item in results}

    for item in results:
        freqs[item] += 1

    most_frequent = list(freqs.items())
    most_frequent.sort(key = lambda x : x[1], reverse = True)
    most_frequent = [item[0] for item in most_frequent]
    return json.dumps(most_frequent)



#titles, values = importData()


a = fullPrediction(tuple((float(sys.argv[1]),float(sys.argv[2]))), float(sys.argv[3]), int(sys.argv[4]))
print(a)
#sys.out(a)

#names = ['rdm%f'%r.random() for _ in range(100)]
#testing_data = [generateFrame() for _ in range(100)]

#minimum, maximum = minmaxArrs(values)
#print(maximum)
#norm_values = normAll(values, minimum, maximum)
#print(values.index(values[50]))

#print('predicting: ', norm_values[26:30])
