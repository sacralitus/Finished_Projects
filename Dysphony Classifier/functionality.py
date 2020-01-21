import glob
import numpy as np
import pandas as pd
import parselmouth
import os, re
from parselmouth.praat import call
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pickle


def measurePitch(voiceID, f0min, f0max, unit):
    sound = parselmouth.Sound(voiceID)  # read the sound
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max)  # create a praat pitch object
    meanF0 = call(pitch, "Get mean", 0, 0, unit)  # get mean pitch
    stdevF0 = call(pitch, "Get standard deviation", 0, 0, unit)  # get standard deviation
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    ddpJitter = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer = call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    aqpq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq11Shimmer = call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    ddaShimmer = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

    return meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer

def runPCA(df):
    #Z-score the Jitter and Shimmer measurements
    features = ['localJitter', 'localabsoluteJitter', 'rapJitter', 'ppq5Jitter', 'ddpJitter',
                'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer', 'apq11Shimmer', 'ddaShimmer']
    # Separating out the features
    x = df.loc[:, features].values
    # Separating out the target
    y = df.loc[:,['target']].values
    # Standardizing the features
    x = StandardScaler().fit_transform(x)
    #PCA
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(x)
    principalDf = pd.DataFrame(data = principalComponents, columns = ['JitterPCA', 'ShimmerPCA'])

    return principalDf

def classify(wave_file, clf_name):
    global mean_F0_list,sd_F0_list,hnr_list,localJitter_list,ppq5Jitter_list,localShimmer_list,apq11Shimmer_list

    mean_F0_list,sd_F0_list,hnr_list,localJitter_list,ppq5Jitter_list,localShimmer_list,apq11Shimmer_list = [],[],[],[],[],[],[]

    sound = parselmouth.Sound(wave_file)

    (meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer) = measurePitch(sound, 75, 500, "Hertz")

    mean_F0_list.append(meanF0)
    sd_F0_list.append(stdevF0)
    hnr_list.append(hnr)
    localJitter_list.append(localJitter)
    ppq5Jitter_list.append(ppq5Jitter)
    localShimmer_list.append(localShimmer)
    apq11Shimmer_list.append(apq11Shimmer)
    df = pd.DataFrame(np.column_stack([mean_F0_list, sd_F0_list, hnr_list, localJitter_list, ppq5Jitter_list, localShimmer_list, apq11Shimmer_list]),
                               columns=['meanF0Hz', 'stdevF0Hz', 'HNR', 'localJitter','ppq5Jitter','localShimmer','apq11Shimmer'])
    arr = df.values

    clf = pickle.load(open(f'{clf_name}_model.sav','rb'))
    return "\nDysphonic probability: {} %".format(round(clf.predict_proba(arr)[0,1],2)*100)