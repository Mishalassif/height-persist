import math
import numpy as np

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

def fibonacci_sphere(samples=1000):

    points = []
    phi = math.pi * (3. - math.sqrt(5.))  # golden angle in radians

    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2  # y goes from 1 to -1
        radius = math.sqrt(1 - y * y)  # radius at y

        theta = phi * i  # golden angle increment

        x = math.cos(theta) * radius
        z = math.sin(theta) * radius

        points.append([x, y, z])

    return points

def fibonacci_semisphere(samples=1000):

    points = []
    phi = math.pi * (3. - math.sqrt(5.))  # golden angle in radians
    
    for i in range(samples):
        y = 1 - (i / float(2*samples - 1)) * 2  # y goes from 1 to 0
        radius = math.sqrt(1 - y * y)  # radius at y

        theta = phi * i  # golden angle increment

        x = math.cos(theta) * radius
        z = math.sin(theta) * radius

        points.append([x, y, z])

    return points

def visualize_fibonacci_sphere(samples=1000):
    points = fibonacci_sphere(samples)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax = plt.axes(projection='3d')

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)

    x = 1 * np.outer(np.cos(u), np.sin(v))
    y = 1 * np.outer(np.sin(u), np.sin(v))
    z = 1 * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='y', linewidth=0, alpha=0.5)

    xdata = [points[i][0] for i in range(len(points))]
    ydata = [points[i][1] for i in range(len(points))]
    zdata = [points[i][2] for i in range(len(points))]

    ax.scatter3D(xdata, ydata, zdata, color='g');
    plt.show()

def visualize_fibonacci_semisphere(samples=1000):
    points = fibonacci_semisphere(samples)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax = plt.axes(projection='3d')

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)

    x = 1 * np.outer(np.cos(u), np.sin(v))
    y = 1 * np.outer(np.sin(u), np.sin(v))
    z = 1 * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='y', linewidth=0, alpha=0.5)

    xdata = [points[i][0] for i in range(len(points))]
    ydata = [points[i][1] for i in range(len(points))]
    zdata = [points[i][2] for i in range(len(points))]

    ax.scatter3D(xdata, ydata, zdata, color='g');
    plt.show()
