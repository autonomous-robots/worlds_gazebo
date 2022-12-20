# worlds_gazebo

This repository contains the files of the worlds created for the presentation of the work. The obstacles were positioned in different configurations so that the solution proposed by the group could have been tested and validated. When launching [turtlebot3_world.launch.py](https://github.com/autonomous-robots/worlds_gazebo/blob/main/launch/turtlebot3_world.launch.py), one of the worlds will be randomly chosen as well as the position of the robot. The python-sdformat library is used to read the sdl file. Thus, the position of the cylinders is collected and a check is made to ensure that the robot never starts in a place already occupied by an obstacle.

## steps to run the project

#### 1º

```
git clone https://github.com/autonomous-robots/worlds_gazebo.git

```

#### 2º

```
cd worlds_gazebo

```

#### 3º

```
cp worlds/autonomous_robots_world_1.world ~/../../opt/ros/humble/share/turtlebot3_gazebo/worlds/

```

#### 4º

```
cp worlds/autonomous_robots_world_2.world ~/../../opt/ros/humble/share/turtlebot3_gazebo/worlds/

```

#### 5º

```
cp -r models/autonomous_robots_world_1 ~/../../opt/ros/humble/share/turtlebot3_gazebo/models/

```

#### 6º

```
cp -r models/autonomous_robots_world_2 ~/../../opt/ros/humble/share/turtlebot3_gazebo/models/
```

#### 7º

```
cp launch/turtlebot3_world.launch.py ~/../../opt/ros/humble/share/turtlebot3_gazebo/launch/
```

#### 8º

```
pip install -r requirements.sdf
```
