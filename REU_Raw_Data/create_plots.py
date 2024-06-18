import numpy as np
import matplotlib.pyplot as plt
from os import listdir #standard library
from os.path import isfile, join


def make_plot(rp_file, b_file, name):
    print("rp_file is", rp_file)
    print("b_file is", b_file)  
    with open(rp_file) as f:
        lines = f.readlines()

    with open(b_file) as fb:
        lines_b = fb.readlines()

    rp_wavelength = []
    rp_intensity = []

    # lines 319 to 2441 is the range of wavelengths from 350 to 750
    max_intensity = 0
    #for n in range(319, 2441):
    for n in range(319, 2441):
        # i = '294.396000\t0.000000\n'
        w, i = lines[n].split('\t')
        i_b = lines_b[n].split('\t')[1]
        w = float(w)
        # i = float(i[:-1])
        i = float(i[:-1]) - float(i_b[:-1])
        rp_wavelength.append(w)
        rp_intensity.append(i)
        max_intensity = max(max_intensity, i)


    # Make first Graph
    plt.figure(figsize=(20,2))
    fig, ax = plt.subplots()             # Create a figure containing a single Axes.

    ax.plot(np.asarray(rp_wavelength), np.asarray(rp_intensity), label=name, color='orange')  # Plot some data on the Axes.

    ax.set_title('RP_14')
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('Intensity (mW/nm)')
    ax.axis([350, 750, -10, 100])
    ax.legend()
    # for normalized graph
    # ax.axis([350, 750, 0, 1])

    plt.savefig(name + '.png', dpi=400)


    # NORMALIZED GRAPH
    rp_intensity_normalized = [x/max_intensity for x in rp_intensity]

    fig_n, ax_n = plt.subplots()             # Create a figure containing a single Axes.
    ax_n.plot(np.asarray(rp_wavelength), np.asarray(rp_intensity_normalized), label=name, color='blue')  # Plot some data on the Axes.

    ax_n.set_title('RP_14' + '_N')
    ax_n.set_xlabel('Wavelength (nm)')
    ax_n.set_ylabel('Intensity (mW/nm)')
    ax_n.axis([350, 750, 0, 1])
    ax_n.legend()
    # for normalized graph
    plt.savefig(name + '_n.png', dpi=400)


def get_all_files():
    rp_files = []
    b_files = []
    allFiles = [f for f in listdir('./') if isfile(join('./', f))]
    sortedFiles = sorted(allFiles)

    # since it is sorted all of the bs will be added by the time we get to the rps or ws
    for f in sortedFiles:
        out = f.split("_")
        if len(out) == 3: #it is a b
            type, et, date = out
            if type == "b" and date == "617":
                b_files.append(f)

        elif len(out) == 4: #it is an rp
            type, num, et, redo = out
            if (type == "rp" or type == "w") and int(num) >= 14 and redo == "redo":
                rp_files.append(f)
            b_file = "b_" + et + "et_617"
            # call function
            # make_plot(out, b_file, "RP_" + num)
        
        elif len(out) == 5: #it is an rp
            type, num, et, real, redo = out
            if (type == "rp" or type == "w") and int(num) >= 14 and real == "real" and redo == "redo":
                rp_files.append(f)
            b_file = "b_" + et + "et_617"
            # call function
            # make_plot(out, b_file, "RP_" + num)

    print("b_files :", b_files)
    print("rp_files :", rp_files)

    # Make a dictionary:
    # for rp in rp_files:
    #     type, num, et, redo = rp
    #     b = b_files.find("b_" + et + "et_617")
        # call make_plot with rp and b


    # rp_file = "rp_14_275et_redo"
    # b_file = "rp_14_275et_redo"
    #takes parameter: rp_file and b_file


if __name__ == "__main__":
    make_plot("rp_14_275et_redo", "b_275et_617", "RP_14")
    # get_all_files()
