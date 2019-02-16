# intuitive-physics
Includes models/dataset/literature overview for question answering in physical scene understanding tasks.

## Literature

This section includes literature overview for different methods developed for different intiutive physics task. You can filter these works by [year](#papers-by-year), [task](#papers-by-task), [dataset](#papers-by-dataset) or [conference or journal](#papers-by-conference-or-journal). [Read queue](#read-queue) is sort of a to do for this section and expected to be empty for most of the time.

### Papers by Year

#### 2019

- [Reasoning about physical interactions with object oriented prediction and planning](#reasoning-about-physical-interactions-with-object-oriented-prediction-and-planning)

#### 2018

#### 2017

#### 2013

- [Simulation as an engine of physical scene understanding](#simulation-as-an-engine-of-physical-scene-understanding)

### Papers by Task

#### Next Frame Prediction

##### Object Dropped to a Scene

- [Reasoning about physical interactions with object oriented prediction and planning](#reasoning-about-physical-interactions-with-object-oriented-prediction-and-planning)

##### Is this stable?

- [Simulation as an engine of physical scene understanding](#simulation-as-an-engine-of-physical-scene-understanding)

#### Planning Physical Actions

##### Building Towers

- [Reasoning about physical interactions with object oriented prediction and planning](#reasoning-about-physical-interactions-with-object-oriented-prediction-and-planning)

### Papers by Dataset

#### Custom (either not being available or used extensively)

- [Reasoning about physical interactions with object oriented prediction and planning](#reasoning-about-physical-interactions-with-object-oriented-prediction-and-planning)

### Papers by Conference or Journal

#### ICLR

- [Reasoning about physical interactions with object oriented prediction and planning](#reasoning-about-physical-interactions-with-object-oriented-prediction-and-planning)

#### PNAS

- [Simulation as an engine of physical scene understanding](#simulation-as-an-engine-of-physical-scene-understanding)

### References

#### Reasoning about physical interactions with object oriented prediction and planning

The main problem which is tried to be solved is to learn object representations to plan actions for pyhsical scene understanding without using object representations as explicit supervisions. The training is done by dropping objects to a scene containing at most four objects and trying to predict the steady state image while learning physical relations between objects. Extractor model for these object representations can then be used, for example, for building a tower from scratch. Object representation labels are difficult to obtain and therefore methods using them are not scalable. Instead of directly using them, method uses segmentation map estimates of each object in an image to train an object representation extractor. This model is jointly trained with physical scene understanding model and pixel level frame prediction model.

#### Simulation as an engine of physical scene understanding

It is one of the examples from pre deep learning era. It basically defines different scence states at different time steps. Method incorporates two different forces applied to the scene which are the initial force and the transition forces betweeen two time steps. There are observable information for both scenes and forces. Given observed information about these states and latent forces, the method uses Bayesian learning to estimate the posterior probabilities for physical scene understanding. The first problem that the method is trying to solve is "Will it fall?". When provided with an image of a tower, the model and the subjects are asked to decide whether the tower will fall or not. 

### Read Queue


