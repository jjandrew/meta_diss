import matplotlib.pyplot as plt

if __name__ == "__main__":
    sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    aco_time = [5.816179323196411, 15.39100685119629, 30.004591464996338, 48.752499389648435, 67.56675248146057,
                94.85416975021363, 133.77529129981994, 167.1307382106781, 208.88485946655274, 249.86360750198364]

    ga_time = [7.235821056365967, 14.177123928070069, 23.9303026676178, 34.58152670860291, 46.26217265129089,
               64.14483547210693, 83.72838521003723, 101.45285158157348, 122.98123760223389, 145.62766394615173]

    sa_time = [1.545849370956421, 2.4534868717193605, 3.6972556114196777, 4.864213466644287, 5.417836999893188,
               7.373422145843506, 9.607509756088257, 11.473828506469726, 12.991342306137085, 14.747153902053833]
    # # Divide each value by its corresponding size
    # aco_best_qual = [val/size for val, size in zip(aco_best_qual, sizes)]
    # ga_best_qual = [val/size for val, size in zip(ga_best_qual, sizes)]
    # sa_best_qual = [val/size for val, size in zip(sa_best_qual, sizes)]
    # rs_best_qual = [val/size for val, size in zip(rs_best_qual, sizes)]

    plt.plot(sizes, aco_time, label='ACO')
    plt.plot(sizes, ga_time, label='GA')
    plt.plot(sizes, sa_time, label='SA')
    # plt.plot(sizes, rs_time, label='Random Search')

    # Adding labels and title
    plt.xlabel('No. of Depots')
    plt.ylabel('Time (s)')

    # Adding a legend
    plt.legend()

    # Displaying the plot
    plt.show()
