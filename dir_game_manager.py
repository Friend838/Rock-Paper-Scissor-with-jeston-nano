import random
import time
import mediapipe_detector as md


class dir_game_manager:
    def __init__(self):
        self.detector = md.mediapipe_detector()
        self.draw_round_count = 0

    def frame_detect(self, container):
        while 1:
            if container.game_end == True:
                break

            while not container.dir_phase:
                time.sleep(0.5)

            x = container.frame
            x, _, dir_result = self.detector.detect(x)
            if dir_result == 'up':
                container.player_dir_result = 0
                print("up")
            elif dir_result == 'left':
                container.player_dir_result = 1
                print("left")
            elif dir_result == 'down':
                container.player_dir_result = 2
                print("down")
            elif dir_result == 'right':
                container.player_dir_result = 3
                print("right")
            else:
                container.player_dir_result = -1
                print("please show index finger")

    # change opponent's image to question mark, container mean "mainWindow"
    def opponent_default(self, container):
        container.opponent_result_label.config(image=container.question_markTk)
        container.opponent_result_label.image = container.question_markTk

    # pass what opponent's play, and change to related image, container mean "mainWindow"
    def opponent_play(self, container, opponent_result):
        if opponent_result == 0:
            container.opponent_result_label.config(image=container.upTk)
            container.opponent_result_label.image = container.upTk
        elif opponent_result == 1:
            container.opponent_result_label.config(image=container.leftTk)
            container.opponent_result_label.image = container.leftTk
        elif opponent_result == 2:
            container.opponent_result_label.config(image=container.downTk)
            container.opponent_result_label.image = container.downTk
        elif opponent_result == 3:
            container.opponent_result_label.config(image=container.rightTk)
            container.opponent_result_label.image = container.rightTk

    def dir_game_loop(self, container):
        while 1:
            while not container.dir_phase:
                time.sleep(0.5)

            self.opponent_default(container)

            container.info2_label.config(text='男生')
            time.sleep(0.5)
            container.info2_label.config(text='女生')
            time.sleep(0.5)
            container.info2_label.config(text='配!!')

            # opponent use random to play
            rint = random.randint(0, 3)
            self.opponent_play(container, rint)

            # Wait a little and detect hand gesture
            time.sleep(0.5)
            sint = container.player_dir_result

            dir_round_status = -1
            # win(1), lose(0) or replay(-1)
            if sint == -1:
                dir_round_status = 0
                container.info2_label.config(text='no index finger')
                time.sleep(0.5)
                container.info2_label.config(text='You lose')
                container.opponent_score += 1
                container.opponent_score_label.config(
                    text=container.opponent_score)
            elif rint == sint:
                if container.RPS_round_status == 0:
                    dir_round_status = 0
                    container.info2_label.config(text='You lose')
                    container.opponent_score += 1
                    container.opponent_score_label.config(
                        text=container.opponent_score)
                elif container.RPS_round_status == 1:
                    dir_round_status = 1
                    container.info2_label.config(text='You win!!')
                    container.player_score += 1
                    container.player_score_label.config(
                        text=container.player_score)
            else:
                dir_round_status = -1
                self.draw_round_count = self.draw_round_count + 1
                if self.draw_round_count == 3:
                    container.info2_label.config(text='ESCAPE!')
                else:
                    container.info2_label.config(text='Show Again')
                    # 測試男生女生配一直接續
                    continue

            time.sleep(3)
            container.info2_label.config(text='')

            if dir_round_status == -1:
                if self.draw_round_count == 3:
                    # because we add one when RPS phase end, we need to substract one back when ESCAPE happen
                    container.round_passed = container.round_passed - 1
                    self.draw_round_count = 0
                    container.RPS_phase = True
                    container.dir_phase = False
                else:
                    container.RPS_phase = False
                    container.dir_phase = True
            elif dir_round_status == 0 or dir_round_status == 1:
                self.draw_round_count = 0
                container.RPS_phase = True
                container.dir_phase = False
