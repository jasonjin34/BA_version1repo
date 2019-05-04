import numpy as np
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from cubic_sphere import Sphere, Cubic, listcopy, projection_origin, projection_test_fun
from image_preprocess import findEffectivePoints

'''generate the test image of longtitude and latitude for reverse
   projection 
'''
class testCircleImage:
    image_data = [[], [], []]
    def __init__(self, edgesize, samplesize, divide_input):
        self.edge = edgesize
        self.sample_size = samplesize
        self.divide = divide_input

    def generate_data(self):
        phi = np.arange(0.0, np.pi * (1 + 1 / self.divide), np.pi / self.divide)
        rho = np.arange(-self.edge/2, self.edge/2 + self.edge/self.sample_size, self.edge/self.sample_size)
        '''first facet z = -10'''
        for phi_index in phi:
            for rho_index in rho:
                self.image_data[0].append(rho_index*np.cos(phi_index))
                self.image_data[1].append(rho_index*np.sin(phi_index))
                self.image_data[2].append(-self.edge/2)

        '''second facet z = 10'''
        for phi_index in phi:
            for rho_index in rho:
                self.image_data[0].append(rho_index*np.cos(phi_index))
                self.image_data[1].append(rho_index*np.sin(phi_index))
                self.image_data[2].append(self.edge/2)

class testLineImage:
    image_data = [[], [], []]
    '''constructor: testimage edge size, in total 6 facets'''
    def __init__(self, edgesize, samplesize, divide_input):
        self.edge = edgesize
        self.sample_size = samplesize
        self.divide = divide_input

    '''test for the first side'''
    def generate_data(self):
        step = np.arange(-self.edge/2, self.edge/2 + self.edge/self.divide, self.edge/self.divide)
        step_sample = np.arange(-self.edge/2, self.edge/2 + self.edge/self.sample_size, self.edge/self.sample_size)
        '''first facet x = -10'''
        for step_index in step:
            for sample_index in step_sample:
                self.image_data[0].append(-self.edge/2)
                self.image_data[2].append(step_index)
                self.image_data[1].append(sample_index)

        '''second facet x = 10'''
        for step_index in step:
            for sample_index in step_sample:
                self.image_data[0].append(self.edge/2)
                self.image_data[1].append(sample_index)
                self.image_data[2].append(step_index)

        '''third facet y = -10'''
        for step_index in step:
            for sample_index in step_sample:
                self.image_data[0].append(sample_index)
                self.image_data[1].append(-self.edge/2)
                self.image_data[2].append(step_index)

        '''fourth facet y = 10'''
        for step_index in step:
            for sample_index in step_sample:
                self.image_data[0].append(sample_index)
                self.image_data[1].append(self.edge/2)
                self.image_data[2].append(step_index)

def reverse_projection(inputdata, edgesize):
    output_data = listcopy(inputdata)
    print("the size of list " + str(0.25*len(output_data[0])))
    for index in range(len(output_data[0])):
        '''distance from the point to origin'''
        length = np.sqrt(np.power(output_data[0][index],2) + np.power(output_data[1][index], 2) + np.power(output_data[2][index],2))
        factor = length/(edgesize)
        output_data[0][index] = output_data[0][index]/factor
        output_data[1][index] = output_data[1][index]/factor
        output_data[2][index] = output_data[2][index]/factor
    return output_data

def reverse_projection_result():
    # generate sphere
    sphere = Sphere(100, 10, 10)
    sphere.generate_data()

    # generate cubic
    cubic = Cubic(20, 100, 2)
    cubic.generate_data()

    # testImage
    testData = testLineImage(20, 4, 40) #edge, sample, samplesize
    testData.generate_data()

    # testCircleImage
    testCircleData = testCircleImage(20, 8, 40)
    testCircleData.generate_data()
    reverTestDataCircle = reverse_projection(testCircleData.image_data, 10)

    # reverse projection
    reverTestData=reverse_projection(testData.image_data, 10)

    # set figured
    fig = plt.figure(figsize=(8.5, 9))
    ax = fig.add_subplot(221, projection='3d')
    ax.plot(sphere.sphere_data_display[0], sphere.sphere_data_display[1], sphere.sphere_data_display[2], 'k',
            label='parametric curve', linewidth=1)
    ax.plot(cubic.cubic_data_display[0], cubic.cubic_data_display[1], cubic.cubic_data_display[2], 'g',
            label='parametric curve', linewidth=0.5)
    ax.scatter(testData.image_data[0], testData.image_data[1], testData.image_data[2], 'r', marker='o', s=1, color='r')

    ax2 = fig.add_subplot(222, projection="3d")
    ax2.plot(sphere.sphere_data_display[0], sphere.sphere_data_display[1], sphere.sphere_data_display[2], 'k',
            label='parametric curve', linewidth=0.5)
    ax2.scatter(reverTestData[0], reverTestData[1], reverTestData[2], 'r', marker='o', s=1, color='r')

    ax3 = fig.add_subplot(223, projection="3d")
    ax3.plot(sphere.sphere_data_display[0], sphere.sphere_data_display[1], sphere.sphere_data_display[2], 'k',
            label='parametric curve', linewidth=1)
    ax3.plot(cubic.cubic_data_display[0], cubic.cubic_data_display[1], cubic.cubic_data_display[2], 'g',
            label='parametric curve', linewidth=0.5)
    ax3.scatter(testCircleData.image_data[0], testCircleData.image_data[1], testCircleData.image_data[2], 'r', marker='o', s=1, color='r')


    ax4 = fig.add_subplot(224, projection="3d")
    ax4.plot(sphere.sphere_data_display[0], sphere.sphere_data_display[1], sphere.sphere_data_display[2], 'k',
            label='parametric curve', linewidth=0.5)
    ax4.scatter(reverTestDataCircle[0], reverTestDataCircle[1], reverTestDataCircle[2], 'r', marker='o', s=1, color='r')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()


'''find the point for great circle'''
def showreverseData(input):
    output = [[], [], []]
    index_list = []
    for index in range(len(input[2])):
        if max(input[2]) == np.abs(input[2][index]):
            output[0].append(input[0][index])
            output[1].append(input[1][index])
            output[2].append(input[2][index])
            index_list.append(index)
    return output, index_list


def crossPoduct(pointlist,index1, index2):
    x_value = pointlist[1][index1] * pointlist[2][index2] - pointlist[2][index1] * pointlist[1][index2]
    y_value = pointlist[2][index1] * pointlist[0][index2] - pointlist[0][index1] * pointlist[2][index2]
    z_value = pointlist[0][index1] * pointlist[1][index2] - pointlist[1][index1] * pointlist[0][index2]
    if x_value == 0 and y_value == 0 and z_value == 0:
        x_value = (pointlist[1][index1] + 0.0001) * (pointlist[2][index2] + 0.0001) - (pointlist[2][index1] + 0.0001) * (pointlist[1][index2] + 0.0001)
        y_value = (pointlist[2][index1] + 0.0001) * (pointlist[0][index2] + 0.0001) - (pointlist[0][index1] + 0.0001) * (pointlist[2][index2] + 0.0001)
        z_value = (pointlist[0][index1] + 0.0001) * (pointlist[1][index2] + 0.0001) - (pointlist[1][index1] + 0.0001) * (pointlist[0][index2] + 0.0001)
    reference_vector = []
    reference_vector.append(x_value)
    reference_vector.append(y_value)
    reference_vector.append(z_value)
    return reference_vector

def dotPoduct(pointsList, pointIndex, referencePoint):
    return pointsList[0][pointIndex]*referencePoint[0] + pointsList[1][pointIndex]*referencePoint[1] + pointsList[2][pointIndex]*referencePoint[2]

