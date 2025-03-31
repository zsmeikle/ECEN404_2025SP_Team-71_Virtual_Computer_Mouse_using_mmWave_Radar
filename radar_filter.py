#pointCloud is an array of point cloud data
#pointCloud contains at least 1 point
#y is distance and always positive
def filter_ys(pointCloud):
    newPointCloud = []
    y_avg = 0
    for point in pointCloud:
        y_avg += point[1]
    y_avg /= len(pointCloud)
    print(y_avg)
    for point in pointCloud:
        minY = .95*y_avg
        maxY = 1.05*y_avg
        if point[1] > minY and point[1] < maxY:
            newPointCloud.append(point)
    return newPointCloud

def filter_range(pointCloud, min_range=.05, max_range=3.5):
    newPointCloud = []
    for point in pointCloud:
        if point[1] > min_range and point[1] < max_range:
            newPointCloud.append(point)
    return newPointCloud

def filter_under_avg(pointCloud):
    newPointCloud = []
    y_avg = 0
    for point in pointCloud:
        y_avg += point[1]
    y_avg /= len(pointCloud)
    for point in pointCloud:
        if point[1] < y_avg:
            newPointCloud.append(point)
    return newPointCloud


def simple_avg(vals):

    avg_x = 0
    for x in vals:
        avg_x += x
    avg_x /= len(vals)
    return avg_x

def exponetial_avg(vals):
    avg_x = 0
    total_weights = 0
    for x in range(len(vals)):
        total_weights += x+1
        avg_x += vals[x]*(x+1)
    avg_x /= total_weights
    return avg_x

def geometric_avg(vals):
    if(len(vals) == 0): return 0
    prod = 1
    for num in vals:
        prod *= num
    return prod ** (1/len(vals))