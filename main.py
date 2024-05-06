import pygame
import random
from pieceEval import PieceEvaluation
pygame.init()
WIDTH = 800
HEIGHT = 640
SQUARE_SIZE = min(WIDTH, HEIGHT) // 8
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Pygame Chess!')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60

# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []

class Button:
    def __init__(self, x, y, width, height, text,level):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.level = level

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
captured_pieces_white = []
captured_pieces_black = []

# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
black_queen = pygame.image.load('assets/images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
black_queen_small = pygame.transform.scale(black_queen, (SQUARE_SIZE/2 - 5, SQUARE_SIZE/2 - 5))
black_king = pygame.image.load('assets/images/black king.png')
black_king = pygame.transform.scale(black_king, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
black_king_small = pygame.transform.scale(black_king, (SQUARE_SIZE/2 - 5, SQUARE_SIZE/2 - 5))
black_rook = pygame.image.load('assets/images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
black_rook_small = pygame.transform.scale(black_rook, (SQUARE_SIZE/2 - 5, SQUARE_SIZE/2 - 5))
black_bishop = pygame.image.load('assets/images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
black_bishop_small = pygame.transform.scale(black_bishop, (SQUARE_SIZE/2 - 5, SQUARE_SIZE/2 - 5))
black_knight = pygame.image.load('assets/images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
black_knight_small = pygame.transform.scale(black_knight, (SQUARE_SIZE/2 - 5, SQUARE_SIZE/2 - 5))
black_pawn = pygame.image.load('assets/images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (SQUARE_SIZE/2 + 15, SQUARE_SIZE/2 + 15))
black_pawn_small = pygame.transform.scale(black_pawn, (SQUARE_SIZE/2 - 5, SQUARE_SIZE/2 - 5))
white_queen = pygame.image.load('assets/images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
white_queen_small = pygame.transform.scale(white_queen, (SQUARE_SIZE/2 - 5, SQUARE_SIZE/2 - 5))
white_king = pygame.image.load('assets/images/white king.png')
white_king = pygame.transform.scale(white_king, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
white_king_small = pygame.transform.scale(white_king, (SQUARE_SIZE/2 - 5, SQUARE_SIZE/2 - 5))
white_rook = pygame.image.load('assets/images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
white_rook_small = pygame.transform.scale(white_rook, (SQUARE_SIZE/2 - 5, SQUARE_SIZE/2 - 5))
white_bishop = pygame.image.load('assets/images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
white_bishop_small = pygame.transform.scale(white_bishop, (SQUARE_SIZE/2 - 5, SQUARE_SIZE/2 - 5))
white_knight = pygame.image.load('assets/images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
white_knight_small = pygame.transform.scale(white_knight, (SQUARE_SIZE/2 - 5, SQUARE_SIZE/2 - 5))
white_pawn = pygame.image.load('assets/images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (SQUARE_SIZE/2 + 15, SQUARE_SIZE/2 + 15))
white_pawn_small = pygame.transform.scale(white_pawn, (SQUARE_SIZE/2 - 5, SQUARE_SIZE/2 - 5))
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']


# check variables/ flashing counter
counter = 0
winner = ''
game_over = False

def draw_board2():
    for row in range(8):
        for column in range(8):
            color = 'white' if (row + column) % 2 == 0 else 'light gray'
            pygame.draw.rect(screen, color, [column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE])

def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * SQUARE_SIZE + 10, white_locations[i][1] * SQUARE_SIZE + 10))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * SQUARE_SIZE + 10, white_locations[i][1] * SQUARE_SIZE + 10))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * SQUARE_SIZE + 1, white_locations[i][1] * SQUARE_SIZE + 1,
                                                 SQUARE_SIZE, SQUARE_SIZE], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * SQUARE_SIZE + 10, black_locations[i][1] * SQUARE_SIZE + 10))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * SQUARE_SIZE + 10, black_locations[i][1] * SQUARE_SIZE + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * SQUARE_SIZE + 1, black_locations[i][1] * SQUARE_SIZE + 1,
                                                  SQUARE_SIZE, SQUARE_SIZE], 2)

def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list

def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in white_locations and \
                (position[0], position[1] + 2) not in black_locations and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in white_locations and \
                (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list

def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list

def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options

# draw captured pieces on side of screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))

def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * SQUARE_SIZE + 50, moves[i][1] * SQUARE_SIZE + 50), 5)


def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * SQUARE_SIZE + 1,
                                                              white_locations[king_index][1] * SQUARE_SIZE + 1, SQUARE_SIZE, SQUARE_SIZE], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * SQUARE_SIZE + 1,
                                                               black_locations[king_index][1] * SQUARE_SIZE + 1, SQUARE_SIZE, SQUARE_SIZE], 5)


def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))

def draw_chooseOption(is_clicked,list_button):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Button Example")
    while is_clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in list_button:
                    if button.is_clicked(pygame.mouse.get_pos()):
                        is_clicked = False
                        return button.level

        screen.fill(WHITE)
        for button in list_button:
            button.draw(screen)
        pygame.display.flip()

def board_scoreVer2(white_pieces,black_pieces,white_locations,black_locations):
    white_score = 0
    black_score = 0
    evaluator = PieceEvaluation()
    i = 0
    for white_piece in white_pieces:
        x = white_locations[i][0]
        y = white_locations[i][1]
        white_score += evaluator.evaluate_piece(white_piece,x,y,'white')
        i += 1
    
    i = 0
    for black_piece in black_pieces:
        x = black_locations[i][0]
        y = black_locations[i][1]
        black_score += evaluator.evaluate_piece(black_piece,x,y,'black')
        i +=1
    return white_score + black_score

def board_score(white_pieces, black_pieces):
    white_score = 0
    black_score = 0
    for white_piece in white_pieces:
        if white_piece == 'pawn':
            white_score -= 1
        elif white_piece == 'rook':
            white_score -= 5
        elif white_piece == 'knight':
            white_score -= 3
        elif white_piece == 'bishop':
            white_score -= 3
        elif white_piece == 'queen':
            white_score -= 10
        elif white_piece == 'king':
            white_score -= 100
    for black_piece in black_pieces:
        if black_piece == 'pawn':
            black_score += 1
        elif black_piece == 'rook':
            black_score += 5
        elif black_piece == 'knight':
            black_score += 3
        elif black_piece == 'bishop':
            black_score += 3
        elif black_piece == 'queen':
            black_score += 10
        elif black_piece == 'king':
            black_score += 100
    return white_score + black_score

def get_new_state(black_pieces,white_pieces,black_locations,white_locations,start_pos,move):
    new_black_locations = black_locations.copy()
    new_black_pieces = black_pieces.copy()
    new_white_locations = white_locations.copy()
    new_white_pieces = white_pieces.copy()
    if start_pos in new_black_locations:
        selection = new_black_locations.index(start_pos)
        if move in new_white_locations:
            white_piece = new_white_locations.index(move)
            new_black_locations[selection] = move
            new_white_pieces.pop(white_piece)
            new_white_locations.pop(white_piece)
    elif start_pos in new_white_locations:
        selection = new_white_locations.index(start_pos)
        if move in new_black_locations:
            black_piece = new_black_locations.index(move)
            new_white_locations[selection] = move
            new_black_pieces.pop(black_piece)
            new_black_locations.pop(black_piece)
    return board_score(new_white_pieces,new_black_pieces),new_black_pieces,new_white_pieces,new_black_locations,new_white_locations


def get_new_stateVer2(black_pieces,white_pieces,black_locations,white_locations,start_pos,move):
    new_black_locations = black_locations.copy()
    new_black_pieces = black_pieces.copy()
    new_white_locations = white_locations.copy()
    new_white_pieces = white_pieces.copy()
    if start_pos in new_black_locations:
        selection = new_black_locations.index(start_pos)
        if move in new_white_locations:
            white_piece = new_white_locations.index(move)
            new_black_locations[selection] = move
            new_white_pieces.pop(white_piece)
            new_white_locations.pop(white_piece)
    elif start_pos in new_white_locations:
        selection = new_white_locations.index(start_pos)
        if move in new_black_locations:
            black_piece = new_black_locations.index(move)
            new_white_locations[selection] = move
            new_black_pieces.pop(black_piece)
            new_black_locations.pop(black_piece)

    return board_scoreVer2(new_white_pieces,new_black_pieces,new_white_locations,new_black_locations),new_black_pieces,new_white_pieces,new_black_locations,new_white_locations


#level0 + 1
def minimax(black_pieces,white_pieces,black_locations,white_locations,depth,maximizingPlayer):
    if depth == 0 : 
        return board_score(white_pieces,black_pieces),None,None
    if maximizingPlayer:
        value = float('-inf')
        possible_moves = check_options(black_pieces,black_locations,'black')
        i = 0
        for moves in possible_moves:
            sp = black_locations[i]
            i+=1
            for move in moves:
                child,nbp,nwp,nbl,nwl = get_new_state(black_pieces,white_pieces,black_locations,white_locations,sp,move)
                tmp,_,_ = minimax(nbp,nwp,nbl,nwl,depth-1,False,alpha,beta)
                if tmp > value :
                    value = tmp
                    start_pos = sp
                    end_pos = move
        
    else:
        value = float('inf')
        possible_moves = check_options(white_pieces,white_locations,'white')
        i = 0
        for moves in possible_moves:
            sp = white_locations[i]
            i+=1
            for move in moves:
                child,nbp,nwp,nbl,nwl = get_new_state(black_pieces,white_pieces,black_locations,white_locations,sp,move)
                tmp,_,_ = minimax(nbp,nwp,nbl,nwl,depth-1,True,alpha,beta)
                if tmp < value :
                    value = tmp
                    start_pos = sp
                    end_pos = move
    return value,start_pos,end_pos

#level 2 + 3
def minimax1(black_pieces,white_pieces,black_locations,white_locations,depth,maximizingPlayer,alpha = float('-inf'),beta = float('inf')):
    if depth == 0 : 
        return board_score(white_pieces,black_pieces),None,None
    if maximizingPlayer:
        value = float('-inf')
        possible_moves = check_options(black_pieces,black_locations,'black')
        i = 0
        for moves in possible_moves:
            sp = black_locations[i]
            i+=1
            for move in moves:
                child,nbp,nwp,nbl,nwl = get_new_state(black_pieces,white_pieces,black_locations,white_locations,sp,move)
                tmp,_,_ = minimax1(nbp,nwp,nbl,nwl,depth-1,False,alpha,beta)
                if tmp > value :
                    value = tmp
                    start_pos = sp
                    end_pos = move
                if value >= beta:
                    break
                alpha = max(alpha,value)
        
    else:
        value = float('inf')
        possible_moves = check_options(white_pieces,white_locations,'white')
        i = 0
        for moves in possible_moves:
            sp = white_locations[i]
            i+=1
            for move in moves:
                child,nbp,nwp,nbl,nwl = get_new_state(black_pieces,white_pieces,black_locations,white_locations,sp,move)
                tmp,_,_ = minimax1(nbp,nwp,nbl,nwl,depth-1,True,alpha,beta)
                if tmp < value :
                    value = tmp
                    start_pos = sp
                    end_pos = move
                if value <= alpha:
                    break
                beta = min(beta,value)
    return value,start_pos,end_pos

#level 4 + 5

def minimax2(black_pieces,white_pieces,black_locations,white_locations,depth,maximizingPlayer,alpha = float('-inf'),beta = float('inf')):
    if depth == 0 : 
        return board_score(white_pieces,black_pieces),None,None
    if maximizingPlayer:
        value = float('-inf')
        black_locations_copy = black_locations.copy()
        black_pieces_copy = black_pieces.copy()
        possible_moves = check_options(black_pieces,black_locations_copy,'black')
        paired_lists = list(zip(possible_moves, black_locations_copy,black_pieces_copy))
        random.shuffle(paired_lists)
        shuffled_possible_move, shuffled_black_locations,shuffle_black_pieces = zip(*paired_lists)
        shuffled_black_locations = list(shuffled_black_locations)
        shuffle_black_pieces = list(shuffle_black_pieces)
        i = 0
        for moves in shuffled_possible_move:
            sp = shuffled_black_locations[i]
            i+=1
            for move in moves:
                child,nbp,nwp,nbl,nwl = get_new_state(shuffle_black_pieces,white_pieces,shuffled_black_locations,white_locations,sp,move)
                tmp,_,_ = minimax2(nbp,nwp,nbl,nwl,depth-1,False,alpha,beta)
                if tmp > value :
                    value = tmp
                    start_pos = sp
                    end_pos = move
                if value >= beta:
                    break
                alpha = max(alpha,value)
        
    else:
        value = float('inf')
        possible_moves = check_options(white_pieces,white_locations,'white')
        white_locations_copy = white_locations.copy()
        white_pieces_copy = white_pieces.copy()
        possible_moves = check_options(white_pieces_copy,white_locations_copy,'white')
        paired_lists = list(zip(possible_moves, white_locations_copy,white_pieces_copy))
        random.shuffle(paired_lists)
        shuffled_possible_move, shuffled_white_locations,shuffle_white_pieces = zip(*paired_lists)
        shuffled_white_locations = list(shuffled_white_locations)
        shuffle_white_pieces = list(shuffle_white_pieces)
        i = 0
        for moves in shuffled_possible_move:
            sp = shuffled_white_locations[i]
            i+=1
            for move in moves:
                child,nbp,nwp,nbl,nwl = get_new_state(black_pieces,shuffle_white_pieces,black_locations,shuffled_white_locations,sp,move)
                tmp,_,_ = minimax2(nbp,nwp,nbl,nwl,depth-1,True,alpha,beta)
                if tmp < value :
                    value = tmp
                    start_pos = sp
                    end_pos = move
                if value <= alpha:
                    break
                beta = min(beta,value)
    return value,start_pos,end_pos


def minimax3(black_pieces,white_pieces,black_locations,white_locations,depth,maximizingPlayer,alpha = float('-inf'),beta = float('inf')):
    if depth == 0 : 
        return board_scoreVer2(white_pieces,black_pieces,white_locations,black_locations),None,None
    if maximizingPlayer:
        value = float('-inf')
        black_locations_copy = black_locations.copy()
        black_pieces_copy = black_pieces.copy()
        possible_moves = check_options(black_pieces,black_locations_copy,'black')
        paired_lists = list(zip(possible_moves, black_locations_copy,black_pieces_copy))
        random.shuffle(paired_lists)
        shuffled_possible_move, shuffled_black_locations,shuffle_black_pieces = zip(*paired_lists)
        shuffled_black_locations = list(shuffled_black_locations)
        shuffle_black_pieces = list(shuffle_black_pieces)
        i = 0
        for moves in shuffled_possible_move:
            sp = shuffled_black_locations[i]
            i+=1
            for move in moves:
                child,nbp,nwp,nbl,nwl = get_new_stateVer2(shuffle_black_pieces,white_pieces,shuffled_black_locations,white_locations,sp,move)
                tmp,_,_ = minimax3(nbp,nwp,nbl,nwl,depth-1,False,alpha,beta)
                if tmp > value :
                    value = tmp
                    start_pos = sp
                    end_pos = move
                if value >= beta:
                    break
                alpha = max(alpha,value)
        
    else:
        value = float('inf')
        possible_moves = check_options(white_pieces,white_locations,'white')
        white_locations_copy = white_locations.copy()
        white_pieces_copy = white_pieces.copy()
        possible_moves = check_options(white_pieces_copy,white_locations_copy,'white')
        paired_lists = list(zip(possible_moves, white_locations_copy,white_pieces_copy))
        random.shuffle(paired_lists)
        shuffled_possible_move, shuffled_white_locations,shuffle_white_pieces = zip(*paired_lists)
        shuffled_white_locations = list(shuffled_white_locations)
        shuffle_white_pieces = list(shuffle_white_pieces)
        i = 0
        for moves in possible_moves:
            sp = white_locations[i]
            i+=1
            for move in moves:
                child,nbp,nwp,nbl,nwl = get_new_stateVer2(black_pieces,white_pieces,black_locations,white_locations,sp,move)
                tmp,_,_ = minimax3(nbp,nwp,nbl,nwl,depth-1,True,alpha,beta)
                if tmp < value :
                    value = tmp
                    start_pos = sp
                    end_pos = move
                if value <= alpha:
                    break
                beta = min(beta,value)
    return value,start_pos,end_pos



button0 = Button(50, 100, 100, 50, "Level 0",0)
button1 = Button(200, 100, 100, 50, "Level 1",1)
button2 = Button(350, 100, 100, 50, "Level 2",2)
button3 = Button(500, 100, 100, 50, "Level 3",3)
button4 = Button(50, 250, 100, 50, "Level 4",4)
button5 = Button(200, 250, 100, 50, "Level 5",5)
button6 = Button(350, 250, 100, 50, "Level 6",6)
button7 = Button(500, 250, 100, 50, "Level 7",7)
list_button = [button0,button1,button2,button3,button4,button5,button6,button7]

level = draw_chooseOption(True,list_button)




turn_step = 0
run = True
#ai_turn = False
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')



while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    draw_board2()
    draw_pieces()
    draw_captured()
    draw_check()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // SQUARE_SIZE
            y_coord = event.pos[1] // SQUARE_SIZE
            click_coords = (x_coord, y_coord)
            if turn_step <= 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'black'
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []
        if turn_step > 1 :
            if level == 0:
                _,start_pos,end_pos = minimax(black_pieces,white_pieces,black_locations,white_locations,2,True)
            elif level == 1:
                _,start_pos,end_pos = minimax(black_pieces,white_pieces,black_locations,white_locations,3,True)
            elif level == 2 :
                _,start_pos,end_pos = minimax1(black_pieces,white_pieces,black_locations,white_locations,2,True)
            elif level == 3:
                _,start_pos,end_pos = minimax1(black_pieces,white_pieces,black_locations,white_locations,3,True)
            elif level == 4 :
                _,start_pos,end_pos = minimax2(black_pieces,white_pieces,black_locations,white_locations,2,True)
            elif level == 5 :
                _,start_pos,end_pos = minimax2(black_pieces,white_pieces,black_locations,white_locations,3,True)
            elif level == 6:
                _,start_pos,end_pos = minimax3(black_pieces,white_pieces,black_locations,white_locations,2,True)
            elif level == 7:
                _,start_pos,end_pos = minimax3(black_pieces,white_pieces,black_locations,white_locations,3,True)
            click_coords = start_pos
            if click_coords == (8, 8) or click_coords == (9, 8):
                winner = 'white'
            if click_coords in black_locations:
                selection = black_locations.index(click_coords)
                if turn_step == 2:
                    turn_step = 3
                click_coords = end_pos
            if  click_coords in valid_moves and selection != 100:
                
                black_locations[selection] = click_coords
                
                if click_coords in white_locations:
                    white_piece = white_locations.index(click_coords)
                    captured_pieces_black.append(white_pieces[white_piece])
                    if white_pieces[white_piece] == 'king':
                        winner = 'black'
                    white_pieces.pop(white_piece)
                    white_locations.pop(white_piece)
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
                turn_step = 0
                selection = 100
                valid_moves = []
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')

    if winner != '':
        game_over = True
        draw_game_over()

    pygame.display.flip()
pygame.quit()