#!/usr/bin/env python

import robot_upstart
j = robot_upstart.Job(name="run_game",workspace_setup="source /home/diyazen/hashika_ws/install/setup.bash")
j.symlink = True
j.add(package="game", filename="launch/run.launch" )
j.install()