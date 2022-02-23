# Reinforcement Racer Project Challenges

---

This file is your **single-source-of-truth** for accessing relevant challenges and tasks required to complete the Reinforcement Racer project. 

Please read through this document exhaustively and make sure you have a fundamental understanding of the range and type of tasks you're required to complete for successful project completion. 

## PROGRESSIVE CHALLENGES

The first major benchmark of successful project performance is being able to run the project successfully and understand the basics of its architecture and hierarchy.

**Navigate to `project.py` and `structures/structures.py`: answer all relevant _TODOs_ to complete the first part of the project.**

## ANALYTIC CHALLENGES

Once you've successfully ran and interpreted your project once, you'll perform some additional challenges flexing both your working knowledge of reinforcement-learning-based artificial intelligence as well as your experience in software engineering and computer science. 

### OBJECTIVE 1: Configured Hyperparameter Optimization

Remember that odd little configuration file we have? The one named `config.txt`? 

This is your chance to get a better understanding of what the file is and how to manipulate it to improve your abilities in reinforcement learning.

Navigate to the `config.txt` file and perform **at least five** different hyperparameter tunings, changing up discretized values within reason. 

Be sure to make use of official NEAT documentation for what type of hyperparameters and information is embedded within the file, [as provided via this link](https://neat-python.readthedocs.io/en/latest/config_file.html).

Finally, create a new subdirectory in your project directory called `tuning/`; after running _at least twenty (20) generations_ for each of your tuned hyperparameter cases, save the final accuracy report (as produced by your terminal) as an image within the `tuning/` folder.

If all is done correctly, you should be left with a new subdirectory called `tuning/` that contains at least five (5) new screenshotted images on your hyperparameter optimization task.

### OBJECTIVE 2: Complicating Racetracks

The nice thing about how we've structured the environments across our reinforcement learning scenario is that the environment spaces themselves are pretty seamless to replicate.

Let's try and evaluate how our reinforced racer would fare with custom-designed racetracks!

Open up any basic artistic drawing tool (e.g. Microsoft Paint, Paintbrush) and create a new racetrack, ensuring the color choices and appropriate design architecture is conceptually similar to the provided default maps (`map01.png`, `map02.png`, `map03.png`). 

Once you've created a satisfactory test map, go ahead and save it to your `environments/` subdirectory and update your project code to allow for training across the newly designed map.

After _at least (20)_ generations of training, save the final accuracy report (as produced by your terminal) as a screenshot – save the screenshotted custom map accuracy report to your project directory (ideally in the outermost level, adjacent to `project.py`).