'''great circle class'''
class greatCircle():
    pointlist = [[], [], []]
    circleData = [[], [], [], []]
    spheredata = [[], [], []]
    def __init__(self, inputlist,sphere):
        self.pointlist = listcopy(inputlist)
        self.spheredata = sphere

    '''generate the great circle functions'''
    def generate_data(self):
        count = 0
        for first_index in range(len(self.pointlist[0])):
            for second_index in range(first_index + 1, len(self.pointlist[0])):
                if first_index != second_index:
                    count = count + 1
                    refVector = crossPoduct(self.pointlist, first_index, second_index)
                    if abs(refVector[0] + refVector[1] + refVector[2]) > 0.001:
                        for sphereindex in range(len(self.spheredata[0])):
                            dotProduct_result = dotPoduct(self.spheredata, sphereindex, refVector)
                            if abs(dotProduct_result) < 5:
                                self.circleData[0].append(self.spheredata[0][sphereindex])
                                self.circleData[1].append(self.spheredata[1][sphereindex])
                                self.circleData[2].append(self.spheredata[2][sphereindex])
                                self.circleData[3].append(0) # Counting the close neighbor

    def generate_data_test(self):
        refVector = crossPoduct(self.pointlist, 2, 3)
        if abs(refVector[0] + refVector[1] + refVector[2]) > 0.001:
            for sphereindex in range(len(self.spheredata[0])):
                dotProduct_result = dotPoduct(self.spheredata, sphereindex, refVector)
                if abs(dotProduct_result) < 10:
                    self.circleData[0].append(self.spheredata[0][sphereindex])
                    self.circleData[1].append(self.spheredata[1][sphereindex])
                    self.circleData[2].append(self.spheredata[2][sphereindex])


'''minimize the error function'''
def pole_estimation(circleData):
    pole_list = [[], [], []]
    count = 0
    data_length = len(circleData[0])
    totalinteration = data_length*data_length
    start = time.time()
    for index_data in range(data_length):
        for index_reference in range(data_length):
            if index_data != index_reference:
                timebefore = int(100*count/totalinteration)
                count = count + 1
                timenow = int(100*count/totalinteration)
                if timebefore != timenow:
                    print('processing... ' + str(timenow) + '%')
                x_diff = circleData[0][index_data] - circleData[0][index_reference]
                y_diff = circleData[1][index_data] - circleData[1][index_reference]
                z_diff = circleData[2][index_data] - circleData[2][index_reference]
                error = x_diff*x_diff + y_diff*y_diff + z_diff*z_diff
                if error < 1:
                    circleData[3][index_data] = circleData[3][index_data] + 1
    min_value = min(circleData[3])
    for index_data in range(data_length):
        if circleData[3][index_data] >= 15*min_value:
            pole_list[0].append(circleData[0][index_data])
            pole_list[1].append(circleData[1][index_data])
            pole_list[2].append(circleData[2][index_data])
    print(pole_list)
    print(len(pole_list[0]))
    end = time.time()
    print(end-start)
    return pole_list


'''delete highest remark point'''
def removeHighestData(input, list):
    count = 0
    for index in range(len(list)):
        input[0].pop(list[index] - count)
        input[1].pop(list[index] - count)
        input[2].pop(list[index] - count)
        count = count + 1
    return input

