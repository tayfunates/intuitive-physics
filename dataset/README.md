# Simulated Visual Question Answering Dataset

Includes general information about visual question answering dataset (Simulated Visual Question Answering, SVQA) that we have generated from our Box2D simulated environment. 

Internal tagging information:

[RED]: https://placehold.it/15/f03c15/000000?text=+
[GREEN]: https://placehold.it/15/3cf015/000000?text=+
[BLUE]: https://placehold.it/15/3c15f0/000000?text=+
[PURPLE]: https://placehold.it/15/f015f0/000000?text=+
[CYAN]: https://placehold.it/15/15f0f0/000000?text=+

- ![RED] Shows properties that CLEVRER has and we do not consider yet.
- ![GREEN] Shows questions or functional modules whose implementation has been completed in our backend.
- ![BLUE] Shows questions or functional modules whose implementation has NOT been completed in our backend, but it can be completed without any design updates.
- ![PURPLE] Shows questions or functional modules whose implementation has NOT been completed in our backend. Implementing such properties is not easy now, and needs discussing.
- ![CYAN] Internal discussion tag.

## Objects

### Shapes

- Cube
- Triangle
- Hexagon
- Circle

### Sizes

- Small
- Large

### Colors

- Gray
- Red
- Blue
- Green
- Brown
- Purple
- Cyan
- Yellow
- Black (Only static objects are black, and they cannot be covered by any other color.)

### Static Objects

- Ramp
- Platform
- Basket
- Left Wall
- Right Wall
- Ground

## Events

- Start Event (SE)
- End Event (EE)
- Collision Event (CE)
- Start Touching Event (STE)
- End Touching Event (ETE)
- Basket En Up Event (BEUE)

## Input and Output Data Types of Functional Modules

- Object: A dictionary holding static and dynamic properties of an object at a time step
- ObjectSet: A list of unique objects
- ObjectSetList: A list of ObjectSet
- Event: A dictionary holding information of a specific event: id, type, time step, participating objects
- EventSet: A list of unique events
- EventSetList: A list of EventSet
- Color: A tag indicating the color of an object
- Shape: A tag indicating the shape of an object
- ![RED] Frame or Step: An integer representing when an event happened 
- Integer: An integer type
- Bool: A boolean type
- BoolList: A list of Bool

## Side Inputs

### Object Side Inputs

- **Z**: Size
- **C**: Color
- **S**: Shape

### Synonmys

#### Noun and Adjective Synonyms

"thing": "thing", "object"</br>
"sphere": "sphere", "ball"</br>
"cube": "cube", "block"</br>
"large": "large", "big"</br>
"small": "small", "tiny"</br>
"ground": "ground", "bottom", "floor"</br>
"basket": "basket", "container", "bucket"</br>

#### Verb Synonyms

"prevent": "prevent", "keep", "hold", "block", "hinder"</br>
"prevents": "prevents", "keeps", "holds", "blocks", "hinders"</br>
"prevented": "prevented", "kept", "held", "blocked"</br>
"enable": "enable", "permit", "allow"</br>
"enables": "enables", "permits", "allows"</br>
"cause": "cause", "stimulate", "lead", "trigger"</br>
"causes": "causes", "stimulates", "leads", "triggers"</br>
"enter": "enter", "go into", "get into", "end up in", "fall into"</br>
"entering": "entering", "going into", "getting into", "ending up in", "falling into"</br>
"enters": "enters", "goes into", "gets into", "ends up in", "falls into"</br>
"fall to": "fall to", "hit"</br>
"falling to": "falling to", "hitting"</br>
"falls to": "falls to", "hits"</br>

## Functional Modules

| Name  | Description  | Input Types  | Output Types  | Implementation Status |
|---|---|---|---|---|
| SceneAtStart  | Returns all object properties at the start of the simulation  | None | ObjectSet | ![GREEN] |
| SceneAtEnd | Returns all object properties at the end of the simulation | None  | ObjectSet  | ![GREEN]   |
| StartSceneStep  | Returns 0  | None | Integer | ![GREEN] |
| EndSceneStep  | Returns -1  | None | Integer | ![GREEN] |
| Intersect  | Intersects two sets of objects | ObjectSet, ObjectSet | ObjectSet | ![GREEN]  |
| IntersectList  | Intersects an object set with all object sets in a list of ObjectSet | ObjectSetList, ObjectSet | ObjectSetList | ![GREEN]  |
| Events  | Returns all events between video start and end  | None  | EventSet  | ![GREEN]  |
| StartEvent  | Returns start event  | None  | Event  | ![BLUE]  |
| EndEvent  | Returns end event  | None  | Event  | ![BLUE]  |
| FilterColor  | Returns objects from input list which has the color of input color  | ObjectSet, Color  | ObjectSet  | ![GREEN]  |
| FilterShape  | Returns objects from input list which has the shape of input shape  | ObjectSet, Shape  | ObjectSet  | ![GREEN]  |
| FilterCollision  | Returns collision events from the input list | EventSet | EventSet | ![GREEN]  |
| FilterCollisionWithDynamics  | Returns collision events including only dynamic objects from the input list | EventSet | EventSet | ![GREEN]  |
| FilterCollideGround | Returns collision events including the ground from the input list | EventSet | EventSet | ![GREEN]  |
| FilterCollideGroundList | Returns list of collision event sets including the ground from a list of event sets | EventSetList | EventSetList | ![GREEN]  |
| FilterCollideBasket | Returns collision events including the basket from the input list | EventSet | EventSet | ![GREEN]  |
| FilterCollideBasketList | Returns list collision event sets including the basket from a list of event sets | EventSetList | EventSetList | ![GREEN]  |
| FilterEnterContainer | Returns container end up events from the input list | EventSet | EventSet | ![GREEN]  |
| FilterEnterContainerList | Returns list of container end up event sets from a list of event sets | EventSetList | EventSetList | ![GREEN]  |
| FilterStartTouching  | Returns start touching events from the input list | EventSet | EventSet | ![BLUE]  |
| FilterEndTouching  | Returns end touching events from the input list | EventSet | EventSet | ![BLUE]  |
| FilterBefore  | Returns events from the input list that happened before input event  | EventSet, Event  | EventSet  | ![Green]  |
| FilterAfter  | Returns events from the input list that happened after input event  | EventSet, Event  | EventSet  | ![GREEN]  |
| FilterMoving  | Returns objects if they are moving at step specified by an Integer   | ObjectSet, Integer  | ObjectSet  | ![Green]  |
| FilterStationary  | Returns objects if they are stationary at step specified by an Integer   | ObjectSet, Integer  | ObjectSet  | ![Green]  |
| FilterFirst  | Returns the first event from the input list  | EventSet  | Event  | ![GREEN]  |
| FilterLast  | Returns the last event from the input list  | EventSet  | Event  | ![GREEN]  |
| FilterUnique  | Returns unique object from input list with possible side inputs Size, Color, Shape  | Objects, ObjectSideInputs | Object  | ![GREEN]  |
| Unique  | Returns the single object from the input list, if list has more than one elements returns INVALID  | Objects | Object  | ![GREEN]  |
| EventPartner (CE, STE, ETE) | Returns object from the object list of the input event which is not input object  | Event, Object  | Object  | ![GREEN]  |
| QueryColor  | Returns the color of the input object  | Object  | Color  | ![GREEN]  |
| QueryShape  | Returns the shape of the input object  | Object  | Shape  | ![GREEN]  |
| Count  | Returns size of the input list  | ObjectSet, EventSet  | Integer  | ![GREEN] for ObjectSet ![BLUE] for EventSet |
| Exist  | Returns true if the input list is not empty  | ObjectSet, EventSet  | Bool  | ![GREEN] |
| ExistList  | Applies Exist to each item in input list returning a list of Bool | ObjectSetList | BoolList  | ![GREEN] for ObjectSetList ![BLUE] for EventSetList |
| AnyFalse  | Returns true if there is at least one false in a bool list | BoolList  | Bool | ![GREEN] |
| AnyTrue  | Returns true if there is at least one true in a bool list | BoolList  | Bool | ![GREEN] |
| FilterObjectsFromEvents  | Returns objects from events | EventSet  | ObjectSet  | ![Green]  |
| FilterObjectsFromEventsList  | Returns list object sets from a list of event sets | EventSetList  | ObjectSetList  | ![Green]  |
| GetCounterfactEvents  | Returns event list if a specific object is removed from the scene   | Object  | EventSet  | ![Green]  |
| GetCounterfactEventsList  | Returns event list for all objects in an object set | ObjectSet  | EventSetList  | ![Green]  |
| FilterDynamic  | Returns dynamic objects from an object set   | ObjectSet  | ObjectSet  | ![Green]  |
| AsList  | Returns single elemen object set created with a specific object | Object | ObjectSet  | ![GREEN] |

