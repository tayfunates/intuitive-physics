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

## Input and Output Data Types of Functional Modules

- Object: A dictionary holding static and dynamic properties of an object at a time step
- ObjectSet: A list of unique objects
- ObjectSetList: A list of ObjectSet
- Event: A dictionary holding information of a specific event: id, type, time step, participating objects
- EventSet: A list of unique events
- EventSetList: A list of EventSet
- ![RED] Order: A tag indicating chronological ordering of events: such as first, second and last
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
  
We do not have any other side inputs now, but there may some in the future, such as Order type in Clevrer.

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
| FilterStartTouching  | Returns start touching events from the input list | EventSet | EventSet | ![BLUE]  |
| FilterEndTouching  | Returns end touching events from the input list | EventSet | EventSet | ![BLUE]  |
| FilterBefore  | Returns events from the input list that happened before input event  | EventSet, Event  | EventSet  | ![BLUE]  |
| FilterMoving  | Returns objects if they are moving at step specified by an Integer   | ObjectSet, Integer  | ObjectSet  | ![Green]  |
| FilterAfter  | Returns events from the input list that happened after input event  | EventSet, Event  | EventSet  | ![BLUE]  |
| FilterFirst  | Returns the first event from the input list  | EventSet  | Event  | ![GREEN]  |
| FilterUnique  | Returns unique object from input list with possible side inputs Size, Color, Shape  | Objects, ObjectSideInputs | Object  | ![GREEN]  |
| Unique  | Returns the single object from the input list, if list has more than one elements returns INVALID  | Objects | Object  | ![GREEN]  |
| EventPartner (CE, STE, ETE) | Returns object from the object list of the input event which is not input object  | Event, Object  | Object  | ![GREEN]  |
| QueryColor  | Returns the color of the input object  | Object  | Color  | ![GREEN]  |
| QueryShape  | Returns the shape of the input object  | Object  | Shape  | ![GREEN]  |
| Count  | Returns size of the input list  | ObjectSet, EventSet  | Integer  | ![GREEN] for ObjectSet ![BLUE] for EventSet |
| Exist  | Returns true if the input list is not empty  | ObjectSet, EventSet  | Bool  | ![GREEN] for ObjectSet ![BLUE] for EventSet |
| ExistList  | Applies Exist to each item in input list returning a list of Bool | ObjectSetList | BoolList  | ![GREEN] for ObjectSetList ![BLUE] for EventSetList |
| AnyFalse  | Returns true if there is at least one false in a bool list | BoolList  | Bool | ![GREEN] |
| FilterCollideGround  | Returns objects which collides to ground in a specific event set   | EventSet  | ObjectSet  | ![Green]  |
| FilterEnterContainer  | Returns objects which enters to unique container in a specific event set   | EventSet  | ObjectSet  | ![Green]  |
| FilterEnterContainerList  | Applies FilterEnterContainer to each item in a list of event set | EventSetList  | ObjectSetList  | ![Green]  |
| GetCounterfactEvents  | Returns event list if a specific object is removed from the scene   | Object  | EventSet  | ![Green]  |
| GetCounterfactEventsList  | Returns event list for all objects in an object set | ObjectSet  | EventSetList  | ![Green]  |
| FilterDynamic  | Returns dynamic objects from an object set   | ObjectSet  | ObjectSet  | ![Green]  |
| AsList  | Returns single elemen object set created with a specific object | Object | ObjectSet  | ![GREEN] |

Other clevrer filters that are needed to be discussed.
- ![RED]: FilterStationary: Selects all stationary objects in the input frame
or the entire video (when input frame is “null”)
- ![RED]: FilterIn: Selects all incoming events of the input objects
- ![RED]: FilterOut: Selects all exiting events of the input objects

## Questions

![CYAN] Cevap çeşidine bir an önce karar vermek gerekiyor. CLEVR'dan farklı bir yol izleyeceksek (CLEVRER gibi mesela), şimdiden onunla uğraşmalıyız, soru yaratmadan önce.

### Structures Provided to Question Generation Engine

- Scene information at start (SceneAtStart): Holds objects' static and dynamic information at start of the video, color, position, shape, velocity etc.
- Scene information at end (SceneAtEnd): Holds objects' static and dynamic information at end of the video, color, position, shape, velocity etc.
- Causal graph (CausalGraph): Graph constructed by events of objects as nodes. All events causing a specific event are the ancestors of that event.

### Samples

#### Descriptive

##### Query Color

| Question  |  Program | Output Type  | Implementation Status |
|---|---|---|---|
| "What color is the object that first collides with **Z** **C** **S**?", "What is the color of object that first collides with **Z** **C** **S**?", "There is an object that first collides with **Z** **C** **S**; what color is it?", "There is an object that first collides with **Z** **C** **S**; what is its color?" | QueryColor( EventPartner( FilterFirst( FilterCollision( Events, FilterUnique( SceneAtStart, **Z** **C** **S** ) ) ), FilterUnique( SceneAtStart, **Z** **C** **S** ) ) ) | Color | ![GREEN] |


| Question | Answer | Original Video|
|---|---|---|
|"What color is the object that first collides with big purple circle?"|"green"|![](/dataset/examples/ExampleScene9.gif)|

##### Query Shape

| Question  |  Program | Output Type  | Implementation Status |
|---|---|---|---|
| "What shape is the object that first collides with **Z** **C** **S**?", "What is the shape of object that first collides with **Z** **C** **S**?", "There is an object that first collides with **Z** **C** **S**; what shape is it?", "There is an object that first collides with **Z** **C** **S**; what is its shape?" | QueryShape( EventPartner( FilterFirst( FilterCollision( Events, FilterUnique( SceneAtStart, **Z** **C** **S** ) ) ), FilterUnique( SceneAtStart, **Z** **C** **S** ) ) ) | Shape | ![GREEN] |


##### Counting

| Question  |  Program | Output Type  | Implementation Status |
|---|---|---|---|
| "How many **S**s are moving when the video ends?" | Count( FilterMoving( FilterShape( SceneAtEnd, **S**) , EndSceneStep ) ) | Integer | ![GREEN] |
| "How many **C** objects are moving when the video ends?" | Count( FilterMoving( FilterColor( SceneAtEnd, **C**) , EndSceneStep ) ) | Integer | ![GREEN] |
| "How many **Z** objects are moving when the video ends?" | Count( FilterMoving( FilterColor( SceneAtEnd, **Z**) , EndSceneStep ) ) | Integer | ![GREEN] |

![CYAN] Counting için, oluşturalacak sahnelerde hardcoded shape, color, size kullanmamak gerekiyor, atıyorum sadece circlelardan oluşan simulation gibi. Çünkü sahnede olmayan elemanların sayısı çok olmaya başlayınca 0 cevabının yoğunluğu artıyor olacak. 

![CYAN] Prevent/enable için ne gibi assumption olacak? Bu assumptionlar farklı sahneler için yeterince genericlik sağlayacak mı yoksa her simulation için farklı set of questions mı olacak?

##### Enable

| Question  |  Program | Output Type  | Implementation Status |
|---|---|---|---|
| "Does the **Z** **C** **S** enable the **Z2** **C2** **S2** to collide with the ground?", "Does the **Z** **C** **S** enable the collision between the **Z2** **C2** **S2** and the ground?", "There is a **Z** **C** **S**, does it enable **Z2** **C2** **S2** to collide with the ground?", "Is the **Z** **C** **S** responsible for the collision between the **Z2** **C2** **S2** and the ground?" | **TODO**  | Bool | ![GREEN] |
| "Does the **Z** **C** **S** enable the **Z2** **C2** **S2** to enter the basket?", "There is a **Z** **C** **S**, does it enable the **Z2** **C2** **S2** to enter the basket?" | **TODO**  | Bool | ![GREEN] |
| "Is there any object which enables the **Z** **C** **S** to enter the basket?", "Are there any objects which enable the **Z** **C** **S** to enter the basket?" | **TODO**  | Bool | ![GREEN] |
| "How many objects does the **Z** **C** **S** enable to enter the basket?", "What is the number of objects that the **Z** **C** **S** enable to enter the basket?" | **TODO**  | Integer | ![GREEN] |
| "How many objects does the **Z** **C** **S** enable to collide with the ground?", "What is the number of objects that the **Z** **C** **S** enable to collide with the ground?" | **TODO**  | Integer | ![GREEN] |


