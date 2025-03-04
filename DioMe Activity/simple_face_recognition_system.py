# -*- coding: utf-8 -*-
"""Simple_Face_Recognition_System.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14vdQQ8E7ZzIbMae_MaPPiHNctQkx2Prh

Ran on Colab

## **References with links**

This notebook is based on Retina Face tutorial available at this [Git](https://github.com/caiochf/retinaface).

Some arguments and informations were also obtained from [deepFace](https://github.com/serengil/deepface).

---

# Introduction

This notebook aims to deploy a face detection and recognition. For that, RetinaFace and deepFace will be used to recognize a "visitor" at the White House.

---
## **First set up:**
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
from PIL import Image
import numpy as np

# Just to make things look a little better:
from tqdm import tqdm

"""## **Here we have the list of people who are allowed there.**
This images can be obtained in the "database" folder.
"""

database = '/content/database'
files = os.listdir(database)

print(files)

"""We can see that three people are allowed there. This quantity was chosen in order to allow a faster execution and recognition.

---

## **Second set up:**

If you don't have them, it will be necessary to install RetinaFace and deepFace for this notebook to work. This can be done via pip:
"""

!pip install retina-face
!pip install deepface

"""Afte installing, lets import them:"""

from retinaface import RetinaFace
from deepface import DeepFace

"""---

## Now, we have our visitor!

This man approached a guard and wanted to enter in the White House in order to show it to his son Bjorn:
"""

visitor = '/content/ragnar2.jpg'

visit = np.array(Image.open(visitor))

plt.imshow(visit)
plt.title("Visitors picture")
plt.show()

"""Despite not being properly dressed for the ocasion and not looking directly to the camer, we can see that his face is cleary shown at the photo. Lets try to deploy the system to recognize him.

First of all, lets extract his face (some kind of "detection"):
"""

face = RetinaFace.extract_faces(visitor)

for visitor_photo in face:
  plt.imshow(visitor_photo)
  plt.title('This is the visitors face')
  plt.show()

"""His face was extracted successfully! All features (eyes, mouth, nose, chick, forehead...) are visible. We can proceed.

---

## **Recognition**

Now our visitor will be submited to the facial recognition. Note that even with the "True" ou "Valid" output from our system, a human validation will be necessary in the end.

Every system has its probabilities of errors:



> "*Notice that ArcFace got 99.40% accuracy on LFW data set whereas human beings just have 97.53% confidence.*" (RetinaFace GitHub)



 Since we are talking about the White House, no mistakes can be done here. After finding the best match, if available, the guard must validate the recognition.

Here a function will be defined to verify if there is a match between the input photo (visitor) and the dataset available.

Note: There is a specific fucntion available for face recognition in a dataset. It is the DeepFace.find(). It is not used here because we wanted to do it by ourselves.
"""

def verify(img1, database):
    checks = pd.DataFrame({'Image': [], 'Match': []})

    for img2 in tqdm(files, desc="Verifying...", unit="img"):
        img2_path = os.path.join(database, img2)
        verification = DeepFace.verify(img1, img2_path, align=True)
        checks.loc[len(checks)] = [img2_path, verification['verified']]

    matches =  checks[checks["Match"] == True]["Image"]

    if matches.empty:
        print("No matches found!")
        return

    matches = matches.iloc[0]
    image1 = Image.open(img1)
    array1 = np.array(image1)

    image2 = Image.open(matches)
    array2 = np.array(image2)

    fig, axes = plt.subplots(1, 2, figsize=(8, 8))

    axes[0].imshow(array1)
    axes[0].set_title('Input face')
    axes[1].imshow(array2)
    axes[1].set_title('Best correspondence')


    plt.tight_layout()
    return plt.draw()

"""---

## The moment of truth:

Now, lets see if our visitor is allowed to enter.

After the recognition system output, it is still necessary to validate throught a "Y" (Yes) or "N" (No) input.
"""

verify(visitor, database)
plt.pause(2)

allow = input('Allow? [Y]es or [N]o ')

while allow not in ['Y', 'N']:
    allow = input('\n Please, choose between "Y" for Yes or "N" for No ')

if allow == 'Y':
  print('\n Welcome to the White House!')
elif allow == 'N':
  print('\n You are not allowed here! Take Bjorn and go back home!')

"""Done!"""