Other clevrer filters that are needed to be discussed.
- ![RED]: FilterIn: Selects all incoming events of the input objects
- ![RED]: FilterOut: Selects all exiting events of the input objects

## Questions

![CYAN] Cevap çeşidine bir an önce karar vermek gerekiyor. CLEVR'dan farklı bir yol izleyeceksek (CLEVRER gibi mesela), şimdiden onunla uğraşmalıyız, soru yaratmadan önce.

### Structures Provided to Question Generation Engine

- Scene information at start (SceneAtStart): Holds objects' static and dynamic information at start of the video, color, position, shape, velocity etc.
- Scene information at end (SceneAtEnd): Holds objects' static and dynamic information at end of the video, color, position, shape, velocity etc.
- Causal graph (CausalGraph): Graph constructed by events of objects as nodes. All events causing a specific event are the ancestors of that event.

### All Tasks

| Task  |  Category |
|---|---|
| 1. "What color is the object the **Z** **C** **S** first collides with?", "What color is the first object to collide with the **Z** **C** **S**?", "What is the color of object the **Z** **C** **S** first collides with?", "What is the color of first object to collide with the **Z** **C** **S**?" | Descriptive |
| 2. "What shape is the object the **Z** **C** **S** first collides with?", "What shape is the first object to collide with the **Z** **C** **S**?", "What is the shape of object the **Z** **C** **S** first collides with?", "What is the shape of first object to collide with the **Z** **C** **S**?" | Descriptive |
| 3. "What color is the object the **Z** **C** **S** last collides with?", "What color is the last object to collide with the **Z>** **C** **S**?", "What is the color of object the **Z** **C** **S** last collides with?", "What is the color of last object to collide with the **Z** **C** **S**?" | Descriptive |
| 4. "What shape is the object the **Z** **C** **S** last collides with?", "What shape is the last object to collide with the **Z** **C** **S**?", "What is the shape of object the **Z** **C** **S** last collides with?", "What is the shape of last object to collide with the **Z** **C** **S**?" | Descriptive |
| 5. "How many **S**s are moving when the video ends?", "How many **S**s are in motion at the end of the video?" | Descriptive |
| 6. "How many **C** objects are moving when the video ends?", "How many **C** objects are in motion at the end of the video?" | Descriptive |
| 7. "How many **Z** objects are moving when the video ends?", "How many **Z** objects are in motion at the end of the video?" | Descriptive |
| 8. "How many objects are moving when the video ends?", "How many objects are in motion at the end of the video?" | Descriptive |
| 9. "How many **S**s **enter** the **basket**?" | Descriptive|
| 10. "How many **C** objects **enter** the **basket**?" | Descriptive |
| 11. "How many **Z** objects **enter** the **basket**?" | Descriptive |
| 12. "How many objects **enter** the **basket**?" | Descriptive |
| 13. "How many **S**s **fall to** the **ground**?" | Descriptive |
| 14. "How many **C** objects **fall to** the **ground**?" | Descriptive |
| 15. "How many **Z** objects **fall to** the **ground**?" | Descriptive |
| 16. "How many objects **fall to** the **ground**?" | Descriptive |
| 17. "How many **S**s collide with the **basket**?" | Descriptive |
| 18. "How many **C** objects collide with the **basket**?" | Descriptive |
| 19. "How many **Z** objects collide with the **basket**?" | Descriptive |
| 20. "How many objects collide with the **basket**?" | Descriptive |
| 21. "How many objects **enter** the **basket** after the **Z** **C** **S** **enters** the **basket**?" | Descriptive |
| 22. "How many objects **enter** the **basket** before the **Z** **C** **S** **enters** the **basket**?" | Descriptive |
| 23. "How many objects **fall to** the **ground** after the **Z** **C** **S** **falls** to the **ground**?" | Descriptive |
| 24. "How many objects **fall to** the **ground** before the **Z** **C** **S** **falls** to the **ground**?" | Descriptive |
| 25. "How many objects collide with the **basket** after the **Z** **C** **S** hits the **basket**?" | Descriptive |
| 26. "How many objects collide with the **basket** before the **Z** **C** **S** hits the **basket**?" | Descriptive |
| 27. "After **entering** the **basket**, does the **Z** **C** **S** collide with other objects?" | Descriptive |
| 28. "Before **entering** the **basket**, does the **Z** **C** **S** collide with other objects?" | Descriptive |
| 29. "After **falling to** the **ground**, does the **Z** **C** **S** collide with other objects?" | Descriptive |
| 30. "Before **falling to** the **ground**, does the **Z** **C** **S** collide with other objects?" | Descriptive |
| 31. "After colliding with the **basket**, does the **Z** **C** **S** hit other objects?" | Descriptive |
| 32. "Before colliding with the **basket**, does the **Z** **C** **S** hit other objects?" | Descriptive |
| 33. "Are there any collisions between objects after the **Z** **C** **S** **enters** the **basket**?" | Descriptive |
| 34. "Are there any collisions between objects before the **Z** **C** **S** **enters** the **basket**?" | Descriptive |
| 35. "Are there any collisions between objects after the **Z** **C** **S** **falls to** the **ground**?" | Descriptive |
| 36. "Are there any collisions between objects before the **Z** **C** **S** **falls to** the **ground**?" | Descriptive |
| 37. "Are there any collisions between objects after the **Z** **C** **S** hits the **basket**?" | Descriptive |
| 38. "Are there any collisions between objects before the **Z** **C** **S** hits the **basket**?" | Descriptive |
| 39. "Does the **Z2** **C2** **S2** **enter** the **basket**, if the **Z** **C** **S** is removed?", "If the **Z** **C** **S** is removed, does the **Z2** **C2** **S2** **enter** the **basket**?" | Counterfactual |
| 40. "Does the **Z2** **C2** **S2** **fall to** the **ground**, if the **Z** **C** **S** is removed?", "If the **Z** **C** **S** is removed, does the **Z2** **C2** **S2** **fall to** the **ground**?" | Counterfactual |
| 41. "Does the **Z2** **C2** **S2** collide with the **basket**, if the **Z** **C** **S** is removed?", "If the **Z** **C** **S** is removed, does the **Z2** **C2** **S2** collide with the **basket**?" | Counterfactual |
| 42. "How many objects **enter** the **basket**, if the **Z** **C** **S** is removed?", "If the **Z** **C** **S** is removed, how many objects **enter** the **basket**?" | Counterfactual |
| 43. "How many objects **fall to** the **ground**, if the **Z** **C** **S** is removed?", "If the **Z** **C** **S** is removed, how many objects **fall to** the **ground**?" | Counterfactual |
| 44. "How many objects collide with the **basket**, if the **Z** **C** **S** is removed?", "If the **Z** **C** **S** is removed, how many objects collide with the **basket**?" | Counterfactual |
| 45. "Does the **Z** **C** **S** **enter** the **basket**, if any of the other objects are removed?", "If any of the other objects are removed, does the **Z** **C** **S** **enter** the **basket**?" | Counterfactual |
| 46. "Does the **Z** **C** **S** **fall to** the **ground**, if any of the other objects are removed?", "If any of other the objects are removed, does the **Z** **C** **S** **fall to** the **ground**?" | Counterfactual |
| 47. "Does the **Z** **C** **S** collide with the **basket**, if any of the other objects are removed?", "If any of the other objects are removed, does the **Z** **C** **S** collide with the **basket**?" | Counterfactual |
| 48. "Does the **Z** **C** **S** **enable** the **Z2** **C2** **S2** to **fall to** the **ground**?", "Does the **Z** **C** **S** **enable** the collision between the **Z2** **C2** **S2** and the **ground**?", "There is a **Z** **C** **S**, does it **enable** **Z2** **C2** **S2** to **fall to** the **ground**?" | Enable |
| 49. "Does the **Z** **C** **S** **enable** the **Z2** **C2** **S2** to **enter** the **basket**?", "There is a **Z** **C** **S**, does it **enable** the **Z2** **C2** **S2** to **enter** the **basket**?" | Enable |
| 50. "Does the **Z** **C** **S** **enable** the **Z2** **C2** **S2** to collide with the **basket**?", "Does the **Z** **C** **S** **enable** the collision between the **Z2** **C2** **S2** and the **basket**?", "There is a **Z** **C** **S**, does it **enable** **Z2** **C2** **S2** to collide with the **basket**?" | Enable |
| 51. "How many objects does the **Z** **C** **S** **enable** to **fall to** the **ground**?", "What is the number of objects that the **Z** **C** **S** **enables** to **fall to** the **ground**?" | Enable |
| 52. "How many objects does the **Z** **C** **S** **enable** to **enter** the **basket**?", "What is the number of objects that the **Z** **C** **S** **enables** to **enter** the **basket**?" | Enable |
| 53. "How many objects does the **Z** **C** **S** **enable** to collide with the **basket**?", "What is the number of objects that the **Z** **C** **S** **enables** to collide with the **basket**?" | Enable |
| 54. "Does the **Z** **C** **S** **cause** the **Z2** **C2** **S2** to **fall to** the **ground**?", "Does the **Z** **C** **S** cause the collision between the **Z2** **C2** **S2** and the **ground**?", "There is a **Z** **C** **S**, does it **cause** the **Z2** **C2** **S2** to **fall to** the **ground**?" | Cause |
| 55. "Does the **Z** **C** **S** **cause** the **Z2** **C2** **S2** to **enter** the **basket**?", "There is a **Z** **C** **S**, does it **cause** the **Z2** **C2** **S2** to **enter** the **basket**?" | Cause |
| 56. "Does the **Z** **C** **S** **cause** the **Z2** **C2** **S2** to collide with the **basket**?", "Does the **Z** **C** **S** cause the collision between the **Z2** **C2** **S2** and the **basket**?", "There is a **Z** **C** **S**, does it **cause** the **Z2** **C2** **S2** to it the **basket**?" | Cause |
| 57. "How many objects does the **Z** **C** **S** **cause** to **fall to** the **ground**?", "What is the number of objects that the **Z** **C** **S** **causes** to **fall to** the **ground**?" | Cause |
| 58. "How many objects does the **Z** **C** **S** **cause** to **enter** the **basket**?", "What is the number of objects that the **Z** **C** **S** **causes** to **enter** the **basket**?" | Cause |
| 59. "How many objects does the **Z** **C** **S** **cause** to it the **basket**?", "What is the number of objects that the **Z** **C** **S** **causes** to it the **basket**?" | Cause |
| 60. "Does the **Z** **C** **S** **prevent** the **Z2** **C2** **S2** from **falling to** the **ground**?", "There is a **Z** **C** **S**, does it **prevent** the **Z2** **C2** **S2** from **falling to** the **ground**?", "Is the **Z2** **C2** **S2** is **prevented** by the **Z** **C** **S** from **falling to** the **ground**?" | Prevent |
| 61. "Does the **Z** **C** **S** **prevent** the **Z2** **C2** **S2** from **entering** the **basket**?", "There is a **Z** **C** **S**, does it **prevent** the **Z2** **C2** **S2** from **entering** the **basket**?", "Is the **Z2** **C2** **S2** is **prevented** by the **Z** **C** **S** from **entering** the **basket**?" | Prevent |
| 62. "Does the **Z** **C** **S** **prevent** the **Z2** **C2** **S2** from colliding with the **basket**?", "There is a **Z** **C** **S**, does it **prevent** the **Z2** **C2** **S2** from colliding with the **basket**?", "Is the **Z2** **C2** **S2** is **prevented** by the **Z** **C** **S** from colliding with the **basket**?" | Prevent |
| 63. "How many objects does the **Z** **C** **S** **prevent** from **falling to** the **ground**?", "What is the number of objects that the **Z** **C** **S** **prevents** from **falling to** the **ground**?", "How many objects are **prevented** by the **Z** **C** **S** from **falling to** the **ground**?", "What is the number of objects that are **prevented** by the **Z** **C** **S** from **falling to** the **ground**?" | Prevent |
| 64. "How many objects does the **Z** **C** **S** **prevent** from **entering** the **basket**?", "What is the number of objects that the **Z** **C** **S** **prevents** from **entering** the **basket**?", "How many objects are **prevented** by the **Z** **C** **S** from **entering** the **basket**?", "What is the number of objects that are **prevented** by the **Z** **C** **S** from **entering** the **basket**?" | Prevent |
| 65. "How many objects does the **Z** **C** **S** **prevent** from colliding with the **basket**?", "What is the number of objects that the **Z** **C** **S** **prevents** from colliding with the **basket**?", "How many objects are **prevented** by the **Z** **C** **S** from colliding with the **basket**?", "What is the number of objects that are **prevented** by the **Z** **C** **S** from colliding with the **basket**?" | Prevent |

