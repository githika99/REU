import numpy as np
import matplotlib.pyplot as plt
from os import listdir #standard library
from os.path import isfile, join


def make_individual_plots(rp_file, b_file, name):
    print("in make_individual_plots")
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
    for n in range(319, 2441):
        w, i = lines[n].split('\t')
        i_b = lines_b[n].split('\t')[1]
        w = float(w)
        i = float(i[:-1]) - float(i_b[:-1])
        rp_wavelength.append(w)
        rp_intensity.append(i)
        max_intensity = max(max_intensity, i)


    # Make first Graph
    plt.figure(figsize=(10,8))

    plt.plot(np.asarray(rp_wavelength), np.asarray(rp_intensity), label=name, color='orange', linewidth = '.7')  # Plot some data on the Axes.

    plt.title('RP_14')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity (mW/nm)')
    plt.axis([350, 750, -10, 100])
    plt.legend()

    plt.savefig("/Users/githika/GitHub/REU/REU_Raw_Data/Graphs_617/" + name + '.png', dpi=400)
    plt.close()

    # NORMALIZED GRAPH
    rp_intensity_normalized = [x/max_intensity for x in rp_intensity]
    plt.figure(figsize=(10,8))
    plt.plot(np.asarray(rp_wavelength), np.asarray(rp_intensity_normalized), label=name, color='blue', linewidth = '.7')  # Plot some data on the Axes.

    plt.title('RP_14' + '_N')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity (mW/nm)')
    plt.axis([350, 750, 0, 1])
    plt.legend()
    # for normalized graph
    plt.savefig("/Users/githika/GitHub/REU/REU_Raw_Data/Graphs_617/" + name + '_n.png', dpi=400)
    plt.close()


# dic is a dictionary with keys being file names of rps and values being file names of background readings 
def make_one_plot(dic, start, end):
    print("entered make_one_plot")
    plt.figure(figsize=(10,8))

    for rp_file in dic:
        print("going through dic with rp_file", rp_file)
        b_file = dic[rp_file]
        with open(rp_file) as f:
            lines = f.readlines()

        with open(b_file) as fb:
            lines_b = fb.readlines()

        rp_wavelength = []
        rp_intensity = []
        num = rp_file.split("_")[1]

        # lines 319 to 2441 is the range of wavelengths from 350 to 750
        max_intensity = 0
        for n in range(319, 2441):
            w, i = lines[n].split('\t')
            i_b = lines_b[n].split('\t')[1]
            w = float(w)
            i = float(i[:-1]) - float(i_b[:-1])
            rp_wavelength.append(w)
            rp_intensity.append(i)
            max_intensity = max(max_intensity, i)
        
        plt.plot(np.asarray(rp_wavelength), np.asarray(rp_intensity), label="RP_"+num, linewidth = '.7')  # Plot some data on the Axes.
    
    plt.title('All Values')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity (mW/nm)')
    plt.axis([350, 750, -10, 100])
    plt.legend()
    plt.savefig("/Users/githika/GitHub/REU/REU_Raw_Data/Graphs_617/" + 'All_Values.png', dpi=400)
    plt.close()




def get_all_files():
    print("in get_all_files")
    rp_files = []
    b_files = []
    allFiles = [f for f in listdir('./') if isfile(join('./', f))]
    sortedFiles = sorted(allFiles)
    dic = {}
    # since it is sorted all of the b's will be added by the time we get to the rp's or w's
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
                b_file = "b_" + et + "_617"
                dic[f] = b_file
                # call function
                make_individual_plots(f, b_file, "RP_" + num)
        
        elif len(out) == 5: #it is an rp
            type, num, et, real, redo = out
            if (type == "rp" or type == "w") and int(num) >= 14 and real == "real" and redo == "redo":
                rp_files.append(f)
                b_file = "b_" + et + "_617"
                dic[f] = b_file
                # call function
                make_individual_plots(f, b_file, "RP_" + num)

    print("b_files :", b_files)
    print("rp_files :", rp_files)
    make_one_plot(dic, 0, 100)


if __name__ == "__main__":
    # rp_file = "rp_14_275et_redo"
    # b_file = "rp_14_275et_redo"
    # make_individual_plots("rp_14_275et_redo", "b_275et_617", "RP_14")
    get_all_files()
    # make_one_plot({"rp_14_275et_redo": "b_275et_617", "rp_15_500et_real_redo": "b_500et_617"}, 0, 100)
