import tkinter as tk
import tkinter.font as font
import tkinter.simpledialog as simpledialog

import random as rd
from datetime import datetime as dt

# 타이머, P442


class Timer():
    def __init__(self):
        self.reset()

    def start(self):
        # 최초 타이머 시작
        if self.__stop == False:
            self.__elapsed = None
            self.__current = None
            self.__start = dt.now()
        # 스탑 후 다시 시작하면 초기화 하지 않고 그냥 시작
        else:
            self.__stop = False

    def reset(self):
        self.__elapsed = None
        self.__start = None
        self.__current = None
        self.__minute = 0
        self.__stop = False

    def stop(self):
        self.__stop = True

    def getElapsed(self):
        time_6 = 0  # 분 10의자리
        time_5 = 0  # 분 1의자리
        time_4 = 0  # 초 10의 자리
        time_3 = 0  # 초 1의자리
        time_2 = 0  # 1/10초
        time_1 = 0  # 1/10초
        if not self.__stop:
            self.__current = dt.now()
            self.__elapsed = self.__current - self.__start
            delta = int(100*self.__elapsed.total_seconds())  # 0.01초 단위 정수
            time_1 = delta % 10
            time_2 = int((delta / 10) % 10)
            time_3 = int((delta / 100) % 10)
            time_4 = int((delta / 1000) % 10)
            if time_4 == 6 and time_3 == 0:
                self.__minute += 1
                self.__elapsed = None
                self.__current = None
                self.__start = dt.now()
            time_5 = int(self.__minute % 10)
            time_6 = int(self.__minute / 10) % 10
        return f"{time_6}{time_5} : {time_4}{time_3} : {time_2}{time_1}"

# 게임 종료 대화상자


class End(tk.Toplevel):
    def __init__(self, mineNum, arg, gamestate, timer):
        super().__init__()

        # Minesweeper로 부터 타이머 넘겨받음
        self.__timer = timer

        # 게임 화면 설정
        self.title("게임 종료")
        self.geometry("500x400")

        # 시간, 지뢰 수 표시 라벨
        self.__font1 = font.Font(family="Helvatica", size=30, weight="bold")
        self.__lb1 = tk.Label(self, text=gamestate, font=self.__font1)
        self.__lb1.place(relx=0, relwidth=1, rely=0*0.2, relheight=0.2)
        self.__lb2 = tk.Label(self, text="시간 : " +
                              self.__timer.getElapsed(), font=self.__font1)
        self.__timer.stop()
        self.__lb2.place(relx=0, relwidth=1, rely=1*0.2, relheight=0.2)
        self.__lb3 = tk.Label(self, text="MINE : " +
                              str(mineNum), font=self.__font1)
        self.__lb3.place(relx=0, relwidth=1, rely=2*0.2, relheight=0.2)

        # 재시작, 나가기 버튼
        self.__b1 = tk.Button(self, text="재시작", font=self.__font1)
        self.__b2 = tk.Button(self, text="나가기", font=self.__font1)
        self.__b1.bind("<Button-1>", self.quit1)
        self.__b2.bind("<Button-1>", self.quit2)
        self.__b1.place(relx=0, relwidth=1, rely=3*0.2, relheight=0.2)
        self.__b2.place(relx=0, relwidth=1, rely=4*0.2, relheight=0.2)

        # 버튼 선택 값을 담을 변수
        self.__arg = arg

        # 창 닫기 버튼 클릭시 동작
        self.protocol("WM_DELETE_WINDOW", self.quit0)
        self.mainloop()

    # 창 닫기 버튼 callback
    def quit0(self):
        self.__timer.reset()
        self.__arg[0] = 2
        self.quit()
        self.destroy()

    # 재시작 버튼 callback
    def quit1(self, event):
        self.__arg[0] = 1
        self.quit()
        self.destroy()

    # 나가기 버튼 callbark
    def quit2(self, event):
        self.quit0()

# 게임 일시정지 대화상자


class Puase(tk.Toplevel):
    def __init__(self, timer, mineNum, arg):
        super().__init__()
        self.__timer = timer    # Minesweeper 객체로부터 타이머 객채 넘겨받음

        # 창 설정
        self.title("일시정지")
        self.geometry("500x400")
        self.__font1 = font.Font(family="Helvatica", size=30, weight="bold")

        # 멈춘 시간, 지뢰 수 표시
        self.__lb1 = tk.Label(self, text="시간 : " +
                              self.__timer.getElapsed(), font=self.__font1)
        self.__lb1.place(relx=0, relwidth=1, rely=0*0.2, relheight=0.2)
        self.__timer.stop()
        self.__lb2 = tk.Label(self, text="MINE : " +
                              str(mineNum), font=self.__font1)
        self.__lb2.place(relx=0, relwidth=1, rely=1*0.2, relheight=0.2)

        # 재시작, 나가기, 계속하기 버튼 생성
        self.__b1 = tk.Button(self, text="재시작", font=self.__font1)
        self.__b2 = tk.Button(self, text="나가기", font=self.__font1)
        self.__b3 = tk.Button(self, text="계속하기", font=self.__font1)
        self.__b1.bind("<Button-1>", self.quit1)
        self.__b2.bind("<Button-1>", self.quit2)
        self.__b3.bind("<Button-1>", self.quit3)
        self.__b1.place(relx=0, relwidth=1, rely=2*0.2, relheight=0.2)
        self.__b2.place(relx=0, relwidth=1, rely=3*0.2, relheight=0.2)
        self.__b3.place(relx=0, relwidth=1, rely=4*0.2, relheight=0.2)

        # 버튼 선택 값을 담을 변수
        self.__arg = arg

        # 창의 X버튼 클릭시 동작
        self.protocol("WM_DELETE_WINDOW", self.quit0)
        self.mainloop()

    # 창 닫기 버튼 callback
    def quit0(self):
        self.__timer.start()
        self.quit()
        self.destroy()

    # 재시작 버튼 callback
    def quit1(self, event):
        self.__arg[0] = 1
        self.quit()
        self.destroy()

    # 나가기 버튼 callback
    def quit2(self, event):
        self.__arg[0] = 2
        self.__timer.reset()
        self.quit()
        self.destroy()

    # 계속하기 버튼 callback
    def quit3(self, event):
        self.__timer.start()
        self.quit()
        self.destroy()


class Minesweeper(tk.Frame):
    def __init__(self, master, controller):
        self.__controller = controller  # GameController 객체

        super().__init__(master)        # 프레임을 생성하고 container에 담음
        self.initialize(1, 1, 0.1)        # 초기 생성

    # 초기화
    def initialize(self, row, col, level):
        self.__col = col    # 가로 칸 수
        self.__row = row    # 세로 칸 수
        self.__level = level        # 지뢰 비율
        self.__widthRatio = 1/self.__col    # 가로 칸 비율
        self.__heightRatio = 1/(self.__row+1)   # 세로 칸 비율
        self.__mineNum = 0          # 지뢰 수

        self.__Board = []   # 버튼
        self.__mine = [[' ' for x in range(self.__col)] for y in range(
            self.__row)]  # 지뢰 밭을 담을 2차원 리스트

        for i in range(self.__row):
            for j in range(self.__col):
                tmp = tk.Button(self, text="", bg="gray",
                                font=self.__controller.font)
                tmp.place(relx=j*self.__widthRatio, relwidth=self.__widthRatio,
                          rely=(i+1)*self.__heightRatio, relheight=self.__heightRatio)
                tmp.bind("<Button-1>", self.buttonCallback)
                tmp.bind("<Button-3>", self.markPlaceMine)
                self.__Board.append(tmp)

        # 지뢰밭 생성, P288
        for r in range(self.__row):
            for c in range(self.__col):
                # print(f"{r} {c}")
                if rd.random() < self.__level:
                    self.__mine[r][c] = "*"
                    self.__mineNum += 1

        # 지뢰 수 라벨
        self.__font2 = font.Font(family="Helvatica", size=10, weight="bold")
        self.__lbMineNum = tk.Label(
            self, text="MINE : " + str(self.__mineNum), font=self.__font2)
        self.__lbMineNum.place(relx=0, relwidth=1/5,
                               rely=0, relheight=self.__heightRatio)

        # 시간 초 라벨
        self.__lbTimer = tk.Label(
            self, text="00 : 00 : 00", font=self.__font2, anchor="center")
        self.__lbTimer.place(relx=1/5, relwidth=3/5, rely=0,
                             relheight=self.__heightRatio)

        # 일시 정시 버튼
        self.__btPause = tk.Button(
            self, text="일시정지", font=self.__font2, anchor="center")
        self.__btPause.place(relx=4/5, relwidth=1/5, rely=0,
                             relheight=self.__heightRatio)
        self.__btPause.bind("<Button-1>", self.pause)

        self.__tm = Timer()     # 게임에 이용할 타이머
        self.__tm.reset()       # 타이머 초기화
        self.__tm.start()       # 타이머 시작

        self.__numable = 0      # 현재 활성화된 버튼 수
        self.__numcheck = 0     # 지뢰표시의 수
        self.__gamestate = ""   # 게임 상태 변수

    # 버튼 클릭 callback
    def buttonCallback(self, event):
        if self.__gamestate == "":  # 게임이 진행중일 떄 에만 동작
            for k in range(len(self.__Board)):
                # event가 일어난 위젯의 위치 찾기
                if event.widget == self.__Board[k]:
                    row = int(k / self.__col)
                    col = k % self.__col
                    # 지뢰 칸을 클릭 시
                    if self.__mine[row][col] == "*":
                        self.clickMineButton(event.widget)
                        # 게임 패비
                        self.__gamestate = "DEFEATED"
                        self.endofgame()
                        return
                    # 클릭한 칸이 지뢰가 아니면
                    else:
                        result = self.findMineNum(row, col)
                        if result == 0:    # 클릭했는데 주변 1칸에 지뢰가 0개이면
                            self.clickZeroButton(event.widget)
                            self.destroyField(row, col)  # 주변 지뢰가 없는 타일 모두 탐색
                        else:
                            self.clickNonMineButton(
                                event.widget, result)  # 주변 지뢰가 있는 버튼을 클릭 시

    # 클릭한 버튼 주변의 지뢰 숫자 가져오기
    def findMineNum(self, row, col):
        findrow = 0
        endrow = 0
        findcol = 0
        endcol = 0
        minNum = 0
        # row, col의 위치에 따른 탐색 영역 설정
        # 탐색하고자 하는 버튼의 위치가 가장자리 이면 탐색 영역이 달라짐
        if row > 1:
            findrow = row - 1
        if col > 1:
            findcol = col - 1

        if row < self.__row - 1:
            endrow = row + 1
        else:
            endrow = row

        if col < self.__col - 1:
            endcol = col + 1
        else:
            endcol = col

        # 탐색 영역 안에서 지뢰 수 새기
        for r in range(findrow, endrow + 1):
            for c in range(findcol, endcol + 1):
                if self.__mine[r][c] == "*":
                    minNum += 1

        return minNum

    # 주위 지뢰의 숫자가 0일 경우 모두 제거
    def destroyField(self, row, col):
        findrow = 0
        endrow = 0
        findcol = 0
        endcol = 0

        # row, col의 위치에 따른 탐색 영역 설정
        # 탐색하고자 하는 버튼의 위치가 가장자리 이면 탐색 영역이 달라짐
        if row > 1:
            findrow = row - 1
        if col > 1:
            findcol = col - 1

        if row < self.__row - 1:
            endrow = row + 1
        else:
            endrow = row

        if col < self.__col - 1:
            endcol = col + 1
        else:
            endcol = col

        # 시스템 스택 사용
        # 주위 지뢰가 없는 모든 버튼 탐색
        for i in range(findrow, endrow+1):
            for j in range(findcol, endcol+1):
                num = self.findMineNum(i, j)
                if num == 0 and self.__Board[i*self.__col + j]["state"] != "disabled":
                    self.clickZeroButton(self.__Board[i*self.__col + j])
                    self.destroyField(i, j)
                elif num > 0 and self.__Board[i*self.__col + j]["state"] != "disabled":
                    self.clickNonMineButton(
                        self.__Board[i*self.__col + j], num)

    # 지뢰가 있는 곳을 표시하기`
    def markPlaceMine(self, event):
        if event.widget["text"] == "":  # 표시되있지 않은곳이고 disabled되지 않았으면 표시하기
            event.widget["text"] = "M"
            event.widget["bg"] = "green"
            event.widget["fg"] = "black"
            self.__numcheck += 1
        elif event.widget["text"] == "M":   # 표시된 곳이면 표시 해제
            event.widget["text"] = ""
            event.widget["bg"] = "gray"
            event.widget["fg"] = "black"
            self.__numcheck -= 1

    # 지뢰를 눌렀을 때

    def clickMineButton(self, widget):
        widget["text"] = "*"
        widget["bg"] = "red"    # 지뢰를 클릭하면 버튼이 빨간색이 됨
        widget["disabledforeground"] = "black"

    # 0을 눌렀을 떄
    def clickZeroButton(self, widget):
        if self.__gamestate == "":
            widget["text"] = " "
            widget["fg"] = "black"
            widget["bg"] = "white"
            widget["state"] = "disabled"

    # 그 외 버튼을 눌렀을 떄
    def clickNonMineButton(self, widget, num):
        if self.__gamestate == "":
            widget["state"] = "disabled"
            # 버튼 주위의 지뢰 숫자에 따라 버튼에 숫자를 출력하고 색을 달리함
            if num > 3:
                widget["disabledforeground"] = "green"
            elif num > 2:
                widget["disabledforeground"] = "red"
            elif num > 1:
                widget["disabledforeground"] = "blue"
            else:
                widget["disabledforeground"] = "black"
            widget["text"] = str(num)
            widget["bg"] = "white"

    # 일시정지 버튼
    # 게임 중 일시정지 버튼 클릭 시 대화상자 열기
    def pause(self, event):
        if self.__gamestate == "":
            self.__gamestate = "PAUSE"  # PAUSE 상태
            arg = [0]  # reference 변수
            # 일시정지 대화상자
            Puase(self.__tm, self.__mineNum, arg)
            if arg[0] == 1:  # 재시작시 게임의 보드를 다시 만들고 시작
                self.initialize(self.__row, self.__col, self.__level)
            elif arg[0] == 2:  # 게임 나가기 시 시작 화면으로 프레임 전환
                self.__controller.showFrame("StartPage")
            self.__gamestate = ""  # PAUSE 상태 해제

    # 게임 진행 여부
    def gamestate(self):
        numAble = 0
        # 활성화된 버튼의 수 얻기
        for k in range(len(self.__Board)):
            if self.__Board[k]["state"] != "disabled":
                numAble += 1

        self.__numable = numAble
        # 지뢰를 클릭하지 않고, 활성화된 버튼 수와 지뢰 수, 지뢰라고 표시한 수가 일치하면 승리
        if self.__numable == self.__mineNum and self.__numable == self.__numcheck:
            self.__gamestate = "VICTORY"
            self.endofgame()

    # 게임이 끝났을 때, 졌거나 이겼거나
    def endofgame(self):
        arg = [0]   # 게임 종료 대화상자의 값을 가져오기 위한 변수
        # 지뢰 위치를 모두 표시함
        for k in range(len(self.__Board)):
            r = int(k/self.__col)
            c = k % self.__col
            if self.__Board[k]["state"] != "disabled" and self.__mine[r][c] == "*":
                self.clickMineButton(self.__Board[k])
        # 게임 종료 대화상자
        End(self.__mineNum, arg, self.__gamestate, self.__tm)

        if arg[0] == 1:  # 재시작 시 동작
            self.initialize(self.__row, self.__col, self.__level)
        elif arg[0] == 2:   # 나가기 시 동작
            self.__controller.showFrame("StartPage")

    # 게임 프로그램의 루프에서 게임 시간을 계속 업데이트 해주기 위한 함수
    def updateTime(self):
        if self.__gamestate == "":  # 게임이 진행중일 때만 업데이트
            self.__lbTimer["text"] = self.__tm.getElapsed()

    # 게임 시작 시 타이머 시작
    def startGame(self):
        self.__tm.reset()
        self.__tm.start()

# 게임 프로그램


class GameController(tk.Tk):
    # 설정 값 전달받기 위한 함수
    def setGame(self, row, col, level):
        self.__row = row
        self.__col = col
        self.__level = (level / 100)  # 참고한 파이썬 지뢰찾기 Lab 에서 랜덤한 기준으로 1미만 값을 요구함

    def __init__(self):
        super().__init__()

        # 게임 제목
        self.font = font.Font(family="Helvatica", size=30, weight="bold")
        self.title("MINESWEEPER")
        self.geometry("500x500")

        # 프레임을 담을 컨테이너
        self.__container = tk.Frame(self)
        self.__container.pack(side="top", fill="both", expand=True)
        self.__container.grid_rowconfigure(0, weight=1)
        self.__container.grid_columnconfigure(0, weight=1)

        # 게임 화면 프레임 객채
        self.__screenSizeRatio = 50  # 창 크기 조절 상수
        self.__game = Minesweeper(master=self.__container, controller=self)
        self.__game.grid(row=0, column=0, sticky="nsew")

        # 시작 화면 프레임 객체
        self.__startpage = StartPage(master=self.__container, controller=self)
        self.__startpage.grid(row=0, column=0, sticky="nsew")

        self.__currentFrame = ""        # 현재 맨 위에 올라와 있는 프레임
        self.showFrame("StartPage")    # 게임 프로그램을 실행하면 제일 먼저 시작 화면을 띄운다

        self.__row = 10  # 초기 세로 길이
        self.__col = 10  # 초기 가로 길이
        self.__level = 0.1  # 초기 레벨

    # 게임 상태에 따른 화면 전환
    def showFrame(self, frameName):
        self.__currentFrame = frameName

        # 시작 페이지로 가야 하면
        if frameName == "StartPage":
            self.__startpage = StartPage(
                master=self.__container, controller=self)
            self.__startpage.grid(row=0, column=0, sticky="nsew")
            self.__startpage.tkraise()  # 시작 페이지 화면 띄우기
            self.__game.destroy()

        # 게임 페이지로 가야 하면
        elif frameName == "GamePage":
            self.__game = Minesweeper(master=self.__container, controller=self)
            self.__game.grid(row=0, column=0, sticky="nsew")
            self.__game.initialize(self.__row, self.__col, self.__level)
            self.__game.tkraise()
            self.__game.startGame()
            self.__startpage.destroy()

    # 게임 루프
    def controllerLoop(self):
        # 게임중이 아니면
        if self.__currentFrame != "GamePage":
            self.geometry(f"400x400")  # 창 크기 고정
        # 게임중일 때
        elif self.__currentFrame == "GamePage":
            self.geometry(
                f"{self.__col * self.__screenSizeRatio}x{self.__row*self.__screenSizeRatio}")  # 창 크기 고정
            self.__game.gamestate()     # 게임 진행 상황 체크
            self.__game.updateTime()    # 게임 진행 시간 업데이트

        self.after(50, self.controllerLoop)

# 시작 화면


class StartPage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.__controller = controller    # GameController 객체

        # 게임 제목
        self.__label = tk.Label(self, text="MINESWEEPER",
                                font=self.__controller.font)
        self.__label.place(relx=0, rely=0, relwidth=1, relheight=0.25)

        # 시작화면 버튼
        # 게임 종료 버튼 누르면 게임 나가기
        self.__b1 = tk.Button(self, text="게임 종료", font=self.__controller.font)
        self.__b2 = tk.Button(self, text="게임 설정", font=self.__controller.font)
        # 게임 시작 버튼을 누르면 게임 화면 프레임 띄우기
        self.__b3 = tk.Button(self, text="게임 시작", font=self.__controller.font)
        self.__b1.place(relx=0, rely=0.75, relwidth=1, relheight=0.25)
        self.__b2.place(relx=0, rely=0.50, relwidth=1, relheight=0.25)
        self.__b3.place(relx=0, rely=0.25, relwidth=1, relheight=0.25)
        self.__b1.bind("<Button-1>", self.gameQuit)
        self.__b2.bind("<Button-1>", self.gameSetting)
        self.__b3.bind("<Button-1>", self.gameStart)
        self.__dialogFlag = True

    # 게임 설정 버튼 callback
    def gameSetting(self, event):
        if self.__dialogFlag:
            self.__dialogFlag = False
            arg = [1, 1, 1]   # row, col, level을 입력받을 변수
            Setting(arg)    # 게임 설정 대화상자 열기\
            self.__controller.setGame(*arg)   # GameController 객체에 설정 값 전달
            self.__dialogFlag = True

    def gameStart(self, event):
        if self.__dialogFlag:
            self.__controller.showFrame("GamePage")

    def gameQuit(self, event):
        if self.__dialogFlag:
            self.__controller.destroy()

# 게임 설정 대화상자


class Setting(tk.Toplevel):
    def __init__(self, arg):
        super().__init__()

        # 창 설정
        self.title("게임 설정")
        self.geometry("500x250")
        self.__font = font.Font(family="Helvatica", size=20, weight="bold")

        # 설정 값 라벨
        self.__l1 = tk.Label(self, text="세로", font=self.__font)
        self.__l2 = tk.Label(self, text="가로", font=self.__font)
        self.__l3 = tk.Label(self, text="지뢰비율(%)", font=self.__font)
        self.__l1.place(relx=0, rely=0, relwidth=1/3, relheight=0.5)
        self.__l2.place(relx=1/3, rely=0, relwidth=1/3, relheight=0.5)
        self.__l3.place(relx=2/3, rely=0, relwidth=1/3, relheight=0.5)

        # 값을 설정하게 해주는 스핀박스
        # 창의 크기는 15x20으로 제한된다. 버튼 수가 많아지면 프로그램이 느려진다.
        self.__s1 = tk.Spinbox(self, from_=1, to=15, validate="all", wrap=True)
        self.__s2 = tk.Spinbox(self, from_=1, to=20, validate="all", wrap=True)
        self.__s3 = tk.Spinbox(self, from_=1, to=100,
                               validate="all", wrap=True)
        self.__s1.place(relx=1/8, rely=0.50, relwidth=1/12, relheight=0.125)
        self.__s2.place(relx=1/8 + 1/3, rely=0.50,
                        relwidth=1/12, relheight=0.125)
        self.__s3.place(relx=1/8 + 2/3, rely=0.50,
                        relwidth=1/12, relheight=0.125)
        self.__s1.delete(0)
        self.__s2.delete(0)
        self.__s3.delete(0)
        self.__s1.insert(0, "10")
        self.__s2.insert(0, "10")
        self.__s3.insert(0, "10")

        # 확인버튼
        self.__b1 = tk.Button(self, text="확인", font=self.__font)
        self.__b1.place(relx=1/3, rely=0.75, relwidth=1/3, relheight=0.2)
        self.__b1.bind("<Button-1>", self.quit1)

        # 설정 값을 담을 변수
        self.__arg = arg

        # 창의 X 버튼 누를 시 동작
        self.protocol("WM_DELETE_WINDOW", self.quit0)

        self.mainloop()

    # 확인 버튼 callback
    def quit1(self, event):
        self.quit0()

    # 창 닫기 버튼 callback
    def quit0(self):
        self.__arg[0] = int(self.__s1.get())  # row
        self.__arg[1] = int(self.__s2.get())  # col
        self.__arg[2] = int(self.__s3.get())  # level
        self.quit()
        self.destroy()


if __name__ == "__main__":
    ctrl = GameController()
    ctrl.after(10, ctrl.controllerLoop)
    ctrl.mainloop()