### Samples

#### Temporal

##### Yes/No

| Question | Answer | Original Video|
|---|---|---|
|**"Before colliding with big purple circle, does green circle collide with other objects?"**|**"false"**|![](/dataset/examples/ExampleScene9.gif)|
|**1. "Does the big blue ball collide with another object after colliding with the purple ball?"<br>2. "Does the yellow circle collide with an object after ending up in the container?"|**1. "false"<br>2. "true"**|![](/dataset/examples/ExampleScene6.gif)|
|**1. "Does the small green ball collide with an object before colliding with large red ball?"<br>2. "Does the big red circle collide with tiny brown cube before colliding with small blue ball?"**|**1. "true"<br>2. "false"**|![](/dataset/examples/ExampleScene5.gif)|
|**1. "Does the big cyan ball end up in the basket after colliding with the large yellow ball?"<br>2. "Does any other object end up in the basket before tiny brown ball ended up in the basket?"**|**1. "true"<br>2. "false"**|![](/dataset/examples/ExampleScene4.gif)|

#### Descriptive

##### Query Color

| Question | Answer | Original Video|
|---|---|---|
|"What color is the object that the big purple circle first collides with?"|"green"|![](/dataset/examples/ExampleScene9.gif)|

##### Query Shape


##### Counting

| Question | Answer | Original Video|
|---|---|---|
|"How many circles are moving when the video ends?"|"2"|![](/dataset/examples/ExampleScene9.gif)|
|"How many circles enter the basket?"|"1"|![](/dataset/examples/ExampleScene9.gif)|
|1. "How many objects enters the basket after the tiny brown ball enters the basket?"<br>2. "How many objects enters the basket before big yellow ball enters the basket?"|1. "2"<br>2. "2"|![](/dataset/examples/ExampleScene4.gif)|
|**1. "How many circles collide with red circle before it enters the basket?"<br>2. "How many circles collide with red circle before entering the basket?"**|**1. "2"<br>2. "2"**|![](/dataset/examples/ExampleScene7.gif)|
|"**How many objects either enter the basket or collide with the ground?**"|"**2**"|![](/dataset/examples/ExampleScene2.gif)|

![CYAN] Counting için, oluşturalacak sahnelerde hardcoded shape, color, size kullanmamak gerekiyor, atıyorum sadece circlelardan oluşan simulation gibi. Çünkü sahnede olmayan elemanların sayısı çok olmaya başlayınca 0 cevabının yoğunluğu artıyor olacak. 

![CYAN] Prevent/enable için ne gibi assumption olacak? Bu assumptionlar farklı sahneler için yeterince genericlik sağlayacak mı yoksa her simulation için farklı set of questions mı olacak?

##### Yes/No

| Question | Answer | Original Video |
|---|---|---|
|"Before entering the basket, does tiny cyan circle collide with other objects?"|"true"|![](/dataset/examples/ExampleScene11.gif)|
|"Are there any collisions after the brown ball enters the basket?"|"true"|![](/dataset/examples/ExampleScene6.gif)|

##### Counterfactual

| Question | Answer | Original Video| Variation Video |
|---|---|---|---|
|"How many objects get into the basket, if the large green circle is removed?"|3|![](/dataset/examples/ExampleScene13.gif)|![](/dataset/examples/ExampleScene13Variation1.gif)|
|"Does the large blue circle collide with the container, if the big green circle is removed?"|"true"|![](/dataset/examples/ExampleScene13.gif)|![](/dataset/examples/ExampleScene13Variation1.gif)|

##### Enable

| Question | Answer | Original Video| Variation Video |
|---|---|---|---|
|"Is the large green block responsible for the collision between the tiny blue block and the ground?"|"true"|![](/dataset/examples/ExampleScene1.gif)|![](/dataset/examples/ExampleScene1Variation1.gif)|
|"Does the big brown block enable the large cyan circle to enter the basket?"|"true"|![](/dataset/examples/ExampleScene2.gif)|![](/dataset/examples/ExampleScene2Variation1.gif)|
|"There is a tiny purple cube, does it enable the big cyan circle to enter the basket?"|"false"|![](/dataset/examples/ExampleScene2.gif)|![](/dataset/examples/ExampleScene2Variation2.gif)|
|"Are there any objects which enable the small brown cube to enter the basket?"|"true"|![](/dataset/examples/ExampleScene3.gif)|![](/dataset/examples/ExampleScene3Variation2.gif)|
|"How many objects does the big yellow circle enable to enter the basket?"|"2"|![](/dataset/examples/ExampleScene4.gif)|![](/dataset/examples/ExampleScene4Variation1.gif)|
|"What is the number of objects that the big red circle enable to fall to the ground?"|"0"|![](/dataset/examples/ExampleScene5.gif)|![](/dataset/examples/ExampleScene5Variation1.gif)|
|"Is there any object which enables the small green circle to enter the basket?"|"**true**"|![](/dataset/examples/ExampleScene7.gif)|![](/dataset/examples/ExampleScene7Variation1.gif)|
|"What is the number of objects that the large cyan circle enable to fall to the ground?"|"1"|![](/dataset/examples/ExampleScene8.gif)|![](/dataset/examples/ExampleScene8Variation1.gif)|
|"There is a tiny red circle, does it enable the small purple circle to enter the basket?"|"**true**"|![](/dataset/examples/ExampleScene10.gif)|![](/dataset/examples/ExampleScene10Variation1.gif)|

