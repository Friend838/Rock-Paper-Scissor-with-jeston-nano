import sys
from threading import Thread

import mainWindow
import RPS_game_manager
import dir_game_manager

align_mode = 'nswe'


window = mainWindow.mainWindow(align_mode)
manager1 = RPS_game_manager.RPS_game_manager()
manager2 = dir_game_manager.dir_game_manager()

window.video_streaming()

detect_RPS_thread = Thread(target=manager1.frame_detect, args=(window, ))
detect_RPS_thread.daemon = True
detect_RPS_thread.start()

detect_dir_thread = Thread(target=manager2.frame_detect, args=(window, ))
detect_dir_thread.daemon = True
detect_dir_thread.start()

RPS_thread = Thread(target=manager1.RPS_game_loop, args=(window, ))
RPS_thread.daemon = True
RPS_thread.start()

dir_thread = Thread(target=manager2.dir_game_loop, args=(window, ))
dir_thread.daemon = True
dir_thread.start()

window.start_main_loop()

sys.exit(0)
