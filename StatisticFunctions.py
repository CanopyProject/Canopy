import numpy as np

#Number of Observations - The total number of lidar pings that were performed in that area
def NumberofObservations(list):
    num = 0
    for item in list:
        num += 1

    return num

#Data Quality - The average quality of the observations
def DataQuality(list):
    meanQuality = np.mean(list)

    return meanQuality

#Density of Observations - The amount of observations per km2
def DensityofObservations(ObList,area):
    num = NumberofObservations(ObList)

    density = num/area

    return  density

#Standard deviation of the density of observations - Standard deviation performed on the density of observations
def StandardDeviationOfDensityOfObservations(list):
    std = np.std(list,ddof=1)
    return  std

#Mean Vegetation Height - The average vegetation height found over the entire area
def MeanVegetationHeight(list):
    meanHeight = np.mean(list)

    return meanHeight

#Standard Deviation of Vegetation Height - The standard deviation of the vegetation heights found over the entire area
def StandardDeviationOfVegetationHeight(list):
    std = np.std(list,ddof=1)
    return std


