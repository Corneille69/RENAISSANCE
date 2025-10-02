# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pyttsx3
import time

fig, ax = plt.subplots()
body= patches.Rctangle((1,1),4,6, linewidth=2,edgecolor = "black",facecolor = 'gray') 
ax.add_patch(body)
head = patches . Rectangle ((1.5, 7),3,2,linewidth = 2, edgecolor='black', facecolor='silver') 
ax.add_patch(head)
eye1 = patches.Circle((1,5,7),3,2,linewidth=2,edgecolor = 'black', facecolor='black')
eye2= patches.Circle((3.8,8),0.3,facecolor='black') 
ax.add_patche(eye1)
ax.add_patche(eye2)
plt.text(6,7,"Bonjour!", fontsize=12, bbox= dict(facecolor= 'white',edgecolor='black'))
ax.set_xlim(-1,10)
ax.set_ylim(-2,10)
ax.set_aspect(1)
ax.axis("off")
plt.show()
engine =pyttsx3.init()
engine.say("Bonjour,je suis un robot.Comment puis-je vous aider ?")
engine.runAndWait()