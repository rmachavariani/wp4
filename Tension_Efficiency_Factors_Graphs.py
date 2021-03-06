"""Tension Efficiency Factors Graphs"""

# 1.12
curve_121 = [[1, 1], [1.5, 0.99], [2, 0.98], [2.5, 0.94], [3, 0.92], [3.5, 0.92], [4, 0.9], [4.5, 0.85], [5, 0.76]]  # curve 1
curve_123 = [[1, 1], [1.5, 0.98], [2, 0.94], [2.5, 0.9], [3, 0.88], [3.5, 0.84], [4, 0.82], [4.5, 0.78], [5, 0.74]]  # curve 2
curve_124 = [[1, 1], [1.5, 0.96], [2, 0.9], [2.5, 0.84], [3, 0.8], [3.5, 0.78], [4, 0.76], [4.5, 0.72], [5, 0.68]]  # curve 3

graph_12 = [curve_121, curve_123, curve_124]

# 1.15
curve_151 = [[0, 0], [0.1, 0.1], [0.2, 0.28], [0.3, 0.42], [0.4, 0.55], [0.5, 0.68], [0.6, 0.8], [0.7, 0.92], [0.8, 1.15], [0.9, 1.18], [1, 1.26], [1.1, 1.38], [1.2, 1.48],
             [1.3, 1.58], [1.4, 1.66]]
curve_152 = [[0, 0], [0.1, 0.1], [0.2, 0.28], [0.3, 0.42], [0.4, 0.55], [0.5, 0.68], [0.6, 0.8], [0.7, 0.92], [0.8, 1.15], [0.9, 1.18], [1, 1.26], [1.1, 1.38], [1.2, 1.48],
             [1.3, 1.55], [1.4, 1.55]]
curve_153 = [[0, 0], [0.1, 0.1], [0.2, 0.26], [0.3, 0.38], [0.4, 0.5], [0.5, 0.62], [0.6, 0.72], [0.7, 0.8], [0.8, 0.9], [0.9, 0.98], [1, 1.04], [1.1, 1.1], [1.2, 1.18],
             [1.3, 1.22], [1.4, 1.28]]
curve_158 = [[0, 0], [0.1, 0.1], [0.2, 0.26], [0.3, 0.38], [0.4, 0.5], [0.5, 0.58], [0.6, 0.6], [0.7, 0.62], [0.8, 0.64], [0.9, 0.75], [1, 0.78], [1.1, 0.78], [1.2, 0.78],
             [1.3, 0.78], [1.4, 0.78]]
curve_159 = [[0, 0], [0.1, 0.1], [0.2, 0.24], [0.3, 0.32], [0.4, 0.38], [0.5, 0.44], [0.6, 0.48], [0.7, 0.52], [0.8, 0.58], [0.9, 0.58], [1, 0.6], [1.1, 1.62], [1.2, 1.62],
             [1.3, 1.62], [1.4, 1.62]]
curve_1511 = [[0, 0], [0.1, 0.1], [0.2, 0.36], [0.3, 0.34], [0.4, 0.4], [0.5, 0.44], [0.6, 0.45], [0.7, 0.48], [0.8, 0.5], [0.9, 0.5], [1, 0.5], [1.1, 0.5], [1.2, 0.5], [1.3, 0.5],
              [1.4, 0.5]]

graph_15 = [curve_151, curve_152, curve_153, curve_158, curve_159, curve_1511]


def tension_eff_graph(fig, index, x_input):  # index material to be found in the excel file, linking each materials to the above curves, see comments after each curve
    graph_picked = None

    if fig == 12:
        graph_picked = graph_12

    elif fig == 15:
        graph_picked = graph_15

    n = int(index) - 1

    if graph_picked is not None:
        try:
            curve_picked = graph_picked[n]

            if curve_picked[-1][0] > x_input:
                for j, i in enumerate(curve_picked):

                    if j == len(curve_picked) - 1:
                        break

                    if i[0] <= x_input <= curve_picked[curve_picked.index(i) + 1][0]:
                        x1 = i[0]
                        x2 = curve_picked[curve_picked.index(i) + 1][0]

                        y1 = i[1]
                        y2 = curve_picked[curve_picked.index(i) + 1][1]
                        # print(y1,y2)

                        k = (x_input - x1) / (x2 - x1)
                        # print(k)

                        output = (1 - k) * y1 + k * y2

                        return output

        except IndexError:
            print(f"Wrong curve selected; curve {n} with graph {fig}")

    else:
        print(f"Wrong figure index provided in Tension_efficiency_Factors; figure {fig}, index {index}, x_input {x_input}")


# tension_eff_graph(12, 3, 2.2)
# print(tension_eff_graph(12, 4, 0.32))
