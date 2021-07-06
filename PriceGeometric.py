#!/usr/bin/env python
# PyTorch 1.8.1-CPU virtual env.
# Python 3.9.4 Windows 10
# -*- coding: utf-8 -*-

"""The script implement the classical longstaff-schwartz algorithm for pricing american options.
This script focus on the multidimensional case for rainbow option
"""
import numpy as np
import torch
import Products
import SimulationPaths.GBMMultiDim
import time
import FNNMCMultiDim
import h5py

timeStepsTotal = 10
normalizeStrike=100
pathTotal = 10**4
callGeometricAverage = Products.Option(timeToMat=1, strike=1, typeOfContract="CallGeometricAverage")
marketVariables = Products.MarketVariables(r=0.03, dividend=0.05, vol=0.4, spot=[100/normalizeStrike]*7, correlation=0.0)
hyperparameters = FNNMCMultiDim.Hyperparameters(learningRate=0.001, inputSize=7, hiddenlayer1=100, hiddenlayer2=100, epochs=10, batchSize=10**4)

#timeSimPathsStart = time.time()
#learningPaths = SimulationPaths.GBMMultiDim.simulatePaths(timeStepsTotal=timeStepsTotal,pathsTotal=10**4, marketVariables=marketVariables, timeToMat=callGeometricAverage.timeToMat)
#timeSimPathsEnd = time.time()
#print(f"Time taken to simulate paths is: {timeSimPathsEnd-timeSimPathsStart:f}")
#Safe data
#f = h5py.File('data/GeometricAveragePaths.hdf5', 'w')
#f.create_dataset('RND', data = learningPaths)
#f.close()
# load data
f = h5py.File('data/GeometricAveragePaths.hdf5', 'r')
learningPaths = f['RND'][...]

#timeRegressionStart = time.time()
#FNNMCMultiDim.findNeuralNetworkModels(simulatedPaths=learningPaths, Option=callGeometricAverage, MarketVariables=marketVariables, hyperparameters=hyperparameters)
#timeRegressionEnd = time.time()
#print(f"Time taken for find regressioncoefficients: {timeRegressionEnd-timeRegressionStart:f}")
#estimates = np.zeros(100)
#for i in range(100):
#    # create empirical estimations
#    pricingPaths = SimulationPaths.GBMMultiDim.simulatePaths(timeStepsTotal=timeStepsTotal,pathsTotal=pathTotal, marketVariables=marketVariables, timeToMat=callGeometricAverage.timeToMat)
#    timePriceStart = time.time()
#    price = FNNMCMultiDim.priceAmericanOption(simulatedPaths=pricingPaths, Option=callGeometricAverage, MarketVariables=marketVariables, hyperparameters=hyperparameters)*normalizeStrike
#    timePriceEnd = time.time()
#    print(f"Time taken for Pricing: {timePriceEnd-timePriceStart:f}")
#    print(f"The estimated price is: {price:f} and the true price is: 3.27")
#    estimates[i]=price
#print("Mean: ", np.mean(estimates))
#print("Std Error Mean: ", np.std(estimates)/10)

import LSMMultiDim
# create empirical estimations
timeRegressionStart = time.time()
coefMatrix = LSMMultiDim.findRegressionCoefficient(simulatedPaths=learningPaths, Option=callGeometricAverage, MarketVariables=marketVariables, regressionBasis="geometricAverage")
timeRegressionEnd = time.time()
print(f"Time taken for find regressioncoefficients: {timeRegressionEnd-timeRegressionStart:f}")
estimates = np.zeros(100)
for i in range(100):
    # create empirical estimations
    pricingPaths = SimulationPaths.GBMMultiDim.simulatePaths(timeStepsTotal=timeStepsTotal,pathsTotal=pathTotal, marketVariables=marketVariables, timeToMat=callGeometricAverage.timeToMat)
    timePriceStart = time.time()
    price = LSMMultiDim.priceAmericanOption(coefMatrix,pricingPaths,callGeometricAverage, marketVariables, "geometricAverage")*normalizeStrike
    timePriceEnd = time.time()
    print(f"Time taken for Pricing: {timePriceEnd-timePriceStart:f}")
    print(f"The estimated price is: {price:f} and the true price is: 3.27")
    estimates[i]=price
print("Mean: ", np.mean(estimates))
print("Std Error Mean: ", np.std(estimates)/10)
