# intuitive-physics
Includes models/dataset/literature overview for question answering in physical scene understanding tasks.

## Definitions

- **Cohesion:** The principle states that objects are bounded and connected entities. They cannot split into pieces as they move (cohesion) or fuse with other objects (boundedness).

- **Continuity:** The principle states that objects exist and move continuously in time and space, they cannot appear and disappear whenever they want (continuity) and they cannot occupy the same space as other objects (solidity).

- **Persistence:** The principle states that while existing continuosly and remaining cohesive, objects also retain individual properties such as shape, color, size or pattern.

- **Pure Reasoning, one-shot intuition:** The ability to reason for a scene, an event or an action without previously experiencing the same specific situtaion.

- **Basic vs. Variable Violation:** Basic viloation is the one that only involves basic information to be detected whereas variable violation enforces one (possibly and infant) to identify variables such as shape, color and pattern which are relevant for predicting the outcomes of the event. For example, in an occlusion event, an infant may detect an object that gets lost behind a screen and get surprised, but s/he may not detect that object has been changed behind the screen if s/he does not include this variable information in her/his physical representation of event.

## Literature

This section includes literature overview for different methods developed for different intuitive physics tasks. You can filter these works by [year](#papers-by-year), [task](#papers-by-task), [dataset](#papers-by-dataset) or [conference or journal](#papers-by-conference-or-journal). [Read queue](#read-queue) is sort of a to do for this section and expected to be empty for most of the time.

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

#### Is This Stable?

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

It is one of the examples from pre deep learning era. It basically defines different scence states at different time steps. Method incorporates two different forces applied to the scene which are the initial force and the transition forces betweeen two time steps. There are observable information for both scenes and forces. Given observed information about these states and latent forces, the method uses Bayesian learning to estimate the posterior probabilities for physical scene understanding. The first problem that the method is trying to solve is "Will it fall?". When provided with an image of a tower, the model and the subjects are asked to decide whether the tower will fall or not. The second experiment is conducted on top of the first experiment to evaluate the performance of the model and the subject when asked the direction of the fall action. These experiments are also repeated by using object with different masses to evaluate the intuition that the mass brings. In the last experiment, the model and the subjects are compared according to their intuitions in case of an external force such as a bump to a table holding the objects.

#### Innate ideas revisited for a principle of persistence in infants’ physical reasoning

Innate ideas have extensively been argued in philosophy and cognitive science. The source of many arguments is to decide whether or not innate ideas have impact on infants' physical reasoning. Researchers or philosophers who think that these ideas do not have any effect on infant's development, states that reasoning is a capability that can be acquired only by experimenting. However, other side of the argument mainly accepts Spelke's two principles for innate capabilities which are continuity and cohesion. This paper claims that these two principles are actually corollaries of a single principle which is persistence.

### Read Queue

- [Innate Ideas Revisited For a Principle of Persistence in Infants’ Physical Reasoning](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3357323/pdf/nihms375132.pdf)

- [Pure Reasoning in 12-Month-Old Infants as Probabilistic Inference](http://web.mit.edu/cocosci/Papers/Science-2011-Teglas-1054-9.pdf)

- [Newtonian Image Understanding: Unfolding the Dynamics of Objects in Static Images](https://arxiv.org/pdf/1511.04048.pdf)