##### Cause
  
##### Prevent

| Question | Answer | Original Video| Variation Video |
|---|---|---|---|
|"Does the large green block prevent the small red block from falling to the ground?"|"true"|![](/dataset/examples/ExampleScene1.gif)|![](/dataset/examples/ExampleScene1Variation1.gif)|
|"Does the big yellow cube prevent the small blue triangle from entering to the basket?"|"true"|![](/dataset/examples/ExampleScene2.gif)|![](/dataset/examples/ExampleScene2Variation3.gif)|
|"Does the tiny purple circle prevent the big blue circle from entering to the basket?"|"true"|![](/dataset/examples/ExampleScene6.gif)|![](/dataset/examples/ExampleScene6Variation1.gif)|
|"Does the large cyan circle prevent the tiny brown circle from entering to the basket?"|"true"|![](/dataset/examples/ExampleScene8.gif)|![](/dataset/examples/ExampleScene8Variation1.gif)|
|"Does the large purple circle prevent the small green circle from entering to the basket?"|"true"|![](/dataset/examples/ExampleScene9.gif)|![](/dataset/examples/ExampleScene9Variation1.gif)|

### Relationships between Enable, Cause and Prevent Tasks

In order to have better understanding about the differences between the Enable, Cause, and Prevent tasks, one should understand the notion of "intention" in our environments. We identify the intention in a simulation by looking at the initial linear velocity of the corresponding object. If the magnitude of the velocity is greater than zero, then the object **is intended to** do the task specified in the question text, such as entering the basket or colliding with the ground. If the magnitude of the velocity is zero, then the object **is not intended to** do the task, even if there is an external force, such as gravity, upon it at the start of the simulation. Therefore, an affector object or event can only **enable** a patient object to do the task if the patient object is intended to do it but fails without the affector. Similarly, an affector object or event can only **cause** a patient object to do the task if the patient object is **not** intended to do it. Furthermore, an affector object or event can only **prevent** a patient object **not** to do the task if the patient object is intended to do it and succeeds without the affector.

Here are some examples to make these more clear:

![](/dataset/examples/ExampleScene12.gif)

**"Does the small purple triangle cause the tiny green triangle to get into the bucket?"**

The answer to this question is true since the green tiny triangle is not intended to enter the bucket (its initial x and y velocties are 0) and without the purple object, it does not enter the bucket.

**Does the large cyan triangle enable the tiny purple triangle to hit the bottom?**

The answer to this question is true since tiny purple triangle is intended to hit the bottom (its initial x and/or y velocities are not 0s) and without the large cyan triangle, the blue box would not collide with the purple triangle leading it to hit the bottom.

If we switch **cause** and **enable** keywords in these questions, then the answers become **false** because of the patient object intentions.

Similarly,

**Does the big cyan triangle hold the big blue block from going into the basket?**

The answer to this question is true since big blue block is intended to enter the basket, and without the cyan triangle, it succeeds to do so.

### Dataset Statistics

#### Answer Distributions for Different Simulations

| All | SID=1 | SID=2|
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Answer%20frequencies.png)| ![](/dataset/outputs/stats/Dataset_v230920/Answer%20frequencies%20for%20Simulation%20ID%3D1.png)| ![](/dataset/outputs/stats/Dataset_v230920/Answer%20frequencies%20for%20Simulation%20ID%3D2.png)|

| SID=3 | SID=4 | SID=5|
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Answer%20frequencies%20for%20Simulation%20ID%3D3.png)| ![](/dataset/outputs/stats/Dataset_v230920/Answer%20frequencies%20for%20Simulation%20ID%3D4.png)| ![](/dataset/outputs/stats/Dataset_v230920/Answer%20frequencies%20for%20Simulation%20ID%3D5.png)|

| SID=6 | SID=7 | SID=8|
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Answer%20frequencies%20for%20Simulation%20ID%3D6.png)| ![](/dataset/outputs/stats/Dataset_v230920/Answer%20frequencies%20for%20Simulation%20ID%3D7.png)| ![](/dataset/outputs/stats/Dataset_v230920/Answer%20frequencies%20for%20Simulation%20ID%3D8.png)|

| SID=9 | SID=10 |
|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Answer%20frequencies%20for%20Simulation%20ID%3D9.png)| ![](/dataset/outputs/stats/Dataset_v230920/Answer%20frequencies%20for%20Simulation%20ID%3D10.png)|

#### Answer Distributions for Different Tasks

| TID=cause_0 | TID=cause_1 | TID=cause_2 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dcause_0.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dcause_1.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dcause_2.png)|

| TID=cause_3 | TID=cause_4 | TID=cause_5 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dcause_3.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dcause_4.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dcause_5.png)|

| TID=counterfactual_0 | TID=counterfactual_1 | TID=counterfactual_2 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dcounterfactual_0.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dcounterfactual_1.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dcounterfactual_2.png)|

| TID=counterfactual_3 | TID=counterfactual_4 | TID=counterfactual_5 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dcounterfactual_3.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dcounterfactual_4.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dcounterfactual_5.png)|

| TID=counterfactual_6 | TID=counterfactual_7 | TID=counterfactual_8 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dcounterfactual_6.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dcounterfactual_7.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dcounterfactual_8.png)|

| TID=descriptive_0 | TID=descriptive_1 | TID=descriptive_2 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_0.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_1.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_2.png)|

| TID=descriptive_3 | TID=descriptive_4 | TID=descriptive_5 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_3.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_4.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_5.png)|

| TID=descriptive_6 | TID=descriptive_7 | TID=descriptive_8 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_6.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_7.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_8.png)|

| TID=descriptive_9 | TID=descriptive_10 | TID=descriptive_11 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_9.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_10.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_11.png)|

| TID=descriptive_12 | TID=descriptive_13 | TID=descriptive_14 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_12.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_13.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_14.png)|

| TID=descriptive_15 | TID=descriptive_16 | TID=descriptive_17 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_15.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_16.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_17.png)|

| TID=descriptive_18 | TID=descriptive_19 | TID=descriptive_20 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_18.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_19.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_20.png)|

| TID=descriptive_21 | TID=descriptive_22 | TID=descriptive_23 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_21.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_22.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_23.png)|

| TID=descriptive_24 | TID=descriptive_25 | TID=descriptive_26 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_24.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_25.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_26.png)|

| TID=descriptive_27 | TID=descriptive_28 | TID=descriptive_29 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_27.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_28.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_29.png)|

| TID=descriptive_30 | TID=descriptive_31 | TID=descriptive_32 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_30.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_31.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_32.png)|

| TID=descriptive_33 | TID=descriptive_34 | TID=descriptive_35 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_33.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_34.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_35.png)|

| TID=descriptive_36 | TID=descriptive_37 |
|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_36.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Ddescriptive_37.png)|

| TID=enable_0 | TID=enable_1 | TID=enable_2 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Denable_0.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Denable_1.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Denable_2.png)|

| TID=enable_3 | TID=enable_4 | TID=enable_5 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Denable_3.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Denable_4.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Denable_5.png)|

| TID=prevent_0 | TID=prevent_1 | TID=prevent_2 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dprevent_0.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dprevent_1.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dprevent_2.png)|

| TID=prevent_3 | TID=prevent_4 | TID=prevent_5 |
|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dprevent_3.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dprevent_4.png)| ![](/dataset/outputs/stats/Dataset_v230920/Template%20ID%3Dprevent_5.png)|


#### Answer Distributions for Simulation and Task Pairs

| SID=1, TID=cause_0| SID=1, TID=cause_1| SID=1, TID=cause_2 | SID=1, TID=cause_3|SID=1, TID=cause_4 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dcause_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dcause_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dcause_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dcause_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dcause_4.png)|

