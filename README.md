# intuitive-physics
Includes models/dataset/literature overview for question answering in physical scene understanding tasks.

## literature

### papers by year

#### 2019

- [Reasoning about physical interactions with object oriented prediction and planning](#reasoning-about-physical-interactions-with-object-oriented-prediction-and-planning)

#### 2018

#### 2017

#### 2013

- [Simulation as an engine of physical scene understanding](#simulation-as-an-engine-of-physical-scene-understanding)

### papers by task

### papers by datasets

### papers by conference/journal

### references

#### Reasoning about physical interactions with object oriented prediction and planning

The main problem which is tried to be solved is to learn object representations to plan actions for pyhsical scene understanding without using object representations as explicit supervisions. The training is done by dropping objects to a scene containing at most four objects and trying to predict the steady state image while learning physical relations between objects. Extractor model for these object representations can then be used, for example, for building a tower from scratch. Object representation labels are difficult to obtain and therefore methods using them are not scalable. Instead of directly using them, method uses segmentation map estimates of each object in an image to train an object representation extractor. This model is jointly trained with physical scene understanding model and pixel level frame prediction model.

#### Simulation as an engine of physical scene understanding

### read queue


