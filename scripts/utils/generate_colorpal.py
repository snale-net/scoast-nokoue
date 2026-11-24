# MIT License
# Copyright (c) 2024 [SNALE - French SAS Company - RCS 951 724 616]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

if __name__ == "__main__":
    min = 0.2
    max = 2.1
    step = 0.1

    # Generate jet colorpal with max - min colors
    norm = colors.Normalize(vmin=min, vmax=max)
    cmap = plt.colormaps['jet']

    # Dict of value - color
    palette = {}

    for value in np.round(np.arange(min, max, step),2):
        r, g, b, a = cmap(norm(value))
        hexa = '#{:02X}{:02X}{:02X}'.format(
            round(r * 255),
            round(g * 255),
            round(b * 255)
        )
        palette[value] = hexa

    # Print the colorpal
    for value, color in palette.items():
        print(f"{value} : {color}")