| Question | Answer | Original Video| Variation Video |
|---|---|---|---|
|"Is the large green block responsible for the collision between the tiny blue block and the ground?"|"true"|![](/dataset/examples/ExampleScene1.gif)|![](/dataset/examples/ExampleScene1Variation1.gif)|
|"Does the big brown block enable the large cyan circle to enter the basket?"|"true"|![](/dataset/examples/ExampleScene2.gif)|![](/dataset/examples/ExampleScene2Variation1.gif)|
|"There is a tiny purple cube, does it enable the big cyan circle to enter the basket?"|"false"|![](/dataset/examples/ExampleScene2.gif)|![](/dataset/examples/ExampleScene2Variation2.gif)|
|"Is there any object which enables the big red circle to enter the basket?"|"false"|![](/dataset/examples/ExampleScene3.gif)| <table> <tbody>  <tr>  <td>![](/dataset/examples/ExampleScene3Variation1.gif)</td>  <td>![](/dataset/examples/ExampleScene3Variation3.gif)</td>  </tr>  <tr>  <td>![](/dataset/examples/ExampleScene3Variation4.gif)</td>  <td>![](/dataset/examples/ExampleScene3Variation5.gif)</td>  </tr>  <tr>  </tbody>  </table> |
|"Are there any objects which enable the small brown cube to enter the basket?"|"true"|![](/dataset/examples/ExampleScene3.gif)|![](/dataset/examples/ExampleScene3Variation2.gif)|
|"How many objects does the big yellow circle enable to enter the basket?"|"2"|![](/dataset/examples/ExampleScene4.gif)|![](/dataset/examples/ExampleScene4Variation1.gif)|
|"What is the number of objects that the big red circle enable to collide with the ground?"|"0"|![](/dataset/examples/ExampleScene5.gif)|![](/dataset/examples/ExampleScene5Variation1.gif)|
|"Is there any object which enables the small green circle to enter the basket?"|"**true**"|![](/dataset/examples/ExampleScene7.gif)|![](/dataset/examples/ExampleScene7Variation1.gif)|
|"What is the number of objects that the large cyan circle enable to collide with the ground?"|"1"|![](/dataset/examples/ExampleScene8.gif)|![](/dataset/examples/ExampleScene8Variation1.gif)|
|"There is a tiny red circle, does it enable the small purple circle to enter the basket?"|"**true**"|![](/dataset/examples/ExampleScene10.gif)|![](/dataset/examples/ExampleScene10Variation1.gif)|
  
##### Prevent

| Question  |  Program | Output Type  | Implementation Status |
|---|---|---|---|
| "Does the **Z** **C** **S** prevent the **Z2** **C2** **S2** from colliding with the ground?" | **TODO**  | Bool | ![GREEN] |
| "Does the **Z** **C** **S** prevent the **Z2** **C2** **S2** from entering to the basket?" | **TODO**  | Bool | ![GREEN] |

| Question | Answer | Original Video| Variation Video |
|---|---|---|---|
|"Does the large green block prevent the small red block from colliding with the ground?"|"true"|![](/dataset/examples/ExampleScene1.gif)|![](/dataset/examples/ExampleScene1Variation1.gif)|
|"Does the big yellow cube prevent the small blue triangle from entering to the basket?"|"true"|![](/dataset/examples/ExampleScene2.gif)|![](/dataset/examples/ExampleScene2Variation3.gif)|
|"Does the tiny purple circle prevent the big blue circle from entering to the basket?"|"true"|![](/dataset/examples/ExampleScene6.gif)|![](/dataset/examples/ExampleScene6Variation1.gif)|
|"Does the large cyan circle prevent the tiny brown circle from entering to the basket?"|"true"|![](/dataset/examples/ExampleScene8.gif)|![](/dataset/examples/ExampleScene8Variation1.gif)|
|"Does the large purple circle prevent the small green circle from entering to the basket?"|"true"|![](/dataset/examples/ExampleScene9.gif)|![](/dataset/examples/ExampleScene9Variation1.gif)|