'''test function for pose estimation result '''
def TestFunctions():
    # generate sphere
    sphere = Sphere(100, 10, 10)
    sphere.generate_data()

    # testImage
    testData = testLineImage(20, 4, 40) #edge, sample, samplesize
    testData.generate_data()


    # reverse projection
    reverTestData = reverse_projection(testData.image_data, 10)

    #print the projection points results
    greatcircle_list, index_list = showreverseData(reverTestData)

    greatcircle_test = greatCircle(greatcircle_list, sphere.sphere_data)
    greatcircle_test.generate_data()

    pole_list = pole_estimation(greatcircle_test.circleData)


    # set figured
    fig = plt.figure(figsize=(17.5, 8.5))
    ax = fig.add_subplot(121, projection="3d")
    ax.set_title('Draw Great Circle')
    ax.scatter(0, 0, 0, marker='o', s=20, color='g')
    ax.plot(sphere.sphere_data_display[0], sphere.sphere_data_display[1], sphere.sphere_data_display[2], 'k',
            label='parametric curve', linewidth=0.5)
    #ax.scatter(reverTestData[0], reverTestData[1], reverTestData[2], 'r', marker='o', s=1, color='r')
    ax.scatter(greatcircle_list[0], greatcircle_list[1], greatcircle_list[2], 'b', marker='X', s=20
               , color='b')
    ax.scatter(greatcircle_test.circleData[0],greatcircle_test.circleData[1], greatcircle_test.circleData[2], 'b', marker='o', s=1, color='r')

    ax1 = fig.add_subplot(122, projection="3d")
    ax1.set_title("Pose Estimation for the projections")
    ax1.scatter(pole_list[0], pole_list[1], pole_list[2], 'b', marker='D', s=10, color='g')
    ax1.scatter(0, 0, 0, marker='o', s=20, color='r')
    ax1.plot(sphere.sphere_data_display[0], sphere.sphere_data_display[1], sphere.sphere_data_display[2], 'k',
            label='parametric curve', linewidth=0.5)
    ax1.scatter(greatcircle_list[0], greatcircle_list[1], greatcircle_list[2], 'b', marker='X', s=30, color='b')

    ax1.text(0.8, 0.0, 0.0, 'center',  color='green', fontsize=10, fontweight='bold')
    ax1.text(0.0, 0.0, 10.0, 'pole',  color='green', fontsize=10, fontweight='bold')
    ax1.text(10, -10, -10, 'blue points line ares the end points of arcs',  color='green', fontsize=10, fontweight='bold')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    ax1.set_xlabel('X Label')
    ax1.set_ylabel('Y Label')
    ax1.set_zlabel('Z Label')
    plt.show()

def main():
    # generate sphere
    sphere = Sphere(100, 10, 10)
    sphere.generate_data()

    # testImage
    testData = findEffectivePoints()

    # reverse projection
    reverTestData = reverse_projection(testData, 10)

    greatcircle_test = greatCircle(reverTestData, sphere.sphere_data)
    greatcircle_test.generate_data()
    pole_list = pole_estimation(greatcircle_test.circleData)

    ''' ********************* plot image ***********************'''
    fig = plt.figure(figsize=(17.5, 8.5))
    ax = fig.add_subplot(121, projection="3d")
    ax.set_title('Draw Great Circle')
    ax.scatter(0, 0, 0, marker='o', s=20, color='g')
    ax.plot(sphere.sphere_data_display[0], sphere.sphere_data_display[1], sphere.sphere_data_display[2], 'k',
            label='parametric curve', linewidth=0.5)
    #ax.scatter(reverTestData[0], reverTestData[1], reverTestData[2], 'r', marker='o', s=1, color='r')
    ax.scatter(reverTestData[0], reverTestData[1], reverTestData[2], 'b', marker='X', s=20
               , color='b')
    ax.scatter(greatcircle_test.circleData[0],greatcircle_test.circleData[1], greatcircle_test.circleData[2], 'b', marker='o', s=1, color='r')


    ax1 = fig.add_subplot(122, projection="3d")
    ax1.set_title("Pose Estimation for the projections")
    ax1.scatter(pole_list[0], pole_list[1], pole_list[2], 'b', marker='D', s=10, color='g')
    ax1.scatter(0, 0, 0, marker='o', s=20, color='r')
    ax1.plot(sphere.sphere_data_display[0], sphere.sphere_data_display[1], sphere.sphere_data_display[2], 'k',
            label='parametric curve', linewidth=0.5)
    ax1.scatter(reverTestData[0], reverTestData[1], reverTestData[2], 'b', marker='X', s=30, color='b')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    ax1.set_xlabel('X Label')
    ax1.set_ylabel('Y Label')
    ax1.set_zlabel('Z Label')
    plt.show()


if __name__ == "__main__":
    main()



