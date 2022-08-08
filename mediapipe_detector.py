import cv2
import mediapipe as mp
import math


class mediapipe_detector:
    def __init__(self):
        print("loading mediapipe......")
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75)
        print("mediapipe set up finish")

    def __vector_2d_angle(self, v1, v2):
        '''
        求解二维向量的角度
        '''
        v1_x = v1[0]
        v1_y = v1[1]
        v2_x = v2[0]
        v2_y = v2[1]
        try:
            angle_ = math.degrees(math.acos(
                (v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
        except:
            angle_ = 65535.
        if angle_ > 180.:
            angle_ = 65535.
        return angle_

    def hand_angle(self, hand_):
        '''
            获取对应手相关向量的二维角度,根据角度确定手势
        '''
        angle_list = []
        # ---------------------------- thumb 大拇指角度
        angle_ = self.__vector_2d_angle(
            ((int(hand_[0][0]) - int(hand_[2][0])),
             (int(hand_[0][1])-int(hand_[2][1]))),
            ((int(hand_[3][0]) - int(hand_[4][0])),
             (int(hand_[3][1]) - int(hand_[4][1])))
        )
        angle_list.append(angle_)
        # ---------------------------- index 食指角度
        angle_ = self.__vector_2d_angle(
            ((int(hand_[0][0])-int(hand_[6][0])),
             (int(hand_[0][1]) - int(hand_[6][1]))),
            ((int(hand_[7][0]) - int(hand_[8][0])),
             (int(hand_[7][1]) - int(hand_[8][1])))
        )
        angle_list.append(angle_)
        # ---------------------------- middle 中指角度
        angle_ = self.__vector_2d_angle(
            ((int(hand_[0][0]) - int(hand_[10][0])),
             (int(hand_[0][1]) - int(hand_[10][1]))),
            ((int(hand_[11][0]) - int(hand_[12][0])),
             (int(hand_[11][1]) - int(hand_[12][1])))
        )
        angle_list.append(angle_)
        # ---------------------------- ring 无名指角度
        angle_ = self.__vector_2d_angle(
            ((int(hand_[0][0]) - int(hand_[14][0])),
             (int(hand_[0][1]) - int(hand_[14][1]))),
            ((int(hand_[15][0]) - int(hand_[16][0])),
             (int(hand_[15][1]) - int(hand_[16][1])))
        )
        angle_list.append(angle_)
        # ---------------------------- pink 小拇指角度
        angle_ = self.__vector_2d_angle(
            ((int(hand_[0][0]) - int(hand_[18][0])),
             (int(hand_[0][1]) - int(hand_[18][1]))),
            ((int(hand_[19][0]) - int(hand_[20][0])),
             (int(hand_[19][1]) - int(hand_[20][1])))
        )
        angle_list.append(angle_)
        return angle_list

    def calc_slopee(self, p1, p2):
        if p1[0] == p2[0] and p2[1] < p1[1]:
            return "negative infinity"
        elif p1[0] == p2[0] and p2[1] > p1[1]:
            return "positive infinity"
        else:
            return (p2[1] - p1[1]) / (p2[0] - p1[0])

    def h_gesture(self, angle_list):
        '''
        二维约束的方法定义手势
        fist five gun love one six three thumbup yeah
        '''
        thr_angle = 65.  # 手指闭合则大于这个值（大拇指除外）
        thr_angle_thumb = 53.  # 大拇指闭合则大于这个值
        thr_angle_s = 49.  # 手指张开则小于这个值
        gesture_str = "unknown"

        if 65535. not in angle_list:
            if (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
                # rock
                gesture_str = "0"
            elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
                # scissor
                gesture_str = "2"
            elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s):
                # paper
                gesture_str = "5"
            '''
            elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
                gesture_str = "Pink Up"
            elif (angle_list[0] < thr_angle_s) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
                gesture_str = "Thumb Up"
            elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] < thr_angle_s) and (angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
                gesture_str = "Fuck"
            elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] < thr_angle_s) and (angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s):
                gesture_str = "Princess"
            elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
                gesture_str = "Bye"
            elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
                gesture_str = "Spider-Man"
            elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
                gesture_str = "Rock'n'Roll"
            '''

        return gesture_str

    def index_finger_direction(self, point_list):
        direction = 'please show index finger'

        index_angle = self.__vector_2d_angle(
            ((int(point_list[0][0])-int(point_list[6][0])),
             (int(point_list[0][1]) - int(point_list[6][1]))),
            ((int(point_list[7][0]) - int(point_list[8][0])),
             (int(point_list[7][1]) - int(point_list[8][1])))
        )

        if index_angle != 65535. and index_angle < 49.:
            slopee = self.calc_slopee(point_list[5], point_list[8])

            if slopee == "negative infinity":
                direction = 'up'
            elif slopee == "positive infinity":
                direction = 'down'
            elif -1 < slopee < 1:
                if point_list[8][0] - point_list[5][0] > 0:
                    direction = 'right'
                else:
                    direction = 'left'
            elif slopee < -1:
                if point_list[8][0] - point_list[5][0] > 0:
                    direction = 'up'
                else:
                    direction = 'down'
            elif slopee > 1:
                if point_list[8][0] - point_list[5][0] > 0:
                    direction = 'down'
                else:
                    direction = 'up'

        return direction

    def detect(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        results = self.hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        '''
        # detect left hand or right hand
        if results.multi_handedness:
            print('Handedness:', results.multi_handedness)
            for hand_label in results.multi_handedness:
                hand_jugg = str(hand_label).split('"')[1]
                print(hand_jugg)
                cv2.putText(frame, hand_jugg, (50, 200),
                            0, 1.3, (0, 0, 255), 2)
        '''
        gesture_str = 'no hand'
        index_finger_dir = 'please show index finger'
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # self.mp_drawing.draw_landmarks(
                #    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                hand_local = []
                for i in range(21):
                    x = hand_landmarks.landmark[i].x*frame.shape[1]
                    y = hand_landmarks.landmark[i].y*frame.shape[0]
                    hand_local.append((x, y))

                if hand_local:
                    angle_list = self.hand_angle(hand_local)
                    gesture_str = self.h_gesture(angle_list)
                    index_finger_dir = self.index_finger_direction(hand_local)

        return frame, gesture_str, index_finger_dir
