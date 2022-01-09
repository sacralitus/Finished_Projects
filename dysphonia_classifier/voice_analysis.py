from functionality import measurePitch
import os, re
import glob
import parselmouth
import pandas as pd
import numpy as np
from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string('mypath', 'Анализ голоса/Pathology/', 'path to voices directory', short_name = 'p')

def main(argv):
    # create lists to put the results
    file_list = []
    mean_F0_list = []
    sd_F0_list = []
    hnr_list = []
    localJitter_list = []
    #localabsoluteJitter_list = []
    #rapJitter_list = []
    ppq5Jitter_list = []
    #ddpJitter_list = []
    localShimmer_list = []
    #localdbShimmer_list = []
    #apq3Shimmer_list = []
    #aqpq5Shimmer_list = []
    apq11Shimmer_list = []
    #ddaShimmer_list = []

    print("Path:", FLAGS.mypath)

    # Go through all the wave files in the folder and measure pitch
    for root,dirs,files in os.walk(FLAGS.mypath):
        for name in dirs:
            for wave_file in glob.glob("{}/*.wav".format(os.path.join(root, name))):
                sound = parselmouth.Sound(wave_file)
                (meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer) = measurePitch(sound, 75, 500, "Hertz")
                file_list.append((re.findall(r'(\w+).wav',wave_file)[0])) # make an ID list
                mean_F0_list.append(meanF0) # make a mean F0 list
                sd_F0_list.append(stdevF0) # make a sd F0 list
                hnr_list.append(hnr)
                localJitter_list.append(localJitter)
                #localabsoluteJitter_list.append(localabsoluteJitter)
                #rapJitter_list.append(rapJitter)
                ppq5Jitter_list.append(ppq5Jitter)
                #ddpJitter_list.append(ddpJitter)
                localShimmer_list.append(localShimmer)
                #localdbShimmer_list.append(localdbShimmer)
                #apq3Shimmer_list.append(apq3Shimmer)
                #aqpq5Shimmer_list.append(aqpq5Shimmer)
                apq11Shimmer_list.append(apq11Shimmer)
                #ddaShimmer_list.append(ddaShimmer)


    df = pd.DataFrame(np.column_stack([file_list, mean_F0_list, sd_F0_list, hnr_list, localJitter_list, ppq5Jitter_list, localShimmer_list, apq11Shimmer_list]),
                                   columns=['voiceID', 'meanF0Hz', 'stdevF0Hz', 'HNR', 'localJitter','ppq5Jitter','localShimmer','apq11Shimmer'])  #add these lists to pandas in the right order

    # Write out the updated dataframe
    #df.to_csv("norm_results_delete.csv", index=False)

    print("All samples:",len(file_list))
    print("Female samples:", len([i for i in file_list if 'f' in i]))
    print("Male samples:", len([i for i in file_list if 'm' in i]))
    print("Sound i samples:", len([i for i in file_list if 'i' in i]))
    print("Sound a samples:", len([i for i in file_list if 'a' in i]))
    print("Children voices samples:", len([i for i in file_list if 'l' in i]))

if __name__ == "__main__":
    app.run(main)