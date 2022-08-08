import cv2
import pygame
import tkinter as tk
import tkinter.messagebox as tkmb
from PIL import Image, ImageTk


def define_layout(obj, cols=1, rows=1):
    def method(trg, col, row):
        for c in range(cols):
            trg.columnconfigure(c, weight=1)
        for r in range(rows):
            trg.rowconfigure(r, weight=1)

    if type(obj) == list:
        [method(trg, cols, rows) for trg in obj]
    else:
        trg = obj
        method(trg, cols, rows)


class mainWindow:
    def __init__(self, align_mode):
        # all variables game might use
        self.frame = []                 # store what camera capture
        self.opponent_score = 0
        self.player_score = 0
        self.player_RPS_result = 0      # player's RPS detection result
        self.player_dir_result = 0
        self.game_end = False           # a bool to decide whether game needs to end
        # the number of games which are really counted in when win or lose, and it doesn't count if draw or escape
        self.round_passed = 0
        self.round_limited = 0
        self.round_setted = False
        self.RPS_phase = True
        self.dir_phase = False
        # need to be passed to dir_game_manager, -1: initial, 0: RPS lose status, 1: RPS win status
        self.RPS_round_status = -1

        # create main window and title
        self.__window = tk.Tk()
        self.__window.title('Rock Paper Scissors Game')

        # press q to close the game
        self.__window.bind('<q>', lambda q: self.close_game(q))

        # initialize camera -> you can change input port
        print("loading camera......")
        self.__cap = cv2.VideoCapture(0)
        self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        print("camera set up finish")

        # initialize mediapipe
        # self.detector = md.mediapipe_detector()

        # camera read one time for recognition initializing
        ret, self.frame = self.__cap.read()

        # all used images preprocess to tkinter compatible
        self.rockTk = ImageTk.PhotoImage(
            Image.open('./images/rock.png').resize((300, 300)))
        self.paperTk = ImageTk.PhotoImage(
            Image.open('./images/paper.png').resize((300, 300)))
        self.scissorTk = ImageTk.PhotoImage(
            Image.open('./images/scissor.png').resize((300, 300)))
        self.question_markTk = ImageTk.PhotoImage(
            Image.open('./images/question_mark.png').resize((300, 300)))
        self.upTk = ImageTk.PhotoImage(Image.open(
            './images/up.png').resize((300, 300)))
        self.leftTk = ImageTk.PhotoImage(Image.open(
            './images/left.png').resize((300, 300)))
        self.downTk = ImageTk.PhotoImage(Image.open(
            './images/down.png').resize((300, 300)))
        self.rightTk = ImageTk.PhotoImage(Image.open(
            './images/right.png').resize((300, 300)))

        # divide and place frames
        self.__title_frame = tk.Frame(self.__window, width=500, height=100)
        self.__opponent_score_frame = tk.Frame(
            self.__window, width=100, height=100)
        self.__info1_frame = tk.Frame(self.__window, width=100, height=50)
        self.__player_score_frame = tk.Frame(
            self.__window, width=100, height=100)
        self.__opponent_frame = tk.Frame(self.__window, width=400, height=300)
        self.__info2_frame = tk.Frame(self.__window, width=400, height=50)
        self.__video_frame = tk.Frame(self.__window, width=400, height=300)

        self.__title_frame.grid(
            column=0, row=0, columnspan=2, sticky=align_mode)
        self.__opponent_score_frame.grid(column=0, row=1, sticky=align_mode)
        self.__info1_frame.grid(column=0, row=2, sticky=align_mode)
        self.__player_score_frame.grid(column=0, row=3, sticky=align_mode)
        self.__opponent_frame.grid(column=1, row=1, sticky=align_mode)
        self.__info2_frame.grid(column=1, row=2, sticky=align_mode)
        self.__video_frame.grid(column=1, row=3, sticky=align_mode)

        define_layout(self.__window, cols=2, rows=4)
        define_layout([self.__title_frame, self.__opponent_score_frame, self.__info1_frame,
                       self.__player_score_frame, self.__opponent_frame, self.__info2_frame, self.__video_frame])

        # for each frame, implement its component
        self.title_label = tk.Label(self.__title_frame, text='Rock Paper Scissors Game', font=(
            "Arial", 35), bg='blue', fg='white')
        self.opponent_score_label = tk.Label(
            self.__opponent_score_frame, text=self.opponent_score, font=('Arial', 25), bg='green', fg='white')
        self.info1_label = tk.Label(self.__info1_frame, text='VS', font=(
            "Arial", 20), bg='gray', fg='yellow')
        self.player_score_label = tk.Label(
            self.__player_score_frame, text=self.player_score, font=('Arial', 25), bg='green', fg='white')
        self.opponent_result_label = tk.Label(
            self.__opponent_frame, image=self.question_markTk)
        self.info2_label = tk.Label(
            self.__info2_frame, text='loading', font=('Arial', 20))
        self.three_rounds_button = tk.Button(self.__info2_frame, text='3 Rounds', font=(
            'Arial', 20), command=self.set_3_rounds)
        self.five_rounds_button = tk.Button(self.__info2_frame, text='5 Rounds', font=(
            'Arial', 20), command=self.set_5_rounds)
        self.video_label = tk.Label(self.__video_frame)

        self.title_label.grid(sticky=align_mode)
        self.opponent_score_label.grid(sticky=align_mode)
        self.info1_label.grid(sticky=align_mode)
        self.player_score_label.grid(sticky=align_mode)
        self.opponent_result_label.image = self.question_markTk
        self.opponent_result_label.grid(sticky=align_mode)
        # self.info2_label.grid(sticky=align_mode)
        self.three_rounds_button.grid(row=0, column=0, sticky=align_mode)
        self.five_rounds_button.grid(row=0, column=1, sticky=align_mode)
        self.video_label.grid(sticky=align_mode)

        define_layout(self.__window, cols=2, rows=4)
        define_layout(self.__info2_frame, cols=2)

        # background music set up
        pygame.mixer.init()
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.play(loops=5)

    def set_3_rounds(self):
        self.round_setted = True
        self.round_limited = 3
        self.three_rounds_button.destroy()
        self.five_rounds_button.destroy()
        self.info2_label.grid(row=0, column=0, columnspan=2, sticky='nswe')

    def set_5_rounds(self):
        self.round_setted = True
        self.round_limited = 5
        self.three_rounds_button.destroy()
        self.five_rounds_button.destroy()
        self.info2_label.grid(row=0, column=0, columnspan=2, sticky='nswe')

    # start windo main loop
    def start_main_loop(self):
        self.__window.mainloop()

    def close_game(self, q):
        tkmb.showinfo("Score Statistics", "Player Score: {}\nOpponent Score: {}".format(
            self.player_score, self.opponent_score))
        self.game_end = True
        self.__window.destroy()
        self.__cap.release()

    # keep looping to create video stream if game haven't ended
    def video_streaming(self):
        if not self.game_end:
            # Get the latest frame and convert into Image
            ret, temp_image = self.__cap.read()
            self.frame = temp_image
            cv2image = cv2.cvtColor(temp_image, cv2.COLOR_BGR2RGB)
            cv2image = cv2.flip(cv2image, 1)
            img = Image.fromarray(cv2image)
            # Convert image to PhotoImage
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            # Repeat after an interval to capture continiously
            self.video_label.after(10, self.video_streaming)