| SID=1, TID=cause_5| SID=1, TID=counterfactual_0| SID=1, TID=counterfactual_1 | SID=1, TID=counterfactual_2|SID=1, TID=counterfactual_3 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dcause_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dcounterfactual_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dcounterfactual_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dcounterfactual_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dcounterfactual_3.png)|

| SID=1, TID=counterfactual_4| SID=1, TID=counterfactual_5| SID=1, TID=counterfactual_6 | SID=1, TID=counterfactual_7|SID=1, TID=counterfactual_8 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dcounterfactual_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dcounterfactual_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dcounterfactual_6.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dcounterfactual_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dcounterfactual_8.png)|

| SID=1, TID=descriptive_0| SID=1, TID=descriptive_1| SID=1, TID=descriptive_10 | SID=1, TID=descriptive_11|SID=1, TID=descriptive_12 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_10.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_11.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_12.png)|

| SID=1, TID=descriptive_13| SID=1, TID=descriptive_14| SID=1, TID=descriptive_15 | SID=1, TID=descriptive_16|SID=1, TID=descriptive_17 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_13.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_14.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_15.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_16.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_17.png)|

| SID=1, TID=descriptive_18| SID=1, TID=descriptive_19| SID=1, TID=descriptive_2 | SID=1, TID=descriptive_20|SID=1, TID=descriptive_21 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_18.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_19.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_20.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_21.png)|

| SID=1, TID=descriptive_22| SID=1, TID=descriptive_23| SID=1, TID=descriptive_24 | SID=1, TID=descriptive_25|SID=1, TID=descriptive_26 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_22.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_23.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_24.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_25.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_26.png)|

| SID=1, TID=descriptive_27| SID=1, TID=descriptive_28| SID=1, TID=descriptive_29 | SID=1, TID=descriptive_3|SID=1, TID=descriptive_30 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_27.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_28.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_29.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_30.png)|

| SID=1, TID=descriptive_31| SID=1, TID=descriptive_32| SID=1, TID=descriptive_33 | SID=1, TID=descriptive_34|SID=1, TID=descriptive_35 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_31.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_32.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_33.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_34.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_35.png)|

| SID=1, TID=descriptive_36| SID=1, TID=descriptive_37| SID=1, TID=descriptive_4 | SID=1, TID=descriptive_5|SID=1, TID=descriptive_6 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_36.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_37.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_6.png)|

| SID=1, TID=descriptive_7| SID=1, TID=descriptive_8| SID=1, TID=descriptive_9 | SID=1, TID=enable_0|SID=1, TID=enable_1 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_8.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Ddescriptive_9.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Denable_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Denable_1.png)|

| SID=1, TID=enable_2| SID=1, TID=enable_3| SID=1, TID=enable_4 | SID=1, TID=enable_5|SID=1, TID=prevent_0 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Denable_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Denable_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Denable_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Denable_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dprevent_0.png)|

| SID=1, TID=prevent_1| SID=1, TID=prevent_2| SID=1, TID=prevent_3 | SID=1, TID=prevent_4|SID=1, TID=prevent_5 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dprevent_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dprevent_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dprevent_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dprevent_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D1-TID%3Dprevent_5.png)|

| SID=2, TID=cause_0| SID=2, TID=cause_1| SID=2, TID=cause_2 | SID=2, TID=cause_3|SID=2, TID=cause_4 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dcause_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dcause_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dcause_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dcause_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dcause_4.png)|

| SID=2, TID=cause_5| SID=2, TID=counterfactual_0| SID=2, TID=counterfactual_1 | SID=2, TID=counterfactual_2|SID=2, TID=counterfactual_3 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dcause_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dcounterfactual_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dcounterfactual_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dcounterfactual_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dcounterfactual_3.png)|

| SID=2, TID=counterfactual_4| SID=2, TID=counterfactual_5| SID=2, TID=counterfactual_6 | SID=2, TID=counterfactual_7|SID=2, TID=counterfactual_8 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dcounterfactual_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dcounterfactual_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dcounterfactual_6.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dcounterfactual_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dcounterfactual_8.png)|

| SID=2, TID=descriptive_0| SID=2, TID=descriptive_1| SID=2, TID=descriptive_10 | SID=2, TID=descriptive_11|SID=2, TID=descriptive_12 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_10.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_11.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_12.png)|

| SID=2, TID=descriptive_13| SID=2, TID=descriptive_14| SID=2, TID=descriptive_15 | SID=2, TID=descriptive_16|SID=2, TID=descriptive_17 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_13.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_14.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_15.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_16.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_17.png)|

| SID=2, TID=descriptive_18| SID=2, TID=descriptive_19| SID=2, TID=descriptive_2 | SID=2, TID=descriptive_20|SID=2, TID=descriptive_21 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_18.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_19.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_20.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_21.png)|

| SID=2, TID=descriptive_22| SID=2, TID=descriptive_23| SID=2, TID=descriptive_24 | SID=2, TID=descriptive_25|SID=2, TID=descriptive_26 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_22.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_23.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_24.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_25.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_26.png)|

| SID=2, TID=descriptive_27| SID=2, TID=descriptive_28| SID=2, TID=descriptive_29 | SID=2, TID=descriptive_3|SID=2, TID=descriptive_30 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_27.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_28.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_29.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_30.png)|

| SID=2, TID=descriptive_31| SID=2, TID=descriptive_32| SID=2, TID=descriptive_33 | SID=2, TID=descriptive_34|SID=2, TID=descriptive_35 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_31.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_32.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_33.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_34.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_35.png)|

| SID=2, TID=descriptive_36| SID=2, TID=descriptive_37| SID=2, TID=descriptive_4 | SID=2, TID=descriptive_5|SID=2, TID=descriptive_6 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_36.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_37.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_6.png)|

| SID=2, TID=descriptive_7| SID=2, TID=descriptive_8| SID=2, TID=descriptive_9 | SID=2, TID=enable_0|SID=2, TID=enable_1 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_8.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Ddescriptive_9.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Denable_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Denable_1.png)|

| SID=2, TID=enable_2| SID=2, TID=enable_3| SID=2, TID=enable_4 | SID=2, TID=enable_5|SID=2, TID=prevent_0 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Denable_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Denable_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Denable_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Denable_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dprevent_0.png)|

| SID=2, TID=prevent_1| SID=2, TID=prevent_2| SID=2, TID=prevent_3 | SID=2, TID=prevent_4|SID=2, TID=prevent_5 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dprevent_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dprevent_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dprevent_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dprevent_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D2-TID%3Dprevent_5.png)|

| SID=3, TID=cause_0| SID=3, TID=cause_1| SID=3, TID=cause_2 | SID=3, TID=cause_3|SID=3, TID=cause_4 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dcause_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dcause_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dcause_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dcause_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dcause_4.png)|

| SID=3, TID=cause_5| SID=3, TID=counterfactual_0| SID=3, TID=counterfactual_1 | SID=3, TID=counterfactual_2|SID=3, TID=counterfactual_3 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dcause_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dcounterfactual_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dcounterfactual_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dcounterfactual_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dcounterfactual_3.png)|

| SID=3, TID=counterfactual_4| SID=3, TID=counterfactual_5| SID=3, TID=counterfactual_6 | SID=3, TID=counterfactual_7|SID=3, TID=counterfactual_8 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dcounterfactual_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dcounterfactual_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dcounterfactual_6.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dcounterfactual_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dcounterfactual_8.png)|

| SID=3, TID=descriptive_0| SID=3, TID=descriptive_1| SID=3, TID=descriptive_10 | SID=3, TID=descriptive_11|SID=3, TID=descriptive_12 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_10.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_11.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_12.png)|

| SID=3, TID=descriptive_13| SID=3, TID=descriptive_14| SID=3, TID=descriptive_15 | SID=3, TID=descriptive_16|SID=3, TID=descriptive_17 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_13.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_14.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_15.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_16.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_17.png)|

| SID=3, TID=descriptive_18| SID=3, TID=descriptive_19| SID=3, TID=descriptive_2 | SID=3, TID=descriptive_20|SID=3, TID=descriptive_21 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_18.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_19.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_20.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_21.png)|

| SID=3, TID=descriptive_22| SID=3, TID=descriptive_23| SID=3, TID=descriptive_24 | SID=3, TID=descriptive_25|SID=3, TID=descriptive_26 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_22.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_23.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_24.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_25.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_26.png)|

| SID=3, TID=descriptive_27| SID=3, TID=descriptive_28| SID=3, TID=descriptive_29 | SID=3, TID=descriptive_3|SID=3, TID=descriptive_30 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_27.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_28.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_29.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_30.png)|

| SID=3, TID=descriptive_31| SID=3, TID=descriptive_32| SID=3, TID=descriptive_33 | SID=3, TID=descriptive_34|SID=3, TID=descriptive_35 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_31.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_32.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_33.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_34.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_35.png)|

| SID=3, TID=descriptive_36| SID=3, TID=descriptive_37| SID=3, TID=descriptive_4 | SID=3, TID=descriptive_5|SID=3, TID=descriptive_6 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_36.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_37.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_6.png)|

| SID=3, TID=descriptive_7| SID=3, TID=descriptive_8| SID=3, TID=descriptive_9 | SID=3, TID=enable_0|SID=3, TID=enable_1 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_8.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Ddescriptive_9.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Denable_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Denable_1.png)|

| SID=3, TID=enable_2| SID=3, TID=enable_3| SID=3, TID=enable_4 | SID=3, TID=enable_5|SID=3, TID=prevent_0 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Denable_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Denable_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Denable_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Denable_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dprevent_0.png)|

| SID=3, TID=prevent_1| SID=3, TID=prevent_2| SID=3, TID=prevent_3 | SID=3, TID=prevent_4|SID=3, TID=prevent_5 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dprevent_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dprevent_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dprevent_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dprevent_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D3-TID%3Dprevent_5.png)|

| SID=4, TID=cause_0| SID=4, TID=cause_1| SID=4, TID=cause_2 | SID=4, TID=cause_3|SID=4, TID=cause_4 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dcause_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dcause_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dcause_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dcause_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dcause_4.png)|

| SID=4, TID=cause_5| SID=4, TID=counterfactual_0| SID=4, TID=counterfactual_1 | SID=4, TID=counterfactual_2|SID=4, TID=counterfactual_3 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dcause_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dcounterfactual_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dcounterfactual_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dcounterfactual_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dcounterfactual_3.png)|

| SID=4, TID=counterfactual_4| SID=4, TID=counterfactual_5| SID=4, TID=counterfactual_6 | SID=4, TID=counterfactual_7|SID=4, TID=counterfactual_8 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dcounterfactual_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dcounterfactual_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dcounterfactual_6.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dcounterfactual_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dcounterfactual_8.png)|

| SID=4, TID=descriptive_0| SID=4, TID=descriptive_1| SID=4, TID=descriptive_10 | SID=4, TID=descriptive_11|SID=4, TID=descriptive_12 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_10.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_11.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_12.png)|

| SID=4, TID=descriptive_13| SID=4, TID=descriptive_14| SID=4, TID=descriptive_15 | SID=4, TID=descriptive_16|SID=4, TID=descriptive_17 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_13.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_14.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_15.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_16.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_17.png)|

| SID=4, TID=descriptive_18| SID=4, TID=descriptive_19| SID=4, TID=descriptive_2 | SID=4, TID=descriptive_20|SID=4, TID=descriptive_21 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_18.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_19.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_20.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_21.png)|

| SID=4, TID=descriptive_22| SID=4, TID=descriptive_23| SID=4, TID=descriptive_24 | SID=4, TID=descriptive_25|SID=4, TID=descriptive_26 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_22.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_23.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_24.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_25.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_26.png)|

| SID=4, TID=descriptive_27| SID=4, TID=descriptive_28| SID=4, TID=descriptive_29 | SID=4, TID=descriptive_3|SID=4, TID=descriptive_30 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_27.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_28.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_29.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_30.png)|

| SID=4, TID=descriptive_31| SID=4, TID=descriptive_32| SID=4, TID=descriptive_33 | SID=4, TID=descriptive_34|SID=4, TID=descriptive_35 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_31.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_32.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_33.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_34.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_35.png)|

| SID=4, TID=descriptive_36| SID=4, TID=descriptive_37| SID=4, TID=descriptive_4 | SID=4, TID=descriptive_5|SID=4, TID=descriptive_6 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_36.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_37.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_6.png)|

| SID=4, TID=descriptive_7| SID=4, TID=descriptive_8| SID=4, TID=descriptive_9 | SID=4, TID=enable_0|SID=4, TID=enable_1 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_8.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Ddescriptive_9.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Denable_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Denable_1.png)|

| SID=4, TID=enable_2| SID=4, TID=enable_3| SID=4, TID=enable_4 | SID=4, TID=enable_5|SID=4, TID=prevent_0 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Denable_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Denable_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Denable_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Denable_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dprevent_0.png)|

| SID=4, TID=prevent_1| SID=4, TID=prevent_2| SID=4, TID=prevent_3 | SID=4, TID=prevent_4|SID=4, TID=prevent_5 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dprevent_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dprevent_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dprevent_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dprevent_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D4-TID%3Dprevent_5.png)|

| SID=5, TID=cause_0| SID=5, TID=cause_1| SID=5, TID=cause_2 | SID=5, TID=cause_3|SID=5, TID=cause_4 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dcause_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dcause_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dcause_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dcause_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dcause_4.png)|

| SID=5, TID=cause_5| SID=5, TID=counterfactual_0| SID=5, TID=counterfactual_1 | SID=5, TID=counterfactual_2|SID=5, TID=counterfactual_3 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dcause_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dcounterfactual_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dcounterfactual_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dcounterfactual_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dcounterfactual_3.png)|

| SID=5, TID=counterfactual_4| SID=5, TID=counterfactual_5| SID=5, TID=counterfactual_6 | SID=5, TID=counterfactual_7|SID=5, TID=counterfactual_8 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dcounterfactual_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dcounterfactual_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dcounterfactual_6.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dcounterfactual_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dcounterfactual_8.png)|

| SID=5, TID=descriptive_0| SID=5, TID=descriptive_1| SID=5, TID=descriptive_10 | SID=5, TID=descriptive_11|SID=5, TID=descriptive_12 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_10.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_11.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_12.png)|

| SID=5, TID=descriptive_13| SID=5, TID=descriptive_14| SID=5, TID=descriptive_15 | SID=5, TID=descriptive_16|SID=5, TID=descriptive_17 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_13.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_14.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_15.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_16.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_17.png)|

| SID=5, TID=descriptive_18| SID=5, TID=descriptive_19| SID=5, TID=descriptive_2 | SID=5, TID=descriptive_20|SID=5, TID=descriptive_21 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_18.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_19.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_20.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_21.png)|

| SID=5, TID=descriptive_22| SID=5, TID=descriptive_23| SID=5, TID=descriptive_24 | SID=5, TID=descriptive_25|SID=5, TID=descriptive_26 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_22.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_23.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_24.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_25.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_26.png)|

| SID=5, TID=descriptive_27| SID=5, TID=descriptive_28| SID=5, TID=descriptive_29 | SID=5, TID=descriptive_3|SID=5, TID=descriptive_30 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_27.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_28.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_29.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_30.png)|

| SID=5, TID=descriptive_31| SID=5, TID=descriptive_32| SID=5, TID=descriptive_33 | SID=5, TID=descriptive_34|SID=5, TID=descriptive_35 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_31.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_32.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_33.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_34.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_35.png)|

| SID=5, TID=descriptive_36| SID=5, TID=descriptive_37| SID=5, TID=descriptive_4 | SID=5, TID=descriptive_5|SID=5, TID=descriptive_6 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_36.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_37.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_6.png)|

| SID=5, TID=descriptive_7| SID=5, TID=descriptive_8| SID=5, TID=descriptive_9 | SID=5, TID=enable_0|SID=5, TID=enable_1 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_8.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Ddescriptive_9.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Denable_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Denable_1.png)|

| SID=5, TID=enable_2| SID=5, TID=enable_3| SID=5, TID=enable_4 | SID=5, TID=enable_5|SID=5, TID=prevent_0 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Denable_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Denable_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Denable_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Denable_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dprevent_0.png)|

| SID=5, TID=prevent_1| SID=5, TID=prevent_2| SID=5, TID=prevent_3 | SID=5, TID=prevent_4|SID=5, TID=prevent_5 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dprevent_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dprevent_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dprevent_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dprevent_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D5-TID%3Dprevent_5.png)|

| SID=6, TID=cause_0| SID=6, TID=cause_1| SID=6, TID=cause_2 | SID=6, TID=cause_3|SID=6, TID=cause_4 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dcause_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dcause_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dcause_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dcause_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dcause_4.png)|

| SID=6, TID=cause_5| SID=6, TID=counterfactual_0| SID=6, TID=counterfactual_1 | SID=6, TID=counterfactual_2|SID=6, TID=counterfactual_3 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dcause_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dcounterfactual_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dcounterfactual_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dcounterfactual_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dcounterfactual_3.png)|

| SID=6, TID=counterfactual_4| SID=6, TID=counterfactual_5| SID=6, TID=counterfactual_6 | SID=6, TID=counterfactual_7|SID=6, TID=counterfactual_8 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dcounterfactual_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dcounterfactual_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dcounterfactual_6.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dcounterfactual_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dcounterfactual_8.png)|

| SID=6, TID=descriptive_0| SID=6, TID=descriptive_1| SID=6, TID=descriptive_10 | SID=6, TID=descriptive_11|SID=6, TID=descriptive_12 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_10.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_11.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_12.png)|

| SID=6, TID=descriptive_13| SID=6, TID=descriptive_14| SID=6, TID=descriptive_15 | SID=6, TID=descriptive_16|SID=6, TID=descriptive_17 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_13.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_14.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_15.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_16.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_17.png)|

| SID=6, TID=descriptive_18| SID=6, TID=descriptive_19| SID=6, TID=descriptive_2 | SID=6, TID=descriptive_20|SID=6, TID=descriptive_21 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_18.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_19.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_20.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_21.png)|

| SID=6, TID=descriptive_22| SID=6, TID=descriptive_23| SID=6, TID=descriptive_24 | SID=6, TID=descriptive_25|SID=6, TID=descriptive_26 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_22.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_23.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_24.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_25.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_26.png)|

| SID=6, TID=descriptive_27| SID=6, TID=descriptive_28| SID=6, TID=descriptive_29 | SID=6, TID=descriptive_3|SID=6, TID=descriptive_30 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_27.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_28.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_29.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_30.png)|

| SID=6, TID=descriptive_31| SID=6, TID=descriptive_32| SID=6, TID=descriptive_33 | SID=6, TID=descriptive_34|SID=6, TID=descriptive_35 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_31.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_32.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_33.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_34.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_35.png)|

| SID=6, TID=descriptive_36| SID=6, TID=descriptive_37| SID=6, TID=descriptive_4 | SID=6, TID=descriptive_5|SID=6, TID=descriptive_6 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_36.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_37.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_6.png)|

| SID=6, TID=descriptive_7| SID=6, TID=descriptive_8| SID=6, TID=descriptive_9 | SID=6, TID=enable_0|SID=6, TID=enable_1 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_8.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Ddescriptive_9.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Denable_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Denable_1.png)|

| SID=6, TID=enable_2| SID=6, TID=enable_3| SID=6, TID=enable_4 | SID=6, TID=enable_5|SID=6, TID=prevent_0 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Denable_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Denable_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Denable_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Denable_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dprevent_0.png)|

| SID=6, TID=prevent_1| SID=6, TID=prevent_2| SID=6, TID=prevent_3 | SID=6, TID=prevent_4|SID=6, TID=prevent_5 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dprevent_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dprevent_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dprevent_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dprevent_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D6-TID%3Dprevent_5.png)|

| SID=7, TID=cause_0| SID=7, TID=cause_1| SID=7, TID=cause_2 | SID=7, TID=cause_3|SID=7, TID=cause_4 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dcause_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dcause_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dcause_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dcause_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dcause_4.png)|

| SID=7, TID=cause_5| SID=7, TID=counterfactual_0| SID=7, TID=counterfactual_1 | SID=7, TID=counterfactual_2|SID=7, TID=counterfactual_3 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dcause_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dcounterfactual_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dcounterfactual_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dcounterfactual_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dcounterfactual_3.png)|

| SID=7, TID=counterfactual_4| SID=7, TID=counterfactual_5| SID=7, TID=counterfactual_6 | SID=7, TID=counterfactual_7|SID=7, TID=counterfactual_8 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dcounterfactual_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dcounterfactual_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dcounterfactual_6.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dcounterfactual_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dcounterfactual_8.png)|

| SID=7, TID=descriptive_0| SID=7, TID=descriptive_1| SID=7, TID=descriptive_10 | SID=7, TID=descriptive_11|SID=7, TID=descriptive_12 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_10.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_11.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_12.png)|

| SID=7, TID=descriptive_13| SID=7, TID=descriptive_14| SID=7, TID=descriptive_15 | SID=7, TID=descriptive_16|SID=7, TID=descriptive_17 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_13.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_14.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_15.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_16.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_17.png)|

| SID=7, TID=descriptive_18| SID=7, TID=descriptive_19| SID=7, TID=descriptive_2 | SID=7, TID=descriptive_20|SID=7, TID=descriptive_21 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_18.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_19.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_20.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_21.png)|

| SID=7, TID=descriptive_22| SID=7, TID=descriptive_23| SID=7, TID=descriptive_24 | SID=7, TID=descriptive_25|SID=7, TID=descriptive_26 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_22.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_23.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_24.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_25.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_26.png)|

| SID=7, TID=descriptive_27| SID=7, TID=descriptive_28| SID=7, TID=descriptive_29 | SID=7, TID=descriptive_3|SID=7, TID=descriptive_30 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_27.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_28.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_29.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_30.png)|

| SID=7, TID=descriptive_31| SID=7, TID=descriptive_32| SID=7, TID=descriptive_33 | SID=7, TID=descriptive_34|SID=7, TID=descriptive_35 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_31.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_32.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_33.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_34.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_35.png)|

| SID=7, TID=descriptive_36| SID=7, TID=descriptive_37| SID=7, TID=descriptive_4 | SID=7, TID=descriptive_5|SID=7, TID=descriptive_6 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_36.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_37.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_6.png)|

| SID=7, TID=descriptive_7| SID=7, TID=descriptive_8| SID=7, TID=descriptive_9 | SID=7, TID=enable_0|SID=7, TID=enable_1 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_8.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Ddescriptive_9.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Denable_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Denable_1.png)|

| SID=7, TID=enable_2| SID=7, TID=enable_3| SID=7, TID=enable_4 | SID=7, TID=enable_5|SID=7, TID=prevent_0 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Denable_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Denable_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Denable_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Denable_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dprevent_0.png)|

| SID=7, TID=prevent_1| SID=7, TID=prevent_2| SID=7, TID=prevent_3 | SID=7, TID=prevent_4|SID=7, TID=prevent_5 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dprevent_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dprevent_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dprevent_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dprevent_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D7-TID%3Dprevent_5.png)|

| SID=8, TID=cause_0| SID=8, TID=cause_1| SID=8, TID=cause_2 | SID=8, TID=cause_3|SID=8, TID=cause_4 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dcause_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dcause_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dcause_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dcause_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dcause_4.png)|

| SID=8, TID=cause_5| SID=8, TID=counterfactual_0| SID=8, TID=counterfactual_1 | SID=8, TID=counterfactual_2|SID=8, TID=counterfactual_3 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dcause_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dcounterfactual_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dcounterfactual_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dcounterfactual_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dcounterfactual_3.png)|

| SID=8, TID=counterfactual_4| SID=8, TID=counterfactual_5| SID=8, TID=counterfactual_6 | SID=8, TID=counterfactual_7|SID=8, TID=counterfactual_8 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dcounterfactual_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dcounterfactual_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dcounterfactual_6.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dcounterfactual_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dcounterfactual_8.png)|

| SID=8, TID=descriptive_0| SID=8, TID=descriptive_1| SID=8, TID=descriptive_10 | SID=8, TID=descriptive_11|SID=8, TID=descriptive_12 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_10.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_11.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_12.png)|

| SID=8, TID=descriptive_13| SID=8, TID=descriptive_14| SID=8, TID=descriptive_15 | SID=8, TID=descriptive_16|SID=8, TID=descriptive_17 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_13.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_14.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_15.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_16.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_17.png)|

| SID=8, TID=descriptive_18| SID=8, TID=descriptive_19| SID=8, TID=descriptive_2 | SID=8, TID=descriptive_20|SID=8, TID=descriptive_21 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_18.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_19.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_20.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_21.png)|

| SID=8, TID=descriptive_22| SID=8, TID=descriptive_23| SID=8, TID=descriptive_24 | SID=8, TID=descriptive_25|SID=8, TID=descriptive_26 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_22.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_23.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_24.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_25.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_26.png)|

| SID=8, TID=descriptive_27| SID=8, TID=descriptive_28| SID=8, TID=descriptive_29 | SID=8, TID=descriptive_3|SID=8, TID=descriptive_30 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_27.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_28.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_29.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_30.png)|

| SID=8, TID=descriptive_31| SID=8, TID=descriptive_32| SID=8, TID=descriptive_33 | SID=8, TID=descriptive_34|SID=8, TID=descriptive_35 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_31.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_32.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_33.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_34.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_35.png)|

| SID=8, TID=descriptive_36| SID=8, TID=descriptive_37| SID=8, TID=descriptive_4 | SID=8, TID=descriptive_5|SID=8, TID=descriptive_6 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_36.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_37.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_6.png)|

| SID=8, TID=descriptive_7| SID=8, TID=descriptive_8| SID=8, TID=descriptive_9 | SID=8, TID=enable_0|SID=8, TID=enable_1 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_8.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Ddescriptive_9.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Denable_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Denable_1.png)|

| SID=8, TID=enable_2| SID=8, TID=enable_3| SID=8, TID=enable_4 | SID=8, TID=enable_5|SID=8, TID=prevent_0 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Denable_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Denable_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Denable_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Denable_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dprevent_0.png)|

| SID=8, TID=prevent_1| SID=8, TID=prevent_2| SID=8, TID=prevent_3 | SID=8, TID=prevent_4|SID=8, TID=prevent_5 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dprevent_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dprevent_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dprevent_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dprevent_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D8-TID%3Dprevent_5.png)|

| SID=9, TID=cause_0| SID=9, TID=cause_1| SID=9, TID=cause_2 | SID=9, TID=cause_3|SID=9, TID=cause_4 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dcause_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dcause_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dcause_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dcause_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dcause_4.png)|

| SID=9, TID=cause_5| SID=9, TID=counterfactual_0| SID=9, TID=counterfactual_1 | SID=9, TID=counterfactual_2|SID=9, TID=counterfactual_3 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dcause_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dcounterfactual_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dcounterfactual_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dcounterfactual_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dcounterfactual_3.png)|

| SID=9, TID=counterfactual_4| SID=9, TID=counterfactual_5| SID=9, TID=counterfactual_6 | SID=9, TID=counterfactual_7|SID=9, TID=counterfactual_8 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dcounterfactual_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dcounterfactual_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dcounterfactual_6.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dcounterfactual_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dcounterfactual_8.png)|

| SID=9, TID=descriptive_0| SID=9, TID=descriptive_1| SID=9, TID=descriptive_10 | SID=9, TID=descriptive_11|SID=9, TID=descriptive_12 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_10.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_11.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_12.png)|

| SID=9, TID=descriptive_13| SID=9, TID=descriptive_14| SID=9, TID=descriptive_15 | SID=9, TID=descriptive_16|SID=9, TID=descriptive_17 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_13.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_14.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_15.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_16.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_17.png)|

| SID=9, TID=descriptive_18| SID=9, TID=descriptive_19| SID=9, TID=descriptive_2 | SID=9, TID=descriptive_20|SID=9, TID=descriptive_21 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_18.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_19.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_20.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_21.png)|

| SID=9, TID=descriptive_22| SID=9, TID=descriptive_23| SID=9, TID=descriptive_24 | SID=9, TID=descriptive_25|SID=9, TID=descriptive_26 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_22.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_23.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_24.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_25.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_26.png)|

| SID=9, TID=descriptive_27| SID=9, TID=descriptive_28| SID=9, TID=descriptive_29 | SID=9, TID=descriptive_3|SID=9, TID=descriptive_30 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_27.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_28.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_29.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_30.png)|

| SID=9, TID=descriptive_31| SID=9, TID=descriptive_32| SID=9, TID=descriptive_33 | SID=9, TID=descriptive_34|SID=9, TID=descriptive_35 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_31.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_32.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_33.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_34.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_35.png)|

| SID=9, TID=descriptive_36| SID=9, TID=descriptive_37| SID=9, TID=descriptive_4 | SID=9, TID=descriptive_5|SID=9, TID=descriptive_6 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_36.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_37.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_6.png)|

| SID=9, TID=descriptive_7| SID=9, TID=descriptive_8| SID=9, TID=descriptive_9 | SID=9, TID=enable_0|SID=9, TID=enable_1 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_8.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Ddescriptive_9.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Denable_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Denable_1.png)|

| SID=9, TID=enable_2| SID=9, TID=enable_3| SID=9, TID=enable_4 | SID=9, TID=enable_5|SID=9, TID=prevent_0 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Denable_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Denable_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Denable_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Denable_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dprevent_0.png)|

| SID=9, TID=prevent_1| SID=9, TID=prevent_2| SID=9, TID=prevent_3 | SID=9, TID=prevent_4|SID=9, TID=prevent_5 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dprevent_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dprevent_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dprevent_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dprevent_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D9-TID%3Dprevent_5.png)|

| SID=10, TID=cause_0| SID=10, TID=cause_1| SID=10, TID=cause_2 | SID=10, TID=cause_3|SID=10, TID=cause_4 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dcause_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dcause_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dcause_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dcause_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dcause_4.png)|

| SID=10, TID=cause_5| SID=10, TID=counterfactual_0| SID=10, TID=counterfactual_1 | SID=10, TID=counterfactual_2|SID=10, TID=counterfactual_3 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dcause_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dcounterfactual_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dcounterfactual_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dcounterfactual_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dcounterfactual_3.png)|

| SID=10, TID=counterfactual_4| SID=10, TID=counterfactual_5| SID=10, TID=counterfactual_6 | SID=10, TID=counterfactual_7|SID=10, TID=counterfactual_8 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dcounterfactual_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dcounterfactual_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dcounterfactual_6.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dcounterfactual_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dcounterfactual_8.png)|

| SID=10, TID=descriptive_0| SID=10, TID=descriptive_1| SID=10, TID=descriptive_10 | SID=10, TID=descriptive_11|SID=10, TID=descriptive_12 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_10.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_11.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_12.png)|

| SID=10, TID=descriptive_13| SID=10, TID=descriptive_14| SID=10, TID=descriptive_15 | SID=10, TID=descriptive_16|SID=10, TID=descriptive_17 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_13.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_14.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_15.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_16.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_17.png)|

| SID=10, TID=descriptive_18| SID=10, TID=descriptive_19| SID=10, TID=descriptive_2 | SID=10, TID=descriptive_20|SID=10, TID=descriptive_21 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_18.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_19.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_20.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_21.png)|

| SID=10, TID=descriptive_22| SID=10, TID=descriptive_23| SID=10, TID=descriptive_24 | SID=10, TID=descriptive_25|SID=10, TID=descriptive_26 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_22.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_23.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_24.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_25.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_26.png)|

| SID=10, TID=descriptive_27| SID=10, TID=descriptive_28| SID=10, TID=descriptive_29 | SID=10, TID=descriptive_3|SID=10, TID=descriptive_30 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_27.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_28.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_29.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_30.png)|

| SID=10, TID=descriptive_31| SID=10, TID=descriptive_32| SID=10, TID=descriptive_33 | SID=10, TID=descriptive_34|SID=10, TID=descriptive_35 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_31.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_32.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_33.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_34.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_35.png)|

| SID=10, TID=descriptive_36| SID=10, TID=descriptive_37| SID=10, TID=descriptive_4 | SID=10, TID=descriptive_5|SID=10, TID=descriptive_6 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_36.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_37.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_6.png)|

| SID=10, TID=descriptive_7| SID=10, TID=descriptive_8| SID=10, TID=descriptive_9 | SID=10, TID=enable_0|SID=10, TID=enable_1 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_7.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_8.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Ddescriptive_9.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Denable_0.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Denable_1.png)|

| SID=10, TID=enable_2| SID=10, TID=enable_3| SID=10, TID=enable_4 | SID=10, TID=enable_5|SID=10, TID=prevent_0 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Denable_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Denable_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Denable_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Denable_5.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dprevent_0.png)|

| SID=10, TID=prevent_1| SID=10, TID=prevent_2| SID=10, TID=prevent_3 | SID=10, TID=prevent_4|SID=10, TID=prevent_5 |
|---|---|---|---|---|
|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dprevent_1.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dprevent_2.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dprevent_3.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dprevent_4.png)|![](/dataset/outputs/stats/Dataset_v230920/SID%3D10-TID%3Dprevent_5.png)|


### Future Work

- Currently, our programs of tasks depend on the end results of the simulations to be able to provide correct answers to the questions. As an example, consider the following prevent task, "Does the **Z** **C** **S** **prevent** the **Z2** **C2** **S2** from **falling to** the **ground**?". For the answer of this question to be "true", we check the end state of the object **Z2** **C2** **S2** to observe whether it falls to the ground or not. Our programs do not consider local temporal attemps of the object **Z** **C** **S** whether it is trying to prevent in a small time interval. Therefore, our questions do not integrate verbs like "impede", "interfere" or "restrain" instead of "prevent" in different tasks. Similarly, verbs like "help", "aid" or "facilitate" are not integrated instead of "enable".

- We consider events of entering the basket, but our objects inside our simulations are not able get out of the basket. It would be interesting to create such scenes detecting the exit events.

- There can be multiple patients in cause, enable, and prevent tasks, but there cannot be multiple affectors.

- Properties such as object mass can be integrated using material textures.

- Human performance evaluation.

- Other answer types for counterfactual, cause, enable and prevent questions.


