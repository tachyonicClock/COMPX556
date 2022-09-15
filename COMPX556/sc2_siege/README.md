## Setting Up SC2

https://github.com/BurnySc2/python-sc2

> Enabling renders requires the full version of SC2 to be installed
> through Battle.net (using WINE on linux). python-sc2 will enable the renderer if it is
> run with the appropriate environment variables.
> 
> ```
> SC2PF=WineLinux WINE=/usr/bin/wine SC2PATH=/home/anton/.wine/drive_c/Program\ Files\ \(x86\)/StarCraft\ II/  python3 examples/protoss/cannon_rush.py 
> ```

# Scenario

The task is to evolve a 16x16 defensive position. Buildings will conform to the
grid but units wont.

![](img/scenario.png)
![](img/minimap.png)


The Agent is allowed an arbitrary amount of time to setup the defenses. When the Agent messages `Ready!` in chat a sequence of waves starts. The waves will attempt to reach the *command center* through the choke point in the middle of the map. Each wave is progressively more difficult.

![](img/waves.png)

## Evaluation

The 16x16 defensive position is evaluated by the amount of time the *command center*
survives and the resources it takes todo so.

SC2 has two types of resources: Minerals and Gas. Gas is considered more valuable.
We will have to weight them correctly.

### Human Solution
The scenario is solvable by a human. I found the following solution.

 - 3,500 Minerals
 - 1,300 Gas

![](img/human_solution.png)
