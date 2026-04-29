import numpy as np
import matplotlib.pyplot as plt


# eng-kal data
# x = np.array([569,165,165,100,126,77,305,224,223,298,320,240,248])
x = np.array([374, 156, 156, 93, 122, 73, 171, 201, 203, 243, 256, 219, 226])
y = np.array([11,38.7,33.4,40.7,35.6,41.3,29.1,26.6,34.4,23.8,22.6,30.8,30.7])
labels = [
"0-shot", "5-shot", "Extra Parallel", "Extra + Wordlist", "Full Parallel", "Full + Wordlist", "Wordlist",
"Extra only", "Full book", "Book non-parallel", "Book non-parallel/pairs", "Book parallel+pairs", "Book parallel"
]

# kal-eng data
# x = np.array([395, 94, 94, 62, 57, 41, 164, 127, 91, 125, 133, 117, 121])
# y = np.array([12.7, 34.7, 38.5, 46.6, 39.8, 47.5, 27.9, 33.1, 34.4, 27.8, 27.5, 34.7, 33.7])
labels = [
"0-shot", "5-shot", "Extra Parallel", "Extra + Wordlist", "Full Parallel", "Full + Wordlist", "Wordlist",
"Extra only", "Full book", "Book non-parallel", "Book non-parallel/pairs", "Book parallel+pairs", "Book parallel"
]

plt.scatter(x, y)
for i, label in enumerate(labels):
    plt.annotate(label, (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Display the plot
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Scatter Plot with Labels')
plt.show()