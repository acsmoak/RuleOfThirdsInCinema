# RuleOfThirdsInCinema
This tool determines how closely an image follows the rule of thirds assuming a human face is the focal point. 


Aesthetic images evoke an emotional response that transcends mere visual appreciation. 
In this work we develop a computational means for evaluating the composition aesthetics 
of a given image based on measuring one of the most well-grounded composition guidelines—the rule of thirds [Figure 1]. 
We propose analyzing samples of frames from works by Alfred Hitchcock and Wes Anderson, 
with the goal to objectively and computationally prove the subjective observation that Hitchcock 
tends to follow the rule of thirds, while Anderson breaks it. We will first use a face detection API 
based upon OpenCV and Python. We will then create a program to iterate through many frames within a single 
film—specifically Alfred Hitchcock’s Psycho—that will locate the actor’s face, store the center focal point 
of the face, and compute the distance from both the vertical third lines and the horizontal third lines. 
These calculations will then be used to compare how closely Anderson and Hitchcock's compositions follow the rule of thirds.
