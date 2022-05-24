import tkinter
import random

count = 0


def do_nothing(x):
    pass


def check_move():
    if canvas.coords(player) == canvas.coords(exit):
        label.config(text="Победа!")
        master.bind("<KeyPress>", do_nothing)
    for f in fires:
        if canvas.coords(player) == canvas.coords(f):
            label.config(text="Ты проиграл!")
            master.bind("<KeyPress>", do_nothing)
    for e in enemies:
        if canvas.coords(player) == canvas.coords(e[0]):
            label.config(text="Ты проиграл!")
            master.bind("<KeyPress>", do_nothing)


def stop_enemies():
    global count
    count = 0


def move_wrap(obj, move):
    canvas.move(obj, move[0], move[1])
    if canvas.coords(obj)[0] >= 600:
        canvas.move(obj, -step * N_X, 0)

    if canvas.coords(obj)[0] + step <= 0:
        canvas.move(obj, step * N_X, 0)

    if canvas.coords(obj)[1] >= 600:
        canvas.move(obj, 0, -step * N_Y)

    if canvas.coords(obj)[1] + step <= 0:
        canvas.move(obj, 0, step * N_Y)


def key_pressed(event):
    global count
    if event.keysym == 'Up':
        move_wrap(player, (0, -step))
    if event.keysym == 'Down':
        move_wrap(player, (0, step))
    if event.keysym == 'Left':
        move_wrap(player, (-step, 0))
    if event.keysym == 'Right':
        move_wrap(player, (step, 0))
    if count >= 3:
        for enemy in enemies:
            if enemy[1] == smart_move:
                direction = enemy[1](canvas.coords(enemy[0]))
            else:
                direction = enemy[1]()  # вызвать функцию перемещения у "врага"
            move_wrap(enemy[0], direction)  # произвести  перемещение
    count += 1
    check_move()


def always_right():
    return (step, 0)


def random_move():
    return random.choice([(step, 0), (-step, 0), (0, step), (0, -step)])


def smart_move(coord):
    move = [0, 0]
    if canvas.coords(player)[0] > coord[0]:
        move[0] = step
    elif canvas.coords(player)[0] < coord[0]:
        move[0] = -step
    if move[0] == 0:
        if canvas.coords(player)[1] > coord[1]:
            move[1] = step
        elif canvas.coords(player)[1] < coord[1]:
            move[1] = -step
    return (move[0], move[1])


def gen_pos():
    pos = (random.randint(0, N_X - 1) * step,
           random.randint(0, N_Y - 1) * step)
    while pos in list_pos:
        pos = (random.randint(0, N_X - 1) * step,
               random.randint(0, N_Y - 1) * step)
    list_pos.append(pos)
    return pos


def prepare_and_start():
    global player, exit, fires, enemies, list_pos, count
    canvas.delete("all")
    count = 3
    list_pos = []
    player_pos = gen_pos()
    player = canvas.create_image(player_pos, image=player_pic, anchor='nw')

    exit_pos = gen_pos()
    exit = canvas.create_image(exit_pos, image=exit_pic, anchor='nw')

    N_FIRES = 6  #Число клеток, заполненных огнем
    fires = []
    for i in range(N_FIRES):
        fire_pos = gen_pos()
        fire = canvas.create_image(fire_pos, image=fire_pic, anchor='nw')
        fires.append(fire)
    N_ENEMIES = 4  #Число врагов
    enemies = []
    for i in range(N_ENEMIES):
        enemy_pos = gen_pos()
        enemy = canvas.create_image(enemy_pos, image=enemy_pic, anchor='nw')
        enemies.append(
            (enemy, random.choice([always_right, random_move, smart_move])))
    label.config(text="Найди выход!")
    master.bind("<KeyPress>", key_pressed)


step = 60  # Размер клетки
N_X = 10
N_Y = 10  # Размер сетки
master = tkinter.Tk()
label = tkinter.Label(master, text="Найди выход")
label.pack()
canvas = tkinter.Canvas(master,
                        bg='black',
                        height=N_X * step,
                        width=N_Y * step)
canvas.pack()
restart = tkinter.Button(master,
                         text="Начать заново",
                         command=prepare_and_start)
sbutton = tkinter.Button(master,
                         text="Остановка врагов на 3 шага",
                         command=stop_enemies)
sbutton.pack()
restart.pack()
player_pic = tkinter.PhotoImage(file="C:\\Users\\arsen\\1\\game\\player.png.png")
exit_pic = tkinter.PhotoImage(file="C:\\Users\\arsen\\1\\game\\exit.png.png")
fire_pic = tkinter.PhotoImage(file="C:\\Users\\arsen\\1\\game\\fire.png.png")
enemy_pic = tkinter.PhotoImage(file="C:\\Users\\arsen\\1\\game\\enemy.png.png")
prepare_and_start()
master.mainloop()
