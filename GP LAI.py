import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import math

# Load the data
data = np.loadtxt("D:\\temp\\namielai\\rg1.txt", usecols=(0, 1, 2))
data2D = np.loadtxt("D:\\temp\\namielai\\rg1.txt", usecols=(0, 1))

# Compute the convex hull
hull = ConvexHull(data2D)
area = 0.5 * np.abs(np.dot(hull.points[hull.vertices, 0], np.roll(hull.points[hull.vertices, 1], 1)) - 
                    np.dot(hull.points[hull.vertices, 1], np.roll(hull.points[hull.vertices, 0], 1)))

# Define the X and Y limits
X_min, Y_min = np.min(data2D, axis=0)
X_max, Y_max = np.max(data2D, axis=0)

# Compute gap fraction and eLAI for each resolution
#res = np.linspace(0.001, 0.02, num=10)
res = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01]
gf = np.zeros_like(res)
eLAI = np.zeros_like(res)

fig, axes = plt.subplots(nrows=2, ncols=5, dpi = 100)
for i, r in enumerate(res):
    X_length = int(np.ceil((X_max - X_min) / r))
    Y_length = int(np.ceil((Y_max - Y_min) / r))
    GF_map = np.zeros((X_length, Y_length))
    X_cor = np.floor((data[:, 0] - X_min) / r).astype(int)
    Y_cor = np.floor((data[:, 1] - Y_min) / r).astype(int)
    GF_map[X_cor, Y_cor] = 1
    gf[i] = 1 - np.sum(GF_map) / (X_length * Y_length)*(area/((X_max - X_min)*(Y_max - Y_min)))
    eLAI[i] = -math.log(gf[i])
    ax = axes[i // 5, i % 5]
    ax.imshow(GF_map, cmap='tab20c')
    ax.set_title('r={:.4f}\nGF={:.3f}\nLAI={:.3f}'.format(r, gf[i], eLAI[i]))
plt.tight_layout()
plt.show()

#Plot gap fraction and effective LAI versus resolution
#fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
#ax.plot(res, gf, 'o', label='Gap Fraction')
#ax.set_xlabel('Resolution (m)')
#ax.set_ylabel('Gap Fraction')
#ax2 = ax.twinx()
#ax2.plot(res, eLAI, 'o', color='tab:red', label='Effective LAI')
#ax2.set_ylabel('Effective LAI')
#ax2.set_title('Relationship Between Resolution and Gap Fraction/Effective LAI')
#fig.legend()
#plt.show()