import random
import time
import cv2
import torch
import mediapipe_detector as md

TIME_DELTA = 0.5


class RPS_game_manager:
    def __init__(self):
        self.detector = md.mediapipe_detector()

    def frame_detect(self, container):
        while 1:
            if container.game_end == True:
                break

            while not container.RPS_phase:
                time.sleep(0.5)

            x = container.frame
            x, detect_result, _ = self.detector.detect(x)

            if detect_result == '0':
                container.player_RPS_result = 0
                print("rock")
            elif detect_result == '5':
                container.player_RPS_result = 1
                print("paper")
            elif detect_result == '2':
                container.player_RPS_result = 2
                print("scissor")
            elif detect_result == 'unknown':
                container.player_RPS_result = -1
                print("unknwon")
            elif detect_result == 'no hand':
                container.player_RPS_result = -2
                print("no hand")

    # the number corresponds to its related type
    def name_of_value(self, val):
        if val == 0:
            return "Rock    "
        if val == 1:
            return "Paper   "
        if val == 2:
            return "Scissor "

    # pass what opponent's play, and change to related image, container mean "mainWindow"
    def opponent_play(self, container, opponent_result):
        if opponent_result == 0:
            container.opponent_result_label.config(image=container.rockTk)
            container.opponent_result_label.image = container.rockTk
        elif opponent_result == 1:
            container.opponent_result_label.config(image=container.paperTk)
            container.opponent_result_label.image = container.paperTk
        elif opponent_result == 2:
            container.opponent_result_label.config(image=container.scissorTk)
            container.opponent_result_label.image = container.scissorTk

    # change opponent's image to question mark, container mean "mainWindow"
    def opponent_default(self, container):
        container.opponent_result_label.config(image=container.question_markTk)
        container.opponent_result_label.image = container.question_markTk

    # main RPS loop, container mean "mainWindow"
    def RPS_game_loop(self, container):
        global TIME_DELTA
        while not container.round_setted:
            time.sleep(1)

        while 1:
            while not container.RPS_phase:
                time.sleep(0.5)

            if container.round_passed == container.round_limited:
                container.close_game('q')
                break

            container.info2_label.config(text='Are you ready?')
            time.sleep(2.0)
            self.opponent_default(container)
            #GPIO.wait_for_edge(BUTTON_PIN, GPIO.RISING)

            # reset light and rotation
            container.info2_label.config(text='黑')
            time.sleep(TIME_DELTA)

            container.info2_label.config(text='白')
            time.sleep(TIME_DELTA)

            container.info2_label.config(text='猜!!')

            # opponent use random to play
            rint = random.randint(0, 2)
            self.opponent_play(container, rint)

            # Wait a little and detect hand gesture
            time.sleep(0.5)
            sint = container.player_RPS_result

            # win or lose
            diff = 0
            diff = (rint - sint) % 3
            if sint == -2:
                container.round_passed += 1
                container.info2_label.config(text='no hand detected')
                container.opponent_score += 1
                container.opponent_score_label.config(
                    text=container.opponent_score)
            elif sint == -1:
                container.round_passed += 1
                container.info2_label.config(text='unknown gesture')
                container.opponent_score += 1
                container.opponent_score_label.config(
                    text=container.opponent_score)
            elif diff == 0:
                container.info2_label.config(text='Draw')
                # tie_game();
            elif diff == 1:
                container.round_passed += 1
                container.info2_label.config(text='由你防守!')
                container.RPS_round_status = 0
                # won_game();
            elif diff == 2:
                container.round_passed += 1
                container.info2_label.config(text='由你進攻!')
                container.RPS_round_status = 1
                # lost_game();

            time.sleep(0.8)
            container.info2_label.config(text='')

            if sint == -1 or sint == -2:
                container.RPS_phase = True
                container.dir_phase = False
            elif diff == 0:
                container.RPS_phase = True
                container.dir_phase = False
            elif diff == 1 or diff == 2:
                container.RPS_phase = False
                container.dir_phase = True
