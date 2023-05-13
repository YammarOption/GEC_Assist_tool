# GEC Assist Tool
The GEC Assist Tool is a graphical tool to keep track of the  progress made during the Get Everything Challenge in Pokémon. The tool allows to easily monitor the progress throughout the game without the need to memorize the progress made.

The tool allow for the control all of following requirements, needed to complete the GEC challenge:

### 1.  All Pokémons
![image](/img/Main_bar_1.png)

The first requirement of the challenge is to **catch all the pokémon** in the regional dex and obtain a *living dex*. The tool allows users to easily monitor the progress by offering a table with all Pokémon present in the dex and a counter in the top right of the GUI. Clicking on a Pokémon icon will switch its color between three possibilities:
1. **White**: Pokémon not caught yet
2. **Red**: Pokémon caught and present in the living dex
3. **Blue**: Pokémon soon-to-be obtained (i.e. by evolution, trade, etc.)
![image](/img/Dex.png)

### 2. All Instruments
 ![image](/img/Main_bar_2.png)
 The second achievement to get to complete the challenge is to obtain **every single item** in the game. This comes according to the following rules:
 1. Every item in each route **must** be picked up, invisible items included
 2. Items which cannot be found in routes *must be bought*
 3. It is possible to buy an item only after it has been found at least once, if possible. For items of point 2 this rule does not apply
 4. Items can be discarded/sold only when the there is **no more space** available
 5. **TM cannot be used**, unless they contains a move that no Pokémon can learn by level-up

The tool allows to track the progress easily thanks to its item cout. This feature is paired with the Route Tracker, which shows the progress per each route, including items present in it. For items which can only be purchased, a **+** and **-** buttons are present to manually add or remove items from the counter. Additionally, by clicking the potion icon it is possible to display a pop-up window showing all items which have never been obtained.

<img src="img/Missing.png" width="300"/>

The total number of items displayed is computed as *the sum of all pick-up items plus one for each purchasable-only* items

### 3. All Trainers
 ![image](/img/Main_bar_3.png)
The third goal for the challenge is to **battle every trainer** in the game. This also includes optional fights. The tool allows, through the Route Tracker, to see all trainers in each floor of a route alongside their team, to easily mark the ones already defeated from missing. Checking a trainer will automatically increase the counter, while unchecking it will lower the counter. Trainers with multiple possible teams (e.g. rivals) are counted as a single instance, although all their possible teams are shown.

### 4. All Moves
 ![image](/img/Main_bar_4.png)
The third requirement is to **see at least once all the moves** in the game, Struggle included. The Tool offers a practical window on the right with a checklist for all the moves, which will automatically increase the counter.

<img src="img/Move_list.png" width="150"/>

To mark a move as "*seen*" one of the following requirement must be met:
1. The move is performed by a member of the player's party
2. An enemy Pokémon perform the move
3. The move is called by Metronome

In all previous cases, it is **required the move to hit** and the animation to play. For multi-hit moves, only one hit is sufficient. However to achieve such goal **TMs are strictly forbidden**, as moves must be seen only from Pokémon which learn them by level-up. The only exception for this rule is for moves which no Pokémon can learn without TM.

### 5. All Other Stuff
 ![image](/img/Main_bar_5.png)
The last category groups up all remaining miscellaneous elements which must be performed. This groups count **interactions** such as trades with NPCs, obtaining certain achievements or battling certain Pokémons. All this requirements can be found in the Route Tracker window, where they are found under the `Event` label

## The Route Tracker Window
The Route Tracker Window is a secondary element which opens together with tha main GUI. This window displays, for a selected route, all items, trainers and available events grouped by location inside the map. All elements are shown alongside a checkbox to mark them as completed/obtained and to increase the corresponding counter.
 ![image](/img/route_explorer.png)
On the top of the windows there is a combobox, to easily change the route currently displayed. Routes are presented in alphabetic order and once a new one is selected, the Route Tracker closes to immediately reopen with data for the new route.
 ![image](/img/Route_selector.png)

## Saving and deleting data
The tool automatically saves the data once one of the two main windows is closed. To delete all the data it is possible to:
1. Unmark everything
2. Delete the file present ``Data/data.json`` that keeps track of the progress