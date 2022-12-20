#!/usr/bin/env python3
#
# Copyright 2019 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: Joep Tool

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from pysdf import SDF
import numpy as np
import random

class SelectRandomPose:

    def __init__(self, 
            sdl_path, 
            min_x,
            min_y,
            max_x,
            max_y):    

        self.parsed_sdl =  SDF.from_file(sdl_path, remove_blank_text=True)
        self.parsed_sdl.to_file(sdl_path, pretty_print=True)
        self.objects_to_ignore = ["head", "left_hand", "right_hand", "left_foot", "right_foot", "body"]
        self.cylinder_radius = 0.2
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def __cylinder_detect(self):
        self.cylinder_poses = []
        for visual in self.parsed_sdl.iter("visual"):
            if visual.name not in self.objects_to_ignore:
                pose = np.fromstring(visual.pose.text, count=6, sep=" ")
                self.cylinder_poses.append(pose)

    def get_random_pose(self):
        self.__cylinder_detect()
        while True:
            x = random.uniform(self.min_x, self.max_x)
            y = random.uniform(self.min_y, self.max_y)
            self.pose = np.array([x, y])
            self.valid_pose_x_list = []
            self.valid_pose_y_list = []

            for cylinder_pose in self.cylinder_poses:
                valid_pose_x = not cylinder_pose[0] - self.cylinder_radius < self.pose[0] < cylinder_pose[0] + self.cylinder_radius 
                valid_pose_y = not cylinder_pose[1] - self.cylinder_radius < self.pose[1] < cylinder_pose[1] + self.cylinder_radius             
                self.valid_pose_x_list.append(valid_pose_x)
                self.valid_pose_y_list.append(valid_pose_y)

            if False not in self.valid_pose_x_list and False not in self.valid_pose_y_list: 
                return self.pose


def generate_launch_description():
    launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    world = random.randint(1, 4)

    path_sdf_model = f"~/../../opt/ros/humble/share/turtlebot3_gazebo/models/g2w{world}/model.sdf"
    path_sdf_model = os.path.expanduser(path_sdf_model)
    selectRandomPose = SelectRandomPose(sdl_path = path_sdf_model, 
                                min_x = -1.3,
                                min_y = -1.5,
                                max_x =  2.0,
                                max_y =  1.5)
                                
    pose = selectRandomPose.get_random_pose()     

    

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose = LaunchConfiguration('x_pose', default=f'{pose[0]}')
    y_pose = LaunchConfiguration('y_pose', default=f'{pose[1]}')
   

    if world == 1:    
        world = os.path.join(
            get_package_share_directory('turtlebot3_gazebo'),
            'worlds',
            'g2w1.world'
        )    
    elif world == 2:    
        world = os.path.join(
            get_package_share_directory('turtlebot3_gazebo'),
            'worlds',
            'g2w2.world'
        )     
    elif world == 3:    
        world = os.path.join(
            get_package_share_directory('turtlebot3_gazebo'),
            'worlds',
            'g2w3.world'
        )        
    elif world == 4:    
        world = os.path.join(
            get_package_share_directory('turtlebot3_gazebo'),
            'worlds',
            'g2w4.world'
        )               

    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world}.items()
    )

    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    spawn_turtlebot_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'spawn_turtlebot3.launch.py')
        ),
        launch_arguments={
            'x_pose': f'{pose[0]}',
            'y_pose': f'{pose[1]}',
        }.items()
    )

    ld = LaunchDescription()

    # Add the commands to the launch description
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(spawn_turtlebot_cmd)

    return ld
