from board.move import move
from pieces.nullpiece import nullpiece
from pieces.queen import queen
import random

class AI:

    global tp
    tp=[]


    def __init__(self):
        pass


    def evaluate(self,gametiles):
        min=100000
        count=0
        count2=0
        chuk=[]
        movex=move()
        tp.clear()
        xp=self.minimax(gametiles,3,-1000000000,1000000000,False)

        for zoom in tp:
            if zoom[4]<min:
                chuk.clear()
                chuk.append(zoom)
                min=zoom[4]
            if zoom[4]==min:
                chuk.append(zoom)
        fx=random.randrange(len(chuk))
        print(tp)
        return chuk[fx][0],chuk[fx][1],chuk[fx][2],chuk[fx][3]


    def reset(self,gametiles):
        for x in range(8):
            for y in range(8):
                if gametiles[x][y].pieceonTile.tostring()=='k' or gametiles[x][y].pieceonTile.tostring()=='r':
                    gametiles[x][y].pieceonTile.moved=False


    def updateposition(self,x,y):
        a=x*8
        b=a+y
        return b

    def checkmate(self,gametiles):
        movex=move()
        if movex.checkw(gametiles)[0]=='checked':
            array=movex.movesifcheckedw(gametiles)
            if len(array)==0:
                return True

        if movex.checkb(gametiles)[0]=='checked' :
            array=movex.movesifcheckedb(gametiles)
            if len(array)==0:
                return True

    def stalemate(self,gametiles,player):
        movex=move()
        if player==False:
            if movex.checkb(gametiles)[0]=='notchecked':
                check=False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1=movex.pinnedb(gametiles,moves1,y,x)
                            if len(lx1)==0:
                                continue
                            else:
                                check=True
                            if check==True:
                                break
                    if check==True:
                        break

                if check==False:
                    return True

        if player==True:
                if movex.checkw(gametiles)[0]=='notchecked':
                    check=False
                    for x in range(8):
                        for y in range(8):
                            if gametiles[y][x].pieceonTile.alliance=='White':
                                moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                                lx1=movex.pinnedw(gametiles,moves1,y,x)
                                if len(lx1)==0:
                                    continue
                                else:
                                    check=True
                                if check==True:
                                    break
                        if check==True:
                            break

                    if check==False:
                        return True


    def minimax(self,gametiles, depth,alpha , beta ,player):
        if depth==0 or self.checkmate(gametiles)==True or self.stalemate(gametiles,player)==True:
            return self.calculateb(gametiles)
        if not player:
            minEval=100000000
            kp,ks=self.eva(gametiles,player)
            for lk in kp:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.move(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,True)
                    if evalk<minEval and depth==3:
                        tp.clear()
                        tp.append(move)
                    if evalk==minEval and depth==3:
                        tp.append(move)
                    minEval=min(minEval,evalk)
                    beta=min(beta,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break

                if beta<=alpha:
                    break
            return minEval

        else:
            maxEval=-100000000
            kp,ks=self.eva(gametiles,player)
            for lk in ks:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.movew(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,False)
                    maxEval=max(maxEval,evalk)
                    alpha=max(alpha,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break
                if beta<=alpha:
                    break

            return maxEval



    def printboard(self,gametilles):
        count = 0
        for rows in range(8):
            for column in range(8):
                print('|', end=gametilles[rows][column].pieceonTile.tostring())
            print("|",end='\n')


    def checkeva(self,gametiles,moves):
        arr=[]
        for move in moves:
            lk=[[move[2],move[3]]]
            arr.append(self.calci(gametiles,move[0],move[1],lk))

        return arr



    def eva(self,gametiles,player):
        lx=[]
        moves=[]
        kp=[]
        ks=[]
        movex=move()
        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.alliance=='Black' and player==False:
                        if movex.checkb(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedb(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            kp=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='K'):
                                ax=movex.castlingb(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([0,6])
                                        if l=='qs':
                                            moves.append([0,2])
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            lx=movex.pinnedb(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        kp.append(self.calci(gametiles,y,x,moves))


                    if gametiles[y][x].pieceonTile.alliance=='White' and player==True:
                        if movex.checkw(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedw(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            ks=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if moves==None:
                            print(y)
                            print(x)
                            print(gametiles[y][x].pieceonTile.position)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='k'):
                                ax=movex.castlingw(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([7,6])
                                        if l=='qs':
                                            moves.append([7,2])
                        if gametiles[y][x].pieceonTile.alliance=='White':
                            lx=movex.pinnedw(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        ks.append(self.calci(gametiles,y,x,moves))

        return kp,ks



    def calci(self,gametiles,y,x,moves):
        arr=[]
        jk=object
        for move in moves:
            jk=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            mk=self.calculateb(gametiles)
            gametiles[y][x].pieceonTile=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=jk
            arr.append([y,x,move[0],move[1],mk])
        return arr
  

    '''

    DO NOT ENTER UP

    '''
    
    def calculateb(self,gametiles):
        move_i = move()
        value = 0
        
        '''
        This determines the weights for each piece in different function scenarios
        '''
        white_pieces = 0
        black_pieces = 0
        ending = False
        for q in range(8):
            for w in range(8):
                if gametiles[q][w].pieceonTile.alliance == 'White':
                    white_pieces += 1
                if gametiles[q][w].pieceonTile.alliance == 'Black':
                    black_pieces += 1
        # Check if the game is in the endgame phase
        if white_pieces + black_pieces <= 10:
            ending = True
            if black_pieces - white_pieces > 3:
                piece_mobility_weights = {'P': 20, 'N': 15, 'B': 15, 'R': 30, 'Q': 30, 'K': 15,'p': 20, 'n': 15, 'b': 15, 'r': 30, 'q': 30, 'k': 15}
                piece_risk_weights = {'P': 100, 'N': 100, 'B': 100, 'R': 200, 'Q': 200, 'K': 1000,'p': 100, 'n': 100, 'b': 100, 'r': 100, 'q': 100, 'k': 1000}
                piece_ori_weights = {'P': 350, 'N': 350, 'B': 1000, 'R': 525, 'Q': 1000, 'K': 10000,'p': 350, 'n': 350, 'b': 350, 'r': 525, 'q': 1000, 'k': 10000}
                piece_pos_weights = {'P': 5, 'N': 1, 'B': 1, 'R': 1, 'Q': 1, 'K': 1,'p': 5, 'n': 1, 'b': 1, 'r': 1, 'q': 1, 'k': 1}
            else:
                piece_mobility_weights = {'P': 20, 'N': 15, 'B': 15, 'R': 30, 'Q': 30, 'K': 15,'p': 20, 'n': 15, 'b': 15, 'r': 30, 'q': 30, 'k': 15}
                piece_risk_weights = {'P': 35, 'N': 35, 'B': 35, 'R': 100, 'Q': 100, 'K': 1000,'p': 35, 'n': 35, 'b': 35, 'r': 100, 'q': 100, 'k': 1000}
                piece_ori_weights = {'P': 500, 'N': 500, 'B': 1000, 'R': 1000, 'Q': 1000, 'K': 10000,'p': 500, 'n': 500, 'b': 1000, 'r': 1000, 'q': 1000, 'k': 10000}
                piece_pos_weights = {'P': 5, 'N': 1, 'B': 1, 'R': 1, 'Q': 1, 'K': 1,'p': 5, 'n': 1, 'b': 1, 'r': 1, 'q': 1, 'k': 1}
        else:
            piece_mobility_weights = {'P': 10, 'N': 15, 'B': 15, 'R': 20, 'Q': 30, 'K': 15,'p': 10, 'n': 15, 'b': 15, 'r': 20, 'q': 30, 'k': 15,}
            piece_risk_weights = {'P': 10, 'N': 35, 'B': 35, 'R': 55, 'Q': 100, 'K': 1000,'p': 10, 'n': 35, 'b': 35, 'r': 55, 'q': 100, 'k': 1000,}
            piece_ori_weights = {'P': 100, 'N': 350, 'B': 350, 'R': 525, 'Q': 1000, 'K': 10000,'p': 100, 'n': 350, 'b': 350, 'r': 525, 'q': 1000, 'k': 10000,}
            piece_pos_weights = {'P': 1, 'N': 1, 'B': 1, 'R': 1, 'Q': 1, 'K': 1,'p': 5, 'n': 1, 'b': 1, 'r': 1, 'q': 1, 'k': 1}

        '''
        The following code will let each pieces know which positions are more encouraged for them to stay
        for most pieces, center = better
        for king, corner = better
        '''
        if white_pieces + black_pieces <= 16:
            position_values_for_piece_type =\
            {'P': [[200, 200, 200, 200, 200, 200, 200, 200],
                    [150, 150, 150, 150, 150, 150, 150, 150],
                    [80,80, 80, 80, 80, 80, 80, 80],
                    [55,55,55,55,55,55,55,55],
                    [10, 10, 15, 35, 35, 15, 10, 10],
                    [0, 0, 0, 20, 20, 0, 0, 0],
                    [5, -5, -10, 0, 0, -10, -5, 5],
                    [0, 0, 0, 0, 0, 0, 0, 0]],
            'N': [[-50, -40, -30, -30, -30, -30, -40, -50],
                    [-40,-20,0,0,0,0,-20,-40],
                    [-30,0,10,20,20,10,0,-30],
                    [-30,5,20,30,30,20,5,-30],
                    [-30,0,20,30,30,20,0,-30],
                    [-30,5,10,20,20,10,5,-30],
                    [-40,-20,0,5,5,0,-20,-40],
                    [-50, -40, -30, -30, -30, -30, -40, -50]],
            'B': [[-40,-20,-20,-20,-20,-20,-20,-40],
                    [-20,-5,-5,-5,-5,-5,-5,-20],
                    [-20,5,5,20,20,5,5,-20],
                    [-20,5,5,20,20,5,5,-20],
                    [-20,-5,20,20,20,20,-5,-20],
                    [-20,20,20,20,20,20,20,-20],
                    [-20,10,-5,-5,-5,-5,10,-20],
                    [-40,-20,-20,-20,-20,-20,-20,-40]],
            'R': [[0, 0, 0, 0, 0, 0, 0, 0],
                    [5, 10, 10, 10, 10, 10, 10, 5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [0, 0, 0, 5, 5, 0, 0, 0]],
            'Q': [[-30,-20,-20,-15,-15,-20,-20,-30],
                    [-20,0,0,0,0,0,0,-20],
                    [-20,0,10,10,10,10,0,-20],
                    [-10,0,10,10,10,10,0,-10],
                    [0,0,10,10,10,10,0,-5],
                    [-10,10,10,10,10,10,0,-10],
                    [-10,0,0,0,0,0,0,-10],
                    [-20,-10,-10,-5,-5,-10,-10,-20]],
            'K': [[-30,-40,-40,-50,-50,-40,-40,-30],
                    [-30,-40,-40,-50,-50,-40,-40,-30],
                    [-30,-40,-40,-50,-50,-40,-40,-30],
                    [-30,-40,-40,-50,-50,-40,-40,-30],
                    [-20,-30,-40,-40,-40,-30,-30,-20],
                    [-10,-20,-30,-30,-30,-20,-20,-10],
                    [20,20,0,0,0,0,20,20],
                    [20,30,10,0,0,10,30,20]],
            'p': [[0, 0, 0, 0, 0, 0, 0, 0],
                    [150, 150, 150, 150, 150, 150, 150, 150],
                    [80,80, 80, 80, 80, 80, 80, 80],
                    [55,55,55,55,55,55,55,55],
                    [10, 10, 15, 35, 35, 15, 10, 10],
                    [0, 0, 0, 20, 20, 0, 0, 0],
                    [5, -5, -10, 0, 0, -10, -5, 5],
                    [0, 0, 0, 0, 0, 0, 0, 0]],
            'n': [[-50, -40, -30, -30, -30, -30, -40, -50],
                    [-40,-20,0,0,0,0,-20,-40],
                    [-30,0,10,20,20,10,0,-30],
                    [-30,5,20,30,30,20,5,-30],
                    [-30,0,20,30,30,20,0,-30],
                    [-30,5,10,20,20,10,5,-30],
                    [-40,-20,0,5,5,0,-20,-40],
                    [-50, -40, -30, -30, -30, -30, -40, -50]],
            'b': [[-40,-20,-20,-20,-20,-20,-20,-40],
                    [-20,-5,-5,-5,-5,-5,-5,-20],
                    [-20,5,5,20,20,5,5,-20],
                    [-20,5,5,20,20,5,5,-20],
                    [-20,-5,20,20,20,20,-5,-20],
                    [-20,20,20,20,20,20,20,-20],
                    [-20,10,-5,-5,-5,-5,10,-20],
                    [-40,-20,-20,-20,-20,-20,-20,-40]],
            'r': [[0, 0, 0, 0, 0, 0, 0, 0],
                    [5, 10, 10, 10, 10, 10, 10, 5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [0, 0, 0, 5, 5, 0, 0, 0]],
            'q': [[-20,-10,-10,-5,-5,-10,-10,-20],
                    [-10,0,0,0,0,0,0,-10],
                    [-10,0,10,10,10,10,0,-10],
                    [-5,0,10,10,10,10,0,-5],
                    [0,0,10,10,10,10,0,-5],
                    [-10,10,10,10,10,10,0,-10],
                    [-10,0,0,0,0,0,0,-10],
                    [-20,-10,-10,-5,-5,-10,-10,-20]],
            'k': [[-30,-40,-40,-50,-50,-40,-40,-30],
                    [-30,-40,-40,-50,-50,-40,-40,-30],
                    [-30,-40,-40,-50,-50,-40,-40,-30],
                    [-30,-40,-40,-50,-50,-40,-40,-30],
                    [-20,-30,-40,-40,-40,-30,-30,-20],
                    [-10,-20,-30,-30,-30,-20,-20,-10],
                    [20,20,0,0,0,0,20,20],
                    [20,30,10,0,0,10,30,20]]}
                    
        else:
        
            position_values_for_piece_type =\
            {'P': [[0, 0, 0, 0, 0, 0, 0, 0],
                            [100, 100, 100, 100, 100, 100, 100, 100],
                            [50, 50, 50, 50, 50, 50, 50, 50],
                            [30,30,30,30,30,30,30,30],
                            [5, 5, 10, 25, 25, 10, 5, 5],
                            [0, 0, 0, 20, 20, 0, 0, 0],
                            [5, -5, -10, 0, 0, -10, -5, 5],
                            [0, 0, 0, 0, 0, 0, 0, 0]],
            'N': [[-50, -40, -30, -30, -30, -30, -40, -50],
                                    [-40,-20,0,0,0,0,-20,-40],
                                    [-30,0,10,15,15,10,0,-30],
                                    [-30,5,15,20,20,15,5,-30],
                                    [-30,0,15,20,20,15,0,-30],
                                    [-30,5,10,15,15,10,5,-30],
                                    [-40,-20,0,5,5,0,-20,-40],
                                    [-50, -40, -30, -30, -30, -30, -40, -50]],
            'B': [[-20,-10,-10,-10,-10,-10,-10,-20],
                                    [-10,0,0,0,0,0,0,-10],
                                    [-10,5,5,10,10,5,5,-10],
                                    [-10,5,5,10,10,5,5,-10],
                                    [-10,0,10,10,10,10,0,-10],
                                    [-10,10,10,10,10,10,10,-10],
                                    [-10,5,0,0,0,0,5,-10],
                                    [-20,-10,-10,-10,-10,-10,-10,-20]],
            'R': [[0, 0, 0, 0, 0, 0, 0, 0],
                                    [5, 10, 10, 10, 10, 10, 10, 5],
                                    [-5, 0, 0, 0, 0, 0, 0, -5],
                                    [-5, 0, 0, 0, 0, 0, 0, -5],
                                    [-5, 0, 0, 0, 0, 0, 0, -5],
                                    [-5, 0, 0, 0, 0, 0, 0, -5],
                                    [-5, 0, 0, 0, 0, 0, 0, -5],
                                    [0, 0, 0, 5, 5, 0, 0, 0]],
            'Q': [[-20,-10,-10,-5,-5,-10,-10,-20],
                                    [-10,0,0,0,0,0,0,-10],
                                    [-10,0,5,5,5,5,0,-10],
                                    [-5,0,5,5,5,5,0,-5],
                                    [0,0,5,5,5,5,0,-5],
                                    [-10,5,5,5,5,5,0,-10],
                                    [-10,0,5,0,0,0,0,-10],
                                    [-20,-10,-10,-5,-5,-10,-10,-20]],
            'K': [[-30,-40,-40,-50,-50,-40,-40,-30],
                                    [-30,-40,-40,-50,-50,-40,-40,-30],
                                    [-30,-40,-40,-50,-50,-40,-40,-30],
                                    [-30,-40,-40,-50,-50,-40,-40,-30],
                                    [-20,-30,-40,-40,-40,-30,-30,-20],
                                    [-10,-20,-30,-30,-30,-20,-20,-10],
                                    [20,20,0,0,0,0,20,20],
                                    [20,30,10,0,0,10,30,20]],
            'p': [[0, 0, 0, 0, 0, 0, 0, 0],
                            [100, 100, 100, 100, 100, 100, 100, 100],
                            [50, 50, 50, 50, 50, 50, 50, 50],
                            [30,30,30,30,30,30,30,30],
                            [5, 5, 10, 25, 25, 10, 5, 5],
                            [0, 0, 0, 20, 20, 0, 0, 0],
                            [5, -5, -10, 0, 0, -10, -5, 5],
                            [0, 0, 0, 0, 0, 0, 0, 0]],
            'n': [[-50, -40, -30, -30, -30, -30, -40, -50],
                                    [-40,-20,0,0,0,0,-20,-40],
                                    [-30,0,10,15,15,10,0,-30],
                                    [-30,5,15,20,20,15,5,-30],
                                    [-30,0,15,20,20,15,0,-30],
                                    [-30,5,10,15,15,10,5,-30],
                                    [-40,-20,0,5,5,0,-20,-40],
                                    [-50, -40, -30, -30, -30, -30, -40, -50]],
            'b': [[-20,-10,-10,-10,-10,-10,-10,-20],
                                    [-10,0,0,0,0,0,0,-10],
                                    [-10,5,5,10,10,5,5,-10],
                                    [-10,5,5,10,10,5,5,-10],
                                    [-10,0,10,10,10,10,0,-10],
                                    [-10,10,10,10,10,10,10,-10],
                                    [-10,5,0,0,0,0,5,-10],
                                    [-20,-10,-10,-10,-10,-10,-10,-20]],
            'r': [[0, 0, 0, 0, 0, 0, 0, 0],
                                    [5, 10, 10, 10, 10, 10, 10, 5],
                                    [-5, 0, 0, 0, 0, 0, 0, -5],
                                    [-5, 0, 0, 0, 0, 0, 0, -5],
                                    [-5, 0, 0, 0, 0, 0, 0, -5],
                                    [-5, 0, 0, 0, 0, 0, 0, -5],
                                    [-5, 0, 0, 0, 0, 0, 0, -5],
                                    [0, 0, 0, 5, 5, 0, 0, 0]],
            'q': [[-20,-10,-10,-5,-5,-10,-10,-20],
                                    [-10,0,0,0,0,0,0,-10],
                                    [-10,0,5,5,5,5,0,-10],
                                    [-5,0,5,5,5,5,0,-5],
                                    [0,0,5,5,5,5,0,-5],
                                    [-10,5,5,5,5,5,0,-10],
                                    [-10,0,5,0,0,0,0,-10],
                                    [-20,-10,-10,-5,-5,-10,-10,-20]],
            'k': [[-30,-40,-40,-50,-50,-40,-40,-30],
                                    [-30,-40,-40,-50,-50,-40,-40,-30],
                                    [-30,-40,-40,-50,-50,-40,-40,-30],
                                    [-30,-40,-40,-50,-50,-40,-40,-30],
                                    [-20,-30,-40,-40,-40,-30,-30,-20],
                                    [-10,-20,-30,-30,-30,-20,-20,-10],
                                    [20,20,0,0,0,0,20,20],
                                    [20,30,10,0,0,10,30,20]]}
        
        '''
        This determines how many blocks are each pieces controlling
        return the number of blocks they are controlling
        more = better
        '''
        def mobility(row,col):
            moves=gametiles[row][col].pieceonTile.legalmoveb(gametiles)
            if moves is None:
                return 0
            else:
                return len(moves)
#rEVISE
        def Kmobility(row,col):
            moves=gametiles[row][col].pieceonTile.legalmoveb(gametiles)
            if moves is None and (gametiles[row][col].pieceonTile.tostring().lower()=='k'):
                return 100
            else:
                return 0
                
        for x in range(8):
            for y in range(8):
                piece_type = gametiles[y][x].pieceonTile.tostring()
                '''
                This determines whether they are under the risk of being eaten or not
                return the number of potential attackers
                less = better
                '''
      
                def risk(row,col):
                    alli =gametiles[y][x].pieceonTile.alliance
                    if alli =='White': # For black pieces, checking if it will be under attack by white pieces
                        white_moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if white_moves and (row, col) in white_moves:
                            piece_type = gametiles[y][x].pieceonTile.tostring()
                            return 1
                    elif alli =='Black': # For white pieces, checking if it will be under attack by black pieces
                        black_moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if black_moves and (row, col) in black_moves:
                            piece_type = gametiles[y][x].pieceonTile.tostring()
                            return 1
                    return 0
                    
                '''
                Determine is there any pieces they can attack
                '''
                def attack(row, col):
                    piece = gametiles[y][x].pieceonTile
                    piece_alliance = gametiles[y][x].pieceonTile.alliance

                    if piece_alliance == 'Black':
                        black_moves = piece.legalmoveb(gametiles)
                        if black_moves is not None:
                            for move in black_moves:
                                target_piece = gametiles[move[0]][move[1]].pieceonTile
                                if target_piece.alliance == 'White' and (row, col) == (move[0], move[1]):
                                    return piece_ori_weights.get(target_piece.tostring(), 0)
                    elif piece_alliance == 'White':
                        white_moves = piece.legalmoveb(gametiles)
                        if white_moves is not None:
                            for move in white_moves:
                                target_piece = gametiles[move[0]][move[1]].pieceonTile
                                if target_piece.alliance == 'Black' and (row, col) == (move[0], move[1]):
                                    return piece_ori_weights.get(target_piece.tostring(), 0)
                    return 0
                            
                # Black -> Opponent(AI) -> Uppercase
                if piece_type in 'PNBRQK':
                    value -= piece_mobility_weights.get(piece_type, 0) * mobility(y, x)
                    value += piece_ori_weights.get(piece_type, 0) * risk(y, x)
                    value -= attack(y, x)
                    value -= piece_ori_weights.get(piece_type, 0)
                    #value -= Kmobility(y, x)
                    value -= piece_pos_weights.get(piece_type, 0) * position_values_for_piece_type[piece_type][y][x]

                # White -> Player -> Lowercase
                elif piece_type in 'pnbrqk':
                    value += piece_mobility_weights.get(piece_type, 0) * mobility(y, x)
                    value -= piece_ori_weights.get(piece_type, 0) * risk(y, x)
                    value += attack(y, x)
                    value += piece_ori_weights.get(piece_type, 0)
                    #value += Kmobility(y, x)
                    value += piece_pos_weights.get(piece_type, 0) * position_values_for_piece_type[piece_type][y][x]
        return value



    '''

    DO NOT ENTER

    '''



    def move(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='K' or gametiles[y][x].pieceonTile.tostring()=='R':
            gametiles[y][x].pieceonTile.moved=True

        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='P' and y+1==n and y==6:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='P':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('Black',self.updateposition(n,m))
                promotion=False

        return gametiles



    def revmove(self,gametiles,x,y,n,m,mts):
        if gametiles[x][y].pieceonTile.tostring()=='K':
            if m==y-2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[n][7].pieceonTile.moved=False

                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            elif m==y+2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(m,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[n][0].pieceonTile.moved=False
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts

            return gametiles

        if gametiles[x][y].pieceonTile.tostring()=='k':
            if m==y-2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            elif m==y+2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(n,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts


            return gametiles

        gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
        s=self.updateposition(n,m)
        gametiles[n][m].pieceonTile.position=s
        gametiles[x][y].pieceonTile=mts

        return gametiles



    def movew(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='k' or gametiles[y][x].pieceonTile.tostring()=='r':
            pass

        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='p' and y-1==n and y==1:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='p':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('White',self.updateposition(n,m))
                promotion=False

        return gametiles
























                        
