# intuitive-physics
Includes models/dataset/literature overview for question answering in physical scene understanding tasks.

## Simulator

### 2d

Folder **2d** contains box2d executables to render simulations in 2-dimensional environments. [SVQA-Box2D](https://github.com/cagatayyigit/SVQA-Box2D) contains an extension to famous 2D physics engine Box2D.

## Definitions

- **Cohesion:** The principle states that objects are bounded and connected entities. They cannot split into pieces as they move (cohesion) or fuse with other objects (boundedness).

- **Continuity:** The principle states that objects exist and move continuously in time and space, they cannot appear and disappear whenever they want (continuity) and they cannot occupy the same space as other objects (solidity).

- **Persistence:** The principle states that while existing continuosly and remaining cohesive, objects also retain individual properties such as shape, color, size or pattern.

- **Pure Reasoning, one-shot intuition:** The ability to reason for a scene, an event or an action without previously experiencing the same specific situtaion.

- **Basic vs. Variable Violation:** Basic violation is the one that only involves basic information to be detected whereas variable violation enforces one (possibly and infant) to identify variables such as shape, color and pattern which are relevant for predicting the outcomes of the event. For example, in an occlusion event, an infant may detect an object that gets lost behind a screen and get surprised, but s/he may not detect that object has been changed behind the screen if s/he does not include this variable information in her/his physical representation of event.

## Literature

This section includes literature overview for different methods developed for different intuitive physics tasks. You can filter these works by [area](#papers-by-area), [year](#papers-by-year), [task](#papers-by-task), [dataset](#papers-by-dataset) or [conference or journal](#papers-by-conference-or-journal). [Read queue](#read-queue) is sort of a to do for this section and expected to be empty for most of the time.

### Papers by Area

#### Computer Vision

- [Reasoning about physical interactions with object oriented prediction and planning](#reasoning-about-physical-interactions-with-object-oriented-prediction-and-planning)

- [Simulation as an engine of physical scene understanding](#simulation-as-an-engine-of-physical-scene-understanding)

- [Newtonian image understanding: unfolding the dynamics of objects in static images](#newtonian-image-understanding-unfolding-the-dynamics-of-objects-in-static-images)

- [Answering visual what-if questions: from actions to predicted scene descriptions](#answering-visual-what-if-questions-from-actions-to-predicted-scene-descriptions)

- [Learning particle dynamics for manipulating rigid bodies, deformable objects, and fluids](#learning-particle-dynamics-for-manipulating-rigid-bodies-deformable-objects-and-fluids)

- [Clevrer: collision events for video representation and reasoning](#clevrer-collision-events-for-video-representation-and-reasoning)

- [Forward prediction for physical reasoning](#forward-prediction-for-physical-reasoning)

#### Cognitive Science

- [Innate ideas revisited for a principle of persistence in infants’ physical reasoning](#innate-ideas-revisited-for-a-principle-of-persistence-in-infants-physical-reasoning)

- [Mind games: game engines as an architecture for intuitive physics](#mind-games-game-engines-as-an-architecture-for-intuitive-physics)

- [Causal reasoning with forces](#causal-reasoning-with-forces)

### Papers by Year

#### 2020

- [Forward prediction for physical reasoning](#forward-prediction-for-physical-reasoning)

#### 2019

- [Reasoning about physical interactions with object oriented prediction and planning](#reasoning-about-physical-interactions-with-object-oriented-prediction-and-planning)

- [Learning particle dynamics for manipulating rigid bodies, deformable objects, and fluids](#learning-particle-dynamics-for-manipulating-rigid-bodies-deformable-objects-and-fluids)

- [Clevrer: collision events for video representation and reasoning](#clevrer-collision-events-for-video-representation-and-reasoning)

#### 2018

- [Answering visual what-if questions: from actions to predicted scene descriptions](#answering-visual-what-if-questions-from-actions-to-predicted-scene-descriptions)

#### 2017

- [Mind games: game engines as an architecture for intuitive physics](#mind-games-game-engines-as-an-architecture-for-intuitive-physics)

#### 2016

- [Newtonian image understanding: unfolding the dynamics of objects in static images](#newtonian-image-understanding-unfolding-the-dynamics-of-objects-in-static-images)

#### 2015


- [Causal reasoning with forces](#causal-reasoning-with-forces)

#### 2013

- [Simulation as an engine of physical scene understanding](#simulation-as-an-engine-of-physical-scene-understanding)

#### 2011

- [Pure reasoning in 12-month-old infants as probabilistic inference](#pure-reasoning-in-12-month-old-infants-as-probabilistic-inference)

#### 2008

- [Innate ideas revisited for a principle of persistence in infants' physical reasoning](#innate-ideas-revisited-for-a-principle-of-persistence-in-infants-physical-reasoning)

### Papers by Task

#### Next Frame Prediction

- [Clevrer: collision events for video representation and reasoning](#clevrer-collision-events-for-video-representation-and-reasoning)

- [Forward prediction for physical reasoning](#forward-prediction-for-physical-reasoning)

##### Motion Estimation

- [Newtonian image understanding: unfolding the dynamics of objects in static images](#newtonian-image-understanding-unfolding-the-dynamics-of-objects-in-static-images)

- [Learning particle dynamics for manipulating rigid bodies, deformable objects, and fluids](#learning-particle-dynamics-for-manipulating-rigid-bodies-deformable-objects-and-fluids)

- [Clevrer: collision events for video representation and reasoning](#clevrer-collision-events-for-video-representation-and-reasoning)

##### Object Dropped to a Scene

- [Reasoning about physical interactions with object oriented prediction and planning](#reasoning-about-physical-interactions-with-object-oriented-prediction-and-planning)

##### What-if (Counterfactual)

- [Answering visual what-if questions: from actions to predicted scene descriptions](#answering-visual-what-if-questions-from-actions-to-predicted-scene-descriptions)

- [Clevrer: collision events for video representation and reasoning](#clevrer-collision-events-for-video-representation-and-reasoning)

#### Continuity and Change Violation Detection

- [Innate ideas revisited for a principle of persistence in infants’ physical reasoning](#innate-ideas-revisited-for-a-principle-of-persistence-in-infants-physical-reasoning)

- [Pure reasoning in 12-month-old infants as probabilistic inference](#pure-reasoning-in-12-month-old-infants-as-probabilistic-inference)

#### Is This Stable?

- [Simulation as an engine of physical scene understanding](#simulation-as-an-engine-of-physical-scene-understanding)

#### Planning Physical Actions

##### Building Towers

- [Reasoning about physical interactions with object oriented prediction and planning](#reasoning-about-physical-interactions-with-object-oriented-prediction-and-planning)

#### Causal Reasoning

- [Causal reasoning with forces](#causal-reasoning-with-forces)

### Papers by Dataset

#### Custom (either not being available or used extensively)

- [Reasoning about physical interactions with object oriented prediction and planning](#reasoning-about-physical-interactions-with-object-oriented-prediction-and-planning)

- [Learning particle dynamics for manipulating rigid bodies, deformable objects, and fluids](#learning-particle-dynamics-for-manipulating-rigid-bodies-deformable-objects-and-fluids)

#### Visual Newtonian Dynamics Dataset (VIND)

- [Newtonian image understanding: unfolding the dynamics of objects in static images](#newtonian-image-understanding-unfolding-the-dynamics-of-objects-in-static-images)

#### Table-top Interaction Visual What-If Questions Dataset (TIWIQ)

- [Answering visual what-if questions: from actions to predicted scene descriptions](#answering-visual-what-if-questions-from-actions-to-predicted-scene-descriptions)

#### Collision Events For Video Representation and Reasoning Dataset (CLEVRER)

- [Clevrer: collision events for video representation and reasoning](#clevrer-collision-events-for-video-representation-and-reasoning)

### Papers by Conference or Journal

#### ICLR

- [Reasoning about physical interactions with object oriented prediction and planning](#reasoning-about-physical-interactions-with-object-oriented-prediction-and-planning)

- [Learning particle dynamics for manipulating rigid bodies, deformable objects, and fluids](#learning-particle-dynamics-for-manipulating-rigid-bodies-deformable-objects-and-fluids)

- [Clevrer: collision events for video representation and reasoning](#clevrer-collision-events-for-video-representation-and-reasoning) (in review)

#### PNAS

- [Simulation as an engine of physical scene understanding](#simulation-as-an-engine-of-physical-scene-understanding)

#### PPS

- [Innate ideas revisited for a principle of persistence in infants’ physical reasoning](#innate-ideas-revisited-for-a-principle-of-persistence-in-infants-physical-reasoning)

#### AAAS

- [Pure reasoning in 12-month-old infants as probabilistic inference](#pure-reasoning-in-12-month-old-infants-as-probabilistic-inference)

#### CVPR

- [Newtonian image understanding: unfolding the dynamics of objects in static images](#newtonian-image-understanding-unfolding-the-dynamics-of-objects-in-static-images)

#### ECCV

- [Answering visual what-if questions: from actions to predicted scene descriptions](#answering-visual-what-if-questions-from-actions-to-predicted-scene-descriptions)

#### TICS

- [Mind games: game engines as an architecture for intuitive physics](#mind-games-game-engines-as-an-architecture-for-intuitive-physics)

#### FNHUM

- [Causal reasoning with forces](#causal-reasoning-with-forces)

### References

#### Reasoning about physical interactions with object oriented prediction and planning

*Michael Janner, Sergey Levine, William T. Freeman, Joshua B. Tenenbaum, Chelsea Finn, Jiajun Wu - International Conference on Learning Representations, 2019*

The main problem which is tried to be solved is to learn object representations to plan actions for pyhsical scene understanding without using object representations as explicit supervisions. The training is done by dropping objects to a scene containing at most four objects and trying to predict the steady state image while learning physical relations between objects. Extractor model for these object representations can then be used, for example, for building a tower from scratch. Object representation labels are difficult to obtain and therefore methods using them are not scalable. Instead of directly using them, method uses segmentation map estimates of each object in an image to train an object representation extractor. This model is jointly trained with physical scene understanding model and pixel level frame prediction model.

#### Simulation as an engine of physical scene understanding

*Peter W. Battaglia, Jessica B. Hamrick, and Joshua B. Tenenbaum - Proceedings of the National Academy of Sciences, 2013*

It is one of the examples from pre deep learning era. It basically defines different scence states at different time steps. Method incorporates two different forces applied to the scene which are the initial force and the transition forces betweeen two time steps. There are observable information for both scenes and forces. Given observed information about these states and latent forces, the method uses Bayesian learning to estimate the posterior probabilities for physical scene understanding. The first problem that the method is trying to solve is "Will it fall?". When provided with an image of a tower, the model and the subjects are asked to decide whether the tower will fall or not. The second experiment is conducted on top of the first experiment to evaluate the performance of the model and the subject when asked the direction of the fall action. These experiments are also repeated by using object with different masses to evaluate the intuition that the mass brings. In the last experiment, the model and the subjects are compared according to their intuitions in case of an external force such as a bump to a table holding the objects.

#### Innate ideas revisited for a principle of persistence in infants’ physical reasoning

*Renée Baillargeon - Perspectives on Psychological Science, 2008*

Innate ideas have extensively been argued in philosophy and cognitive science. The source of many arguments is to decide whether or not innate ideas have impact on infants' physical reasoning. Researchers or philosophers who think that these ideas do not have any effect on infant's development, states that reasoning is a capability that can be acquired only by experimenting. However, other side of the argument mainly accepts Spelke's two principles for innate capabilities which are continuity and cohesion. This paper claims that these two principles are actually corollaries of a single principle which is persistence. In order to strengthen the claim, it states the importance of variables included by an infant to predict the outcome of an event. If these variables such as height, color of the objects in the event, are somehow induced to the infant, he or she can be able to predict the outcome of that event regardless of the type of the event (continuity or change violation) and age of his or her.

#### Pure reasoning in 12-month-old infants as probabilistic inference

*Ernő Téglás, Edward Vul, Vittorio Girotto, Michel Gonzalez, Joshua B. Tenenbaum, Luca L. Bonatti - American Association for the Advancement of Science, 2011*

Adults' capability for pure reasoning is rich and coherent for identifying the outcomes of the event that they never faced. This is one of the most important issues that artificial intelligence should overcome to be reach the level of human intelligence. Before fully understant how adults are capable of doing such inferences, it is important to understand to what degree infants are capable of doing similar inferences as adults. This paper try to explain 12 month old infants' capabilities for pure reasoning by creating a Bayesian model which predicts infants' looking times for specific events. For one specific event, researchers create videos of four objects moving in a container which contains a gate from which the objects may go out. By having the same color for three of these four objects, researchers estimated how well the infants predicted the true object which goes out from the gate after a few seconds of occluding the scene. By variying, the object positions and the duration of the occlusion, researchers detected that infants use different types of reasonings for different situations as adults do. On top this observations, authors try to develop an ideal observer depending on Monte Carlo sampling which can predict similar to the infants. Here, the similarity of the model and infants' predictions are compared with each other, they are not compared with ground truths.

#### Newtonian image understanding: unfolding the dynamics of objects in static images

*Roozbeh Mottaghi, Hessam Bagherinezhad, Mohammad Rastegari, Ali Farhadi - IEEE Conference on Computer Vision and Pattern Recognition, 2016*

Humans are capable of estimating pyhsical dynamics of moving objects in a scene even from a single source of image. The main purpose of this paper is to create a model that tries to estimate the forces acting on a query object in an image and to predict the expected motion as a response to those forces. Instead of directly trying to estimate physical properties such as mass or friction, the method tries to convert from visual domain to a physical abstraction domain in which 12 Newtonian scenarios with multiple viewpoints are used. Mapping to one of these scenarios allows the method to borrow some physical quantities and to make prediction about 3D motion of the query object. This mapping is achieved by solving two different sub-problems which are finding the best scenario and the moment in the scenario to decide the current state of the object in the scene. These scenarios are created using a game engine simulation. Each resulting image after simulation is represented with 10 channels corresponding to RGB, depth, surface normals and optical flow information.

![Scenarios](/images/NewtonianScenarios.png)

#### Answering visual what-if questions: from actions to predicted scene descriptions

*Misha Wagner, Hector Basevi, Rakshith Shetty, Wenbin Li, Mateusz Malinowski, Mario Fritz, and Ales Leonardis - European Conference on Computer Vision, 2018*

Current work for scene understanding and next frame prediction problems in robotics see the agents as passive observers and do not allow them to manipulate the environment. What-if question tasks on the other hand allow the scene to be manipulated by a hypothetical action. The main problem to be solve is to describe the outcome of an action on a table top scenario. To solve their problem, authors created a dataset, TIWIQ, consisting of 3D scenes of realistically textured objects with interactions. Scenes contained five of eight realistic looking objects such as brick, banana, softball. They use a four different actions which are 1. Push an object in a specific direction. 2. Rotate an object clockwise or anti-clockwise. 3. Remove an object from the scene. 4. Drop an object on another object. They gather annotations on top of simulation rendering videos and ask their model and human baseline to output as similar as possible with the annotations. Their prediction does not include a generator model, instead they use a hybrid QA model for which they integrate a pyhsics engine. Engine gets input from laerning-based components to simulate and the result of the simulation is then tried to be expressed as a natural language output. The method overview can be seen from the visual. They compare their method with an end-to-end network without any image generation to mimic physics simulation and argue that hybrid model is more successful than a data driven model.

![Method Overview](/images/TIWIQBaseModel.png)

#### Mind games: game engines as an architecture for intuitive physics

*Tomer D. Ullman Elizabeth Spelke, Peter Battaglia and Joshua B. Tenenbaum - Trends in Cognitive Sciences, 2017*

This paper investigates the hypothesis that intuitive decisions about physics are made by the help of a mental engine which has similar characteristics with game physics engines especially for the young infants. This hypothesis claims that the data structures in our mind to represent the objects and the events, and the algorithms to simulate have similar characteristics with those provided by video game industry. One of the facts for authors to support their hypothesis is that both mental and game engines are designed to approximate the complex scenes to a reasonable-looking and human-relevant scale. Other than the similarities of representing objects and events, bodies and shapes, static and dynamic objects; resolving the collisions between mental processings and physics engines, they both fail to identify exact physical situations in some physical illusions because of some simplified assumptions made by their processes.

#### Learning particle dynamics for manipulating rigid bodies, deformable objects, and fluids

*Yunzhu Li, Jiajun Wu, Russ Tedrake, Joshua B. Tenenbaum, & Antonio Torralba - International Conference on Learning Representations, 2019*

It is one of the examples that uses graph networks for learning physics dynamics of objects. It is implemented on top of interaction networks, propagation networks and hierarchical relation networks where authors create the relations (edges) dynamically. The creation of these relations and the usage of hierarchy are object state specific where the tested object states are rigid bodies, fluids and deformable objects. Each of these are represented by different graphs where nodes are titled as particles. Besides learning the representation of the physics, authors experimented the models on downstream control tasks using model predictive control algorithms (MPC) where the trajectories are represented as the collection of graphs. The proposed algorithm using MPC is also capable of learning unknown object properties via shooting.

![Method Features](/images/DPINetsFeatures.png)

#### Clevrer: collision events for video representation and reasoning

Authors provide a new dataset for evaluating reasoning performance of the models trained for video understanding. Besides recognizing visual features inside the video, this dataset challenges models to understand the dynamics between objects and events and answer to the questions which require causal analysis to recognize the events and their reasons. The dataset contains for different question types; descriptive, explanatory, predictive and counterfactual whose samples are provided below. There are three events which are enter, exit and collision from them collision is the reason for extracting a causal tree of the events. The dataset objects, materials, colors are very similar to CLEVR dataset except the fact that authors use a physics engine to simulate events and a render engine to create videos instead of single images. A couple of baseline models; language only, video question answering and compositional visual reasoning (by modifying to work with videos) are trained and evaluated using Clevrer. While the overall performance of baseline models are quite low, authors observed that using object segmentation maps as explicit object representations increases performances. The second observation that the authors provided is that the dynamics modeling is required as well as explisit object representations in models to be able to be successful in such datasets requiring investigation of the causal structure between the events. Therefore, they also train a new model which models the dynamics using Propagation Networks (PropNet) and show that the results are better compared to baselines.

![Samples for Four Different Question Types](/images/CLEVRER.png)

#### Causal reasoning with forces

Understanding how people perceive events or statements requiring causal reasoning is important. In order to understand this hierarchical perception of humans there exist several theories, from them some are mental model theory and causal model theory whose units of perceptions are abstract. Mentam model theory states that logical operations are used in sub-relations of complex compositions to produce a single conclusion, whereas causal model theory is based on a Bayesian network where the relations are represented probabilistically. Authors propose a new theory which they title as force theory for which their first claim is that the units of perception need not to be abstract as in the previous theories and can resemblance to real world entities. They represent cause, help or prevent relations by different configurations of the forces appeared in affector and patient. Therefore, composition of sub-relations to obtain the final (possibly more than one) result can be achieved by transferring or eliminating the forces existing in the relation. In their experiments, they created physical environments based on 3D simulators and compared participants' perception results with the outputs of three models mentioned. They observe that the force theory predicts as well as or better than the theories which are based on abstract units. They also provide experiment results evaluating abstract causation performances. They compared how close predictions of force theory to humans when compared to other theories when provided causal compositions such as "Stress causes for getfulness and forgetfulness causes confusion". This time the forces are not real world forces but are approximate influences of affectors on again patients. They observe a similar pattern in their experiments evaluating abstract causation. All three models are very successful mimicing human performances with few mistakes. However, depending on iconic representations, can better explain how these events might be perceived.

![Iconic Representation of Forces](/images/CausalReasoningWithForces.png)

#### Forward prediction for physical reasoning

Given an initial state of the scene, physical reasoning tasks mostly require forward prediction. In this work, authors try to evaluate the performance of forward prediction models on pyhsical reasoning tasks, specifically on the PHYRE benchmark. They observed that although incorporating forward prediction models improves performance of physical reasoning tasks, this does not always mean that better forward prediction models are more successful at understanding the physical dynamics of the scene. Furthermore, they also observed that object based forward predictors outperforms pixels based forward predictor while using pixel based predictors are more helpful in physical reasoning. When using different set of test and train templates of PHYRE, authors' experiments with forward predictors also state that their effects are limited. This suggests that forward predictors brings negligible improvements for cross-template settings. Within the templates, they also experimented to see which tasks benefit more from using forward predictors. Although their success metric for the tasks (AUCCESS) decreases, the improvements when using forward predictors becomes much more visible when the number objects is increased.

### Model Implementations

- [Object level Visual Reasoning in Videos](https://github.com/fabienbaradel/object_level_visual_reasoning) (Object masks are required.)

- [Explore Multi-Step Reasoning in Video Question Answering](https://github.com/SVQA-founder/SVQA/tree/master/code) (Tensorflow.)


### Read Queue

- [Do neural language representations learn physical commonsense?](https://arxiv.org/pdf/1908.02899.pdf)

- [An integrative computational architecture for object-driven cortex](http://www.mit.edu/~ilkery/papers/YildirimetalCONEUR.pdf)

- [The scope and limits of simulation in automated reasoning](https://arxiv.org/pdf/1506.04956.pdf)

- [Unsupervised Intuitive Physics from Visual Observations](http://geometry.cs.ucl.ac.uk/projects/2018/unsupervised-intuitive-physics/paper_docs/EhrhardtMonszpartEtAl_UnsupervisedIntuitivePhysics_ACCV18.pdf)

- [Interaction Networks for Learning about Objects, Relations and Physics](https://arxiv.org/pdf/1612.00222.pdf)

- [Interpretable Intuitive Physics Model](https://arxiv.org/pdf/1808.10002.pdf)

- [The Seven Tools of Causal Inference, with Reflections on Machine Learning](https://ftp.cs.ucla.edu/pub/stat_ser/r481.pdf)

- [Bounce and Learn: Modeling Scene Dynamics with Real-World Bounces](https://openreview.net/forum?id=BJxssoA5KX)

- [NeuroAnimator:
Fast Neural Network Emulation and Control of Physics-Based Models](http://www.cs.toronto.edu/~fritz/absps/siggraph98.pdf)

- [Inferring mass in complex scenes by mental simulation](http://cocosci.princeton.edu/papers/Hamrick_Cognition.pdf)

- [Intuitive Physics](http://www.indiana.edu/~koertge/H205SciReas/McCloskey_IntuitivePhysics.pdf)
