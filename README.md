# NKOAPP
An application written in Python and making use of open source programs such as [Praat](https://github.com/praat/praat) for sound analysis and the synthesis backend of [VocalTractLab](https://github.com/TUD-STKS/VocalTractLab-dev) to allow for an advanced control of the vocal tract shapes and glottis properties over time.
The initial goals for this system were to allow for producing 'natural' and 'unnatural' sounding vocalizations and articulations, interpolations between mouth and glottis configurations in order to allow for continuous parameter changes of invariants (physical properties) and variants(f0, intensity, filtering coefficients) to go from one ‘speaker identity’ to another. Furthermore, using features from actual voice recordings then became an important way of using the system. Using variant parameters such as f0 & loudness to address prosodic, intonation and jitter and shimmer patterns in the voice recordings.

In broad terms the synthesis procedure follows the **source-filter paradigm**, where the vocal fold vibration serves as the excitation of the filter. The vocal tract then serves as the filtering of the glottal pulses.

---

## How to use NKOAPP?
1. First of all download the latest version of the [Praat](https://github.com/praat/praat) and [VocalTractLab](https://github.com/TUD-STKS/VocalTractLab-dev) software. 
2. Then fork this repository locally on your computer.
3. If you want to use f0 and intensity data from an audio recording, then follow the following steps:
    - Open `Praat`> _Open_ > _Read from file..._ and select the audio file you'd like to analyze
    - Then select this sound in the _Object box_, go to the toolbar option _Praat_ > _Open Praat script..._
    - Navigate to the folder in directory `NKOAPP\Praat Scripts\` and choose the `f0_intensity.txt` file. Then click on _Run_ in the script popup window.
    - Wait a bit for the script to finish, then save the file as a txt-file with an arbitrary name in the folder `NKOAPP\f0andIntensity`. For example as `f0andIntVoxAdam.txt`
    - done for now. Continue to 4
4. Open `NKOAPP.py` file and the `VocalTractLab2` software
  - First of all you have to choose the glottis model `glChoice = glGeomOptions['GM']` with three choices `'GM'`, `'2M'` or `'TRI'`.
    - Choose the same glottis model as `glChoice` (see above): _Synthesis models_ > _Vocal folds model_ > Choose one of the three > then click on _Use selected model for synthesis_
  - If you want to use the f0 and intensity data from the recording, you should add the filename in this part of the code `f0andIntFileName = directory + '/f0andIntensity/**filename.txt**'`
  - If we want to manually generate the tractSequence or use the f0 and intensity values from the praat script
    - `manual = True` _go to Section A in the code_
    - `manual = False` _go to Section B in the code_
5. Two ways of working with NKOAPP are either through manual input of glottis parameters, vocal tract shapes and durations of the interpolations between _sources_ and _targets_ 
#### SECTION A
  - **Option A1** for glottis and tract targets (glOption,trOption) and the durations between them
  - **Option A2** to generate random interpolations between a set of chosen glottis and tract targets (glOption, trOption) and random durations
  - Follow the comments in the code. Don't forget to comment out the parts you don't need when working in another section and another Option

#### SECTION B
  - same as above, but now the amount of frames in the tractSequence-file amount to the same duration as the audio file. This can not be changed.

6. Change the durations between targets by proportioning the segments in different ways
  - make the durations get shorter and shorter starting from the longest part: `durModulationG = arithmetic_progression(1,valT)[::1]` or the interpolations get longer and longer starting from the shortest part: `durModulationG = arithmetic_progression(1,valT)[::-1]`
  - change the exponent of the durations
7. Take the time discrete derivative of the splines. The splines are cubic polynomials, so the maximum derivative is `2`. So, three options are available for both the glottis and tract interpolations in `derivativeGlot` and `derivativeTract`. This is still in its experimental state, use at own risk.
    - [0,1,2]: 0=no deriv, 1=1st deriv, 2=2nd deriv
8. Choose the upper and lower boundary for random uniform number generation as a factor to randomize the glottis parameters (f0, Intensity, Jaw Height, Tongue Heigh, etc...)

---
Now build the NKOAPP.py file
- After building, there should be a tractSequence file in the `\TractSequence` folder that should look something like this `2024-05-13_02-50-43_TractSequence_ConstPressureAndf0_Geometric glottis_n9_normalDist[1, 1]_[0, 0]_Manual.txt`
- Go to `VocalTractLab2` and navigate to _Synthesis from file_ > _Tract sequence file to audio_. Then find the tractSequence file in the beforementioned folder and select it.
- This can take long if the tractSequence file is more than 10s. Ignore the `"The Program is not responding"`, it's just rendering. 

<ins>**by Lawrence McGuire**</ins>
    
