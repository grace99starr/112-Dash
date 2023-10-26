from cmu_graphics import *
from PIL import Image, ImageDraw
import random
import os, pathlib

#import all images and sprites

#sprite source: https://giphy.com/stickers/yellow-sparkles-NpMOXmJNHFD3IO9Xto
sparklesstrip = Image.open(os.path.join(pathlib.Path(__file__).parent,"sparkles.gif"))
sparkles = []
for i in range(6):
    sprite = CMUImage(sparklesstrip.crop((30+260*i, 30, 230+260*i, 250)))
    sparkles.append(sprite)

#sprite source: https://gifdb.com/sparkle
rocketduststrip = Image.open(os.path.join(pathlib.Path(__file__).parent,"rocketdust.gif"))
rocketdust = []
for i in range(6):
    sprite = CMUImage(rocketduststrip.crop((30+260*i, 30, 230+260*i, 250)))
    rocketdust.append(sprite)

#image source: https://steamcommunity.com/sharedfiles/filedetails/?id=471014786
settings = Image.open(os.path.join(pathlib.Path(__file__).parent,"settings.png"))
settingsIm = CMUImage(settings)

#image source: https://steamcommunity.com/sharedfiles/filedetails/?id=471014786
playButton = Image.open(os.path.join(pathlib.Path(__file__).parent,"playbutton.png"))
playButtonIm = CMUImage(playButton)

#image source: https://steamcommunity.com/sharedfiles/filedetails/?id=471014786
block = Image.open(os.path.join(pathlib.Path(__file__).parent,"block0.png"))
blockIm = CMUImage(block)

#image source: https://geometrydashscratch.com/geometry-dash-high-hill
ground = Image.open(os.path.join(pathlib.Path(__file__).parent,"ground0.png"))
groundIm = CMUImage(ground)

#image source: https://forums.getpaint.net/topic/111186-how-to-make-this-effect/
pattern = Image.open(os.path.join(pathlib.Path(__file__).parent,"background.png"))
patternIm = CMUImage(pattern)

#image source: https://www.istockphoto.com/vector/cartoon-crown-gm860347166-142317011
crown = Image.open(os.path.join(pathlib.Path(__file__).parent,"crown.png"))
crownIm = CMUImage(crown)

#image source: https://www.shutterstock.com/image-vector/lock-icon-long-shadow-white-isolated-757466449
lock = Image.open(os.path.join(pathlib.Path(__file__).parent,"lock.png"))
lockIm = CMUImage(lock)


def onAppStart(app):
    app.paused = True

    #intialize gameplay when app is first started
    restartApp(app, 'cyan', 1, False, False, 'pink', 'orange', 'pink', 'black', 
               None, None, None, None, None, 0, 0, 0, 0, 1)

def restartApp(app, blockFill, difficulty, switch, fly, easyColor, medColor, 
               hardColor, cyanBorder, pinkBorder, greenBorder, coralBorder, 
               cornBorder, plumBorder, highScore1, highScore2, highScore3, starCount,
               attempts):
    app.stepsPerSecond = 500
    app.paused = True
    app.gameOver = False
    app.attempts = attempts
    app.difficulty = difficulty
    app.score = 0
    app.highScore1 = highScore1
    app.highScore2 = highScore2
    app.highScore3 = highScore3
    app.newHigh = False
    app.starCount = starCount
    app.starMessage = 0
    app.welcomeScreen = True
    app.settingsScreen = False
    app.scoresScreen = False
    app.easyColor = easyColor
    app.medColor = medColor
    app.hardColor = hardColor
    app.cyanBorder = cyanBorder
    app.pinkBorder = pinkBorder
    app.greenBorder = greenBorder
    app.coralBorder = coralBorder
    app.cornBorder = cornBorder
    app.plumBorder = plumBorder
    app.blockScreen = False
    app.bg = 'white'
    app.groundHeight = 300
    app.currGroundHeight = 300
    app.extraSeparation = False
    app.blockX = 100
    app.blockY = 275
    app.blockV = 22
    app.blockNorm = 275
    app.ceil = 50
    app.blockFill = blockFill
    app.blockWidth = 25 
    app.blockHeight = 25
    app.blockCX = app.blockX + app.blockWidth*0.5
    app.blockCY = app.blockY + app.blockWidth*0.5
    app.jumping = False
    app.holding = False
    app.regularZone = True
    app.switchZone = False
    app.switching = False
    app.switchDirections = switch
    app.flyZone = False
    app.flyDirections = fly
    app.currZoneScore = 0
    app.currZoneEnd = random.randint(2500, 3000)
    app.transition = False
    app.up = False
    app.down = True
    app.dt = 0.06
    app.spriteCounter = 0
    app.sparkles = sparkles
    app.rocketdust = rocketdust
    app.currObstacles = [getRandomObstacle(app, app.width)]
    app.pastObstacles = []
    app.characterBlock = CharacterBlock(app.blockX, app.blockY, app.blockV, app.blockV, app.blockWidth, app.blockFill)
    app.sensitiveRadius = distance(app.characterBlock.x, app.characterBlock.x - app.characterBlock.width,
                                app.characterBlock.y, app.characterBlock.y - app.characterBlock.width)*.45

class CharacterBlock:
    gravity  = -3.5

    def __init__(self, x, y, vx, vy, width, fill):
        #set block position, velocity, acceleration
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.width = width
        self.ax, self.ay = 0, CharacterBlock.gravity
        self.fill = fill
        self.cx = self.x + 0.5*self.width
        self.cy = self.y + 0.5*self.width
        self.angle = 0

    def draw(self, width, height):
        drawRect(self.x, self.y, width, height, fill=self.fill, border='white', rotateAngle=self.angle)
        
    def drawFlyer(self):
        drawRect(self.x - 10, self.y + 25, 45, 10, fill='grey',border=self.fill,opacity=70)
        drawRect(self.x - 15, self.y + 10, 10, 20, fill = 'grey', border=self.fill, opacity=70)

    def fall(self, dt, groundHeight):
        #update position and velocity
        self.y += self.vy*dt
        self.cy = self.y + 0.5*self.width
        self.vy -= self.ay*dt

        #if block is below groundheight, stop falling
        if self.y + self.width > groundHeight:
            self.vy = 20
            self.y = groundHeight - self.width
            self.cy = self.y + self.width*0.5

    def jump(self, dt, groundHeight):
        #update position and velocity
        self.vy += self.ay*dt
        self.y -= self.vy*dt
        self.cy = self.y + 0.5*self.width
        self.angle += 1

        #if block is below groundheight, stop jumping
        if self.y + self.width > groundHeight:
            self.vy = 20
            self.ay = CharacterBlock.gravity
            self.y = groundHeight - self.width
            self.cy = self.y + self.width*0.5
            self.angle = 0

            #return False if jump is complete
            return False
        #return True if jump is still occurring
        return True
    
    def switch(self, dt, groundHeight, up):
        self.vy = 45

        #update position
        if up:
            self.y -= self.vy*dt
            self.cy = self.y + self.width*0.5
            if self.y < groundHeight:
                self.y = groundHeight
                self.cy = self.y + self.width*0.5
                self.vy = 22
                return False
        else:
            self.y += self.vy*dt
            self.cy = self.y + self.width*0.5
            if self.y + self.width > groundHeight:
                self.y = groundHeight - self.width
                self.cy = self.y + self.width*0.5
                self.vy = 22

                #return False if switch is complete
                return False
        #return True if switch is still occurring
        return True
    
    def fly(self, dt, groundHeight, ceilHeight, up):
        self.vy = 15

        #update positon
        if up:
            self.y -= self.vy*dt
            self.cy = self.y + self.width*0.5
            if self.y < ceilHeight:
                self.y = ceilHeight
                self.cy = self.y + self.width*0.5
                self.vy = 15
        else:
            self.y += self.vy*dt
            self.cy = self.y + self.width*0.5
            if self.y + self.width > groundHeight:
                self.y = groundHeight - self.width
                self.cy = self.y + self.width*0.5
                self.vy = 22


class BlockObstacle:
    def __init__(self, initialX, fill):
        self.fill = fill
        self.x = initialX
        self.numBlocks = random.randint(3,6)
        self.height = 25
        self.width = self.numBlocks*self.height
        self.groundHeight = 300
        self.relativeHeight = self.height

    def draw(self, obstacleX, obstacleY, groundHeight):
        for block in range(self.numBlocks):
            drawRect(obstacleX + block*self.height, obstacleY,
                self.height, self.height, fill=self.fill, border='white',opacity=80)

class TriangleObstacle:
    def __init__(self, initialX, fill):
        self.fill = fill
        self.x = initialX
        self.numTriangles = random.randint(1,4)
        self.height = 25
        self.widthOfEach = 25
        self.width = self.numTriangles*self.height
        self.groundHeight = 300
        self.relativeHeight = self.height
        self.upsidedown = False
        self.sensitivePoints = []

    def draw(self, obstacleX, obstacleY, groundHeight):
        points = []

        if not self.upsidedown:
            #draw regular triangles
            for triangle in range(self.numTriangles):
                drawPolygon(obstacleX + triangle*self.height, obstacleY + self.height,
                        obstacleX + self.height*0.5 + triangle*self.height,
                        obstacleY, obstacleX + self.height + triangle*self.height,
                        obstacleY + self.height, fill=self.fill, border='white', opacity=80)
            
                #get sensitive points
                sensitivePoints(self, obstacleX, obstacleY, groundHeight, triangle, 6)
                points += self.sensitivePoints
        else:
            #draw upsidedown triangles
            for triangle in range(self.numTriangles):
                drawPolygon(obstacleX + triangle*self.height, self.groundHeight, 
                            obstacleX + self.height*0.5 + triangle*self.height, 
                            self.groundHeight + self.height, 
                            obstacleX + self.height + triangle*self.height, self.groundHeight,
                            fill=self.fill, border='white', opacity=80)
            
                #get sensitive points
                sensitivePointsUpsidedown(self, obstacleX, self.groundHeight + self.height, self.groundHeight, triangle, 6)
                points += self.sensitivePoints
        return points

class BigTriangleObstacle:
    def __init__(self, initialX, fill):
        self.fill = fill
        self.x = initialX
        self.height = random.randint(35, 45)
        self.widthOfEach = self.width = random.randint(25, 30)
        self.groundHeight = 300
        self.relativeHeight = self.height
        self.upsidedown = False
        self.sensitivePoints = []

    def draw(self, obstacleX, obstacleY, groundHeight):
        if not self.upsidedown:
            #draw regular triangles
            drawPolygon(obstacleX, obstacleY + self.height,
                        obstacleX + self.widthOfEach*0.5,
                        obstacleY, obstacleX + self.widthOfEach,
                        obstacleY + self.height, fill=self.fill, border='white')
        
            #get sensitive points
            sensitivePoints(self, obstacleX, obstacleY, self.groundHeight, 0, 6)

        else:
            #draw upsidedown triangles
            drawPolygon(obstacleX, self.groundHeight, 
                        obstacleX + self.height*0.5, 
                        self.groundHeight + self.height, 
                        obstacleX + self.height, self.groundHeight,
                        fill=self.fill, border='white', opacity=80)
            
            #get sensitive points
            sensitivePointsUpsidedown(self, obstacleX, self.groundHeight + self.height, self.groundHeight, 0, 6)


class BlockAndTriangleObstacle:
    def __init__(self, initialX, fill):
        self.fill = fill
        self.x = initialX
        self.height = 25
        self.widthOfEach = 25
        self.groundHeight = 300
        self.blockOb = BlockObstacle(self.x, self.fill)
        self.triangleOb = TriangleObstacle(self.x, self.fill)
        self.width = self.blockOb.numBlocks*self.widthOfEach
        self.sensitivePoints = []
        
    def draw(self, obstacleX, obstacleY, groundHeight):
        block = self.blockOb
        block.fill = self.fill
        if block.numBlocks < 4:
            block.numBlocks = 4
        block.draw(obstacleX, groundHeight - block.height, groundHeight)
        triangle = self.triangleOb
        triangle.fill = self.fill
        triangle.numTriangles = block.numBlocks - 3
        points = triangle.draw(obstacleX + 75, obstacleY - triangle.height, groundHeight - block.height)
        self.sensitivePoints = points

class FlyingObstacle:
    def __init__(self, initialX, fill):
        self.fill = fill
        self.x = initialX
        self.blockObs = []
        self.numBlocks = 0

        #randomly set block number
        for _ in range(random.randint(2,5)):
            self.numBlocks += 1
            self.blockObs.append(BlockObstacle(self.x, self.fill))

        self.triangleOb = TriangleObstacle(self.x, self.fill)
        self.triangleOb.numTriangles = 1
        self.triangleOb.groundHeight -= len(self.blockObs)*25
        self.widthOfEach = self.width = 25
        self.height = (self.numBlocks + 1)*self.width
        self.groundHeight = 300
        self.upsidedown = False
        self.sensitivePoints = []
    
    def draw(self, obstacleX, obstacleY, groundHeight):
        #draw rightsideup obstacles
        if not self.upsidedown:
            for block in range(len(self.blockObs)):
                drawRect(obstacleX, groundHeight - (block+1)*self.width, self.width, self.width, fill=self.fill, border='white', opacity=80)
            self.triangleOb.draw(obstacleX, obstacleY, groundHeight - self.numBlocks*25)
        #draw upsidedown obstacles
        else:
            self.triangleOb.upsidedown = True
            self.triangleOb.groundHeight = self.groundHeight + (self.numBlocks-1)*25
            for block in range(len(self.blockObs)):
                drawRect(obstacleX, self.groundHeight + (block-1)*self.width, self.width, self.width, fill=self.fill, border='white', opacity=80)
            self.triangleOb.draw(obstacleX, obstacleY, self.groundHeight + (self.numBlocks-1)*25)

#build a list of sensitive points on perimeter of a triangle obstacle
def sensitivePoints(obstacle, obstacleX, obstacleY, groundHeight, obstacleNum, numPoints):
    dx = (obstacle.widthOfEach*0.5) / numPoints
    dy = (groundHeight - obstacleY) / numPoints
    obstacle.sensitivePoints = []
    #points along the left side
    for point in range(numPoints):
        obstacle.sensitivePoints += [(obstacleX + obstacleNum*obstacle.widthOfEach + dx*point, groundHeight - dy*point)]
    #points along the right side
    for point in range(numPoints + 1):
        obstacle.sensitivePoints += [(obstacleX + obstacleNum*obstacle.widthOfEach + obstacle.widthOfEach*0.5 + dx*point, obstacleY + dy*point)]


def sensitivePointsUpsidedown(obstacle, obstacleX, obstacleY, groundHeight, obstacleNum, numPoints):
    dx = (obstacle.widthOfEach*0.5) / numPoints
    dy = (obstacleY - groundHeight) / numPoints
    obstacle.sensitivePoints = []
    #points along the left side
    for point in range(numPoints):
        obstacle.sensitivePoints += [(obstacleX + obstacleNum*obstacle.widthOfEach + dx*point, groundHeight + dy*point)]
    #points along the right side
    for point in range(numPoints + 1):
        obstacle.sensitivePoints += [(obstacleX + obstacleNum*obstacle.widthOfEach + obstacle.widthOfEach*0.5 + dx*point, obstacleY - dy*point)]

class Booster:
    def __init__(self, initialX):
        self.x = initialX
        self.height = 5
        self.width = 25
        self.widthOfEach = 25
        self.groundHeight = 300

    def draw(self, obstacleX, obstacleY, groundHeight):
        drawRect(obstacleX, obstacleY, self.widthOfEach, self.height, fill = 'yellow')

    def boost(self, block):
        block.vy += 0.2

class Star:
    def __init__(self, initialX, fill):
        self.fill = 'gold'
        self.x = initialX
        self.height = 40
        self.width = 40
        self.groundHeight = 290
        self.seen = False
        
    def draw(self, obstacleX, obstacleY, groundHeight):
        self.groundHeight = groundHeight - 10
        drawStar(self.x + 20, self.groundHeight - 20, 20, 5, fill=self.fill,
                 roundness=25, opacity=80)


def redrawAll(app):
    #draw background pattern
    drawImage(patternIm, 0, 0, align='center', width=2*app.width, opacity=60)

    #draw features of welcome screen
    if app.welcomeScreen: 
        drawRect(0, 0, app.width, app.height, fill='white', opacity=60)
        drawLabel("112 Dash", 200, 130, bold=True, size=25)
        drawImage(playButtonIm, app.width//2 - 35, app.height//2 - 35, width=70, height=70)
        drawImage(settingsIm, app.width//2 + 60, app.height//2 - 20, width=50,height=50)
        drawImage(blockIm, app.width//2 - 105, app.height//2 - 20, width = 50, height=50)
        drawImage(crownIm, 325, 25, width=50, height=40)
        drawLabel("Pro tip: Hold down the space bar for best performance!", 200, 300, size=13)
        return
    
    #draw features of scores screen
    if app.scoresScreen:
        drawRect(0, 0, app.width, app.height, fill='powderBlue', opacity=60)
        drawLabel("All Time High Scores:", app.width//2, 100, size=17, bold=True)
        drawLabel(f'1. {app.highScore1}', app.width//2, 150, size=15, bold=True)
        drawLabel(f'2. {app.highScore2}', app.width//2, 170, size=15, bold=True)
        drawLabel(f'3. {app.highScore3}', app.width//2, 190, size=15, bold=True)
        drawLabel("Stars Collected:", app.width//2, 230, size=17, bold=True)
        drawStar(app.width//2 - 15, 260, 15, 5, fill='gold', roundness=25)
        drawLabel(f'{app.starCount}', app.width//2 + 20, 260, size=15, bold=True)
        drawBackButton(app)
        return
    
    #draw features of settings screen
    if app.settingsScreen:
        drawRect(0, 0, app.width, app.height, fill='powderBlue', opacity=60)
        drawLabel("Select difficulty level:", 200, 100, size=15, bold=True)
        drawRect(app.width//2 - 90, app.height//2 - 25, 50, 50, fill=app.easyColor, border='black')
        drawRect(app.width//2 - 30, app.height//2 - 25, 50, 50, fill=app.medColor, border='black')
        drawRect(app.width//2 + 30, app.height//2 - 25, 50, 50, fill=app.hardColor, border='black')
        drawLabel("Easy", app.width//2 - 65, app.height//2, size=12)
        drawLabel("Medium", app.width//2 - 5, app.height//2, size=12)
        drawLabel("Hard", app.width//2 + 55, app.height//2, size=12)
        drawBackButton(app)
        return
    
    #draw features of fill selection screen
    if app.blockScreen:
        drawRect(0, 0, app.width, app.height, fill='powderBlue', opacity=60)
        drawLabel("Select character skin:", 200, 100, size=15, bold=True)
        drawRect(app.width//2 - 90, app.height//2 - 25, 50, 50, fill='cyan', border=app.cyanBorder)
        drawRect(app.width//2 - 30, app.height//2 - 25, 50, 50, fill='pink', border=app.pinkBorder)
        drawRect(app.width//2 + 30, app.height//2 - 25, 50, 50, fill='green', border=app.greenBorder)
        drawRect(app.width//2 - 90, app.height//2 + 35, 50, 50, fill='lightCoral', border=app.coralBorder)
        if not app.starCount >= 10:
            drawImage(lockIm, app.width//2 - 75, app.height//2 + 50, width=20, height=20)
        drawRect(app.width//2 - 30, app.height//2 + 35, 50, 50, fill='cornflowerBlue', border=app.cornBorder)
        if not app.starCount >= 20:
            drawImage(lockIm, app.width//2 - 15, app.height//2 + 50, width=20, height=20)
        drawRect(app.width//2 + 30, app.height//2 + 35, 50, 50, fill='plum', border=app.plumBorder)
        if not app.starCount >= 30:
            drawImage(lockIm, app.width//2 + 45, app.height//2 + 50, width=20, height=20)
        drawBackButton(app)
        if app.starMessage != 0:
            starMessage(app, app.starMessage)
        return
    
    #draw background corresponding to current zone
    if app.switchZone:
        drawRect(0, 0, app.width, app.height, fill=app.bg, opacity = 60)
        drawImage(groundIm, 0, 0, width=app.width, height=50)
    elif app.flyZone:
        drawRect(0, 0, app.width, app.height, fill=app.bg, opacity = 60)
        drawImage(groundIm, 0, 0, width=app.width, height=25)
    else:
        drawRect(0, 0, app.width, app.height, fill='white', opacity=40)

    #draw background corresponding to current transition (if any)
    if app.transition and app.flyZone:
        transitionToFly(app)
    if app.transition and app.switchZone:
        transitionToSwitch(app)

    #draw normal background and features
    drawImage(groundIm, 0, 300, width=app.width)
    drawBackButton(app)

    #display score
    drawLabel(f'Score: {app.score}', 360, 40, size=12, bold=True)

    #show instructions breifly at start of first attempt
    if app.score < 600 and app.attempts == 1:
        drawLabel("Hold 'space' and 'up' to jump continuously!", 200, 100, size=13, bold=True)
        drawLabel('Press p to pause/unpause', app.width//2, 30, size=13)
        drawLabel('Press r to restart', app.width//2, 50, size=13)
    
    #show attempt number
    if app.score >= 600 and not app.gameOver:
        drawLabel(f'Attempt {app.attempts}', app.width//2, 75, size=17, bold=True)
    elif app.attempts > 1 and not app.gameOver:
        drawLabel(f'Attempt {app.attempts}', app.width//2, 75, size=17, bold=True)

    #display game over message when block crashes
    if app.gameOver:
        drawLabel("Press any key to restart", app.width//2, 150, size=14, bold=True)
        
    #draw character block
    app.characterBlock.draw(app.blockWidth, app.blockHeight)

    #draw flyer if block is flying
    if app.flyZone:
        app.characterBlock.drawFlyer()
        sprite = app.rocketdust[app.spriteCounter]
        drawImage(sprite, app.characterBlock.x - 35, app.characterBlock.y + 10, width=20, height=15)

    #draw obstacles currently on screen
    for obstacle in app.pastObstacles:
        if isinstance(obstacle, Booster):
            sprite = app.sparkles[app.spriteCounter]
            drawImage(sprite, obstacle.x, obstacle.groundHeight - 10, width=25, height=10)
            continue
        obstacle.draw(obstacle.x, obstacle.groundHeight - obstacle.height, app.groundHeight)
        
    for obstacle in app.currObstacles:
        if isinstance(obstacle, Booster):
            sprite = app.sparkles[app.spriteCounter]
            drawImage(sprite, obstacle.x, obstacle.groundHeight - 10, width=25, height=10)
            continue
        obstacle.draw(obstacle.x, obstacle.groundHeight - obstacle.height, app.groundHeight)

    #display new high score (if any)
    if app.newHigh:
            drawLabel(f'New high score! {app.highScore1}', 200, 100, size=20, bold=True)

#message displayed when user clicks a locked skin
def starMessage(app, num):
    drawLabel(f'You need {num} stars to unlock this skin!', app.width//2, 300, size=13, bold=True)

#draw back button
def drawBackButton(app):
    drawRect(20, 20, 40, 25, fill='lightgrey', border='black')
    drawLabel("BACK", 40, 32, fill='black', size=10, bold=True)

def distance(x0, x1, y0, y1):
    return ((x1-x0)**2+(y1-y0)**2)**0.5

#when block crashes, app is paused and high scores are updated if applicable
def gameOver(app):
    app.paused = True
    app.attempts += 1
    if app.score > app.highScore1:
        app.highScore3, app.highScore2, app.highScore1 = app.highScore2, app.highScore1, app.score
        app.newHigh = True
    elif app.score > app.highScore2:
        app.highScore3, app.highScore2 = app.highScore2, app.score
    elif app.score > app.highScore3:
        app.highScore3 = app.score
    app.gameOver = True

#handle a triangular collision
def hitsTriangle(app, triangle):
    for (x, y) in triangle.sensitivePoints:
        d = distance(x, app.characterBlock.cx, y, app.characterBlock.cy)
        if d <= app.sensitiveRadius + 1:
            gameOver(app)

#establish "ground" height depending on current obstacle
def establishGroundHeight(app):
    for obstacle in app.currObstacles:
        if isinstance(obstacle, Star):
            continue
        if obstacle.x < app.characterBlock.x < obstacle.x + obstacle.width:
            app.currGroundHeight = app.groundHeight - obstacle.height
            return obstacle
        else:
            app.currGroundHeight = app.groundHeight
            return None

#get new zone and initiate a transition     
def getZone(app):
    if app.transition:
        return
    if len(app.currObstacles) < 2:
        return
    
    app.currZoneEnd = random.randint(1500, 2000)
    
    if app.flyZone or app.switchZone:
        app.bg = 'pink'
        app.flyZone = False
        app.switchZone = False
        app.regularZone = True
        app.currZoneScore = 0
    elif random.randint(0,1) == 0:
        app.characterBlock.angle = 0
        app.bg = 'lightgreen'
        app.switchZone = True
        app.characterBlock.y = app.blockNorm
        app.currZoneScore = 0
    else:
        app.characterBlock.angle = 0
        app.bg = 'lightblue'
        app.flyZone = True
        app.currZoneScore = 0

#display an instruction splash screen for fly zone
def transitionToFly(app):
    drawRect(0, 0, app.width, app.height, fill='black', opacity=60)
    drawLabel("Hold the space bar and use the up arrow to fly!", 200, 200, fill='white', size=15, bold=True)
    if len(app.currObstacles) > 0:
        app.currObstacles.pop(0)

#display an instruction splash screen for switch zone
def transitionToSwitch(app):
    # drawRect(0, 0, app.width, app.height, fill=app.bg, opacity=60)
    drawImage(groundIm, 0, 0, width=app.width, height=50)
    drawLabel("Use the up and down arrows to switch!", 200, 200, fill='black', size=15, bold=True)
    if len(app.currObstacles) > 0:
        app.currObstacles.pop(0)

#clear game of obstacles associated with past zone before next zone begins
def clearForTransition(app):
    if len(app.currObstacles) > 0:
        app.currObstacles.pop(0)

#randomly generate an obstacle and set its initial position
def getRandomObstacle(app, initialX):
    if app.switchZone:
        rand = random.choice([1, 2])
    elif app.flyZone:
        rand = 4
    else:
        rand = random.randint(0,3)
    if rand == 0:
        return BlockObstacle(initialX, app.bg)
    elif rand == 1:
        return TriangleObstacle(initialX, app.bg)
    elif rand == 2:
        return BigTriangleObstacle(initialX, app.bg)
    elif rand == 3:
        return BlockAndTriangleObstacle(initialX, app.bg)
    elif rand == 4:
        return FlyingObstacle(initialX, app.bg)

#ensure obstacles are far enough apart
def giveExtraSpace(lastObstacle, newObstacle, minSeparation):
    if newObstacle.x - (lastObstacle.x + lastObstacle.width) < minSeparation:
            newObstacle.x = lastObstacle.x + lastObstacle.width + minSeparation

#keep list of obstacles currently on screen
#update features of obstacles depending on circumtances
def updateObstacleLists(app):
    if len(app.currObstacles) == 0:
        app.currObstacles.append(getRandomObstacle(app, app.width + 200))
        return
    
    lastObstacle = app.currObstacles[-1]

    #remove obstacles that are off of the screen
    for obstacle in app.pastObstacles:
        if obstacle.x < -150:
            app.pastObstacles.remove(obstacle)

    #if block passes an obstacle, remove it and add it to past obstacles
    if app.currObstacles[0].x + app.currObstacles[0].width < app.characterBlock.x:
        app.pastObstacles.append(app.currObstacles.pop(0)) 
    
    #if there is enough space, add a new obstacle
    if lastObstacle.x < app.width:
        #get new starting x
        if (len(app.currObstacles) > 1) and isinstance(app.currObstacles[-2], Booster):
            newStart = app.width + random.randint(275,300)
        else:
            newStart = app.width + random.randint(250, 300)
        
        newObstacle = getRandomObstacle(app, newStart)

        #limit difficulty of obstacles in easy mode
        if isinstance(newObstacle, TriangleObstacle) and app.difficulty == 1:
            if newObstacle.numTriangles > 3:
                newObstacle.numTriangles = 3

        #give enough space to pass block and triangle obstacle
        if isinstance(newObstacle, BlockAndTriangleObstacle):
            giveExtraSpace(lastObstacle, newObstacle, 300)
        
        #give enough space to pass obstacle following block and triangle obstacle
        if isinstance(lastObstacle, BlockAndTriangleObstacle):
            giveExtraSpace(lastObstacle, newObstacle, 250)

        #give enough space to pass obstacle following block obstacle
        if isinstance(lastObstacle, BlockObstacle):
            giveExtraSpace(lastObstacle, newObstacle, 100)

        #sometimes, add a booster in front of triangle obstacles
        if (isinstance(newObstacle, TriangleObstacle) and random.randint(0,1)==0 
            and not app.switchZone):
            app.currObstacles.append(Booster(newObstacle.x - 25))

        #turn some triangle obstacles upside down during switch zone
        if (isinstance(newObstacle, TriangleObstacle) and app.switchZone and (random.randint(0,1) == 0)):
            newObstacle.upsidedown = True
            newObstacle.groundHeight = 50

        if (isinstance(newObstacle, BigTriangleObstacle) and app.switchZone and (random.randint(0,1) == 0)):
            newObstacle.upsidedown = True
            newObstacle.groundHeight = 50

        #turn some flying obstacles upside down during fly zone
        if isinstance(newObstacle, FlyingObstacle) and (random.randint(0,1) == 0):
            newObstacle.upsidedown = True
            newObstacle.groundHeight = 50

        #make triangles bigger during switch zone
        if isinstance(newObstacle, BigTriangleObstacle) and app.switchZone:
            newObstacle.height = random.randint(60, 75)

        if isinstance(newObstacle, TriangleObstacle) and app.switchZone:
            newObstacle.height = random.randint(40, 50)

        #make obstacles closer together during switch and fly in medium and hard mode
        if (app.switchZone or app.flyZone) and app.difficulty == 1.02:
            newObstacle.x -= 75
        elif (app.switchZone or app.flyZone) and app.difficulty == 1.05:
            newObstacle.x -= 100

        #add stars for collection randomly (and always in switchZone)
        if (random.randint(0,3) == 0 and not app.flyZone) or app.switchZone:
            app.currObstacles.append(Star(newObstacle.x + newObstacle.width + 75, 'gold'))

        app.currObstacles.append(newObstacle)

def onStep(app):
    if not app.paused:
        takeStep(app)

def takeStep(app):
    app.score += 1

    #track duration of each zone
    app.currZoneScore += 1

    #get sparkle frame
    if app.score%10 == 0:
        app.spriteCounter = (1 + app.spriteCounter) % len(app.sparkles)

    updateObstacleLists(app)

    #move all obstacles across screen
    for obstacle in app.pastObstacles:
        obstacle.x -= 1*app.difficulty

    for obstacle in app.currObstacles:
        obstacle.x -= 1*app.difficulty

    #handle interactions in switch zone
    if app.switchZone:
        #establish current "ground" height
        #if block is over an obstacle, handle a crash
        if establishGroundHeight(app) != None:
            obstacle = establishGroundHeight(app)
            if isinstance(obstacle, TriangleObstacle) or isinstance(obstacle, BigTriangleObstacle) or isinstance(obstacle, BlockAndTriangleObstacle):
                hitsTriangle(app, obstacle)

        #display instructions or initiate transition before zone begins
        if (app.currZoneScore < 400) and not app.switchDirections:
            app.bg = 'lightgreen'
            app.transition = True
        elif app.currZoneScore < 150:
            app.bg = 'lightgreen'
            clearForTransition(app)
        else:
            app.bg = 'lightgreen'
            app.switchDirections = True
            app.transition = False

        #track if block is "up" or "down"
        if not app.switching:
            if app.characterBlock.y < 150:
                app.down = True
                app.up = False
                app.switchGroundHeight = app.groundHeight
            else:
                app.up = True
                app.down = False
                app.switchGroundHeight = app.ceil

        #initiate switch motion
        if app.switching:
            if not app.characterBlock.switch(app.dt, app.switchGroundHeight, app.up):
                app.switching = False

        #crash if character block hits the side of obstacle
        if len(app.currObstacles) == 0:
            return
        
        dist = distance(app.characterBlock.x + app.blockWidth*0.5, app.currObstacles[0].x,
                        app.characterBlock.y + app.blockWidth*0.5, app.currObstacles[0].groundHeight)
        
        if dist <= app.sensitiveRadius:
            if isinstance(app.currObstacles[0], Booster):
                app.currObstacles[0].boost(app.characterBlock)
                app.jumping = True
            elif isinstance(app.currObstacles[0], Star):
                app.currObstacles[0].fill = 'orange'
                if app.currObstacles[0].seen == False:
                    app.starCount += 1
                app.currObstacles[0].seen = True
            else:
                gameOver(app)
                return

        #switch zones after short time intervals
        if app.currZoneScore > app.currZoneEnd:
            getZone(app)

    #handle interactions in fly zone
    elif app.flyZone:
        #establish current "ground" height
        #if block is over an obstacle, handle a crash
        if establishGroundHeight(app) != None:
            obstacle = establishGroundHeight(app)
            if (isinstance(obstacle, TriangleObstacle) or isinstance(obstacle, BigTriangleObstacle) 
                or isinstance(obstacle, BlockAndTriangleObstacle)):
                hitsTriangle(app, obstacle)
        
        #display instructions or initiate transition before zone begins
        if (app.currZoneScore < 400) and not app.flyDirections:
            app.bg = 'lightblue'
            app.transition = True
        elif app.currZoneScore < 150:
            app.bg = 'lightblue'
            clearForTransition(app)
        else:
            app.bg = 'lightblue'
            app.flyDirections = True
            app.transition = False

        #block flies
        app.characterBlock.fly(app.dt, app.groundHeight, 25, app.holding)
        
        #crash if character block hits the side of obstacle
        if len(app.currObstacles) == 0:
            return
        
        if isinstance(app.currObstacles[0], FlyingObstacle):
            dy = app.currObstacles[0].height / 20
            if app.currObstacles[0].upsidedown:
                for point in range(20):
                    dist = distance(app.characterBlock.x + app.blockWidth*0.5, 
                                    app.currObstacles[0].x, app.characterBlock.y + app.blockWidth, 
                                    app.currObstacles[0].groundHeight + point*dy)
                
                    if dist <= app.sensitiveRadius:
                        gameOver(app)
                        return
                
            else:
                for point in range(10):
                    dist = distance(app.characterBlock.x + app.blockWidth*0.5, app.currObstacles[0].x,
                                    app.characterBlock.y + app.blockWidth*0.5, app.groundHeight - point*dy)

                    if dist <= app.sensitiveRadius:
                        gameOver(app)
                        return
        else:
            return
                
        #switch zones after short time intervals
        if app.currZoneScore > app.currZoneEnd:
            getZone(app)

    #handle interactions in regular zone
    elif app.regularZone:
        #establish current "ground" height
        #if block is over an obstacle, handle a crash
        if establishGroundHeight(app) != None:
            obstacle = establishGroundHeight(app)
            if isinstance(obstacle, TriangleObstacle) or isinstance(obstacle, BigTriangleObstacle) or isinstance(obstacle, BlockAndTriangleObstacle):
                hitsTriangle(app, obstacle)

        #initiate transition before zone begins
        if app.currZoneScore < 150:
            app.bg = 'lavenderBlush'
            clearForTransition(app)

        #block falls to lowest possible height
        if ((app.characterBlock.y + app.blockWidth < app.currGroundHeight) and 
            (not app.jumping)):
            app.characterBlock.fall(app.dt, app.currGroundHeight)
    
        #block jumps
        if app.jumping:
            if not app.characterBlock.jump(app.dt, app.currGroundHeight):
                if app.holding:
                    return
                app.jumping = False


        #crash if character block hits the side of obstacle
        if len(app.currObstacles) == 0:
            return
        dist = distance(app.characterBlock.x + app.blockWidth*0.5, app.currObstacles[0].x,
                        app.characterBlock.y + app.blockWidth*0.5, app.blockNorm)

        if dist <= app.sensitiveRadius:
            if isinstance(app.currObstacles[0], Booster):
                app.currObstacles[0].boost(app.characterBlock)
                app.jumping = True
            elif isinstance(app.currObstacles[0], Star):
                app.currObstacles[0].fill = 'orange'
                if app.currObstacles[0].seen == False:
                    app.starCount += 1
                app.currObstacles[0].seen = True
            else:
                gameOver(app)
                return
        
        #switch zones after short time intervals
        if app.currZoneScore > app.currZoneEnd:
            getZone(app)

    
def onMousePress(app, MouseX, MouseY):
    #handle back button press
    if not app.welcomeScreen and ((20 < MouseX < 60) and (20 < MouseY < 45)):
            app.settingsScreen = False
            app.blockScreen = False
            app.scoresScreen = False
            app.paused = True
            app.welcomeScreen = True

    #handle button presses on welcome screen
    if app.welcomeScreen:
        if ((app.width//2 - 35 < MouseX < app.width//2 + 35) and 
            (app.height//2 - 35 < MouseY < app.height//2 + 35)):
            app.welcomeScreen = False
            app.paused = False
        elif ((app.width//2 - 105 < MouseX < app.width//2 - 65) and
            (app.height//2 - 20 < MouseY < app.height//2 + 20)):
            app.welcomeScreen = False
            app.blockScreen = True
        elif ((app.width//2 + 60 < MouseX < app.width//2 + 110) and 
            (app.height//2 - 20 < MouseY < app.height//2 + 20)):
            app.welcomeScreen = False
            app.settingsScreen = True
        elif (325 < MouseX < 375) and (25 < MouseY < 65):
            app.welcomeScreen = False
            app.scoresScreen = True

    #let user select difficulty and turn chosen difficulty orange
    elif app.settingsScreen:
        if ((app.width//2 - 90 < MouseX < app.width//2 - 40) and 
            (app.height//2 - 25 < MouseY < app.height//2 + 50)):
            app.difficulty = 1
            app.easyColor = 'orange'
            app.medColor = 'pink'
            app.hardColor = 'pink'
        elif ((app.width//2 - 30 < MouseX < app.width//2 + 20) and 
              (app.height//2 - 25 < MouseY < app.height//2 + 50)):
            app.difficulty = 1.02
            app.easyColor = 'pink'
            app.medColor = 'orange'
            app.hardColor = 'pink'
        elif ((app.width//2 + 30 < MouseX < app.width//2 + 80) and 
              (app.height//2 - 25 < MouseY < app.height//2 + 50)):
            app.difficulty = 1.05
            app.easyColor = 'pink'
            app.medColor = 'pink'
            app.hardColor = 'orange'

    #let use select block fill and give only selected block a border
    elif app.blockScreen:
        if ((app.width//2 - 90 < MouseX < app.width//2 - 40) and 
            (app.height//2 - 25 < MouseY < app.height//2 + 50)):
            app.starMessage = 0
            app.cyanBorder = 'black'
            app.pinkBorder = None
            app.greenBorder = None
            app.coralBorder = None
            app.cornBorder = None
            app.plumBorder = None
            app.characterBlock.fill = 'cyan'
            app.blockFill = 'cyan'
        elif ((app.width//2 - 30 < MouseX < app.width//2 + 20) and
               (app.height//2 - 25 < MouseY < app.height//2 + 50)):
            app.starMessage = 0
            app.cyanBorder = None
            app.pinkBorder = 'black'
            app.greenBorder = None
            app.coralBorder = None
            app.cornBorder = None
            app.plumBorder = None
            app.characterBlock.fill = 'pink'
            app.blockFill = 'pink'
        elif ((app.width//2 + 30 < MouseX < app.width//2 + 80) and
              (app.height//2 - 25 < MouseY < app.height//2 + 50)):
            app.starMessage = 0
            app.cyanBorder = None
            app.pinkBorder = None
            app.greenBorder = 'black'
            app.coralBorder = None
            app.cornBorder = None
            app.plumBorder = None
            app.characterBlock.fill = 'green'
            app.blockFill = 'green'
        elif ((app.width//2 - 90 < MouseX < app.width//2 - 40) and 
            (app.height//2 + 35 < MouseY < app.height//2 + 85)):
            #display a message instead of changing if the user has not collected 10 stars yet
            if app.starCount < 10:
                app.starMessage = 10
                return
            app.cyanBorder = None
            app.pinkBorder = None
            app.greenBorder = None
            app.coralBorder = 'black'
            app.cornBorder = None
            app.plumBorder = None
            app.characterBlock.fill = 'lightCoral'
            app.blockFill = 'lightCoral'
        elif ((app.width//2 - 30 < MouseX < app.width//2 + 20) and
               (app.height//2 + 35 < MouseY < app.height//2 + 85)):
            #display a message instead of changing if the user has not collected 20 stars yet
            if app.starCount < 20:
                app.starMessage = 20
                return
            app.cyanBorder = None
            app.pinkBorder = None
            app.greenBorder = None
            app.coralBorder = None
            app.cornBorder = 'black'
            app.plumBorder = None
            app.characterBlock.fill = 'cornflowerBlue'
            app.blockFill = 'cornflowerBlue'
        elif ((app.width//2 + 30 < MouseX < app.width//2 + 80) and
              (app.height//2 + 35 < MouseY < app.height//2 + 85)):
            #display a message instead of changing if the user has not collected 30 stars yet
            if app.starCount < 30:
                app.starMessage = 30
                return
            app.cyanBorder = None
            app.pinkBorder = None
            app.greenBorder = None
            app.coralBorder = None
            app.cornBorder = None
            app.plumBorder = 'black'
            app.characterBlock.fill = 'plum'
            app.blockFill = 'plum'


def onKeyPress(app, key):
    #no key presses matter unless game is in play
    if app.welcomeScreen or app.blockScreen or app.settingsScreen:
        return
    
    if key == 'p':
        app.paused = not app.paused

    if key == 'r':
        restartApp(app, app.blockFill, app.difficulty, app.switchDirections, app.flyDirections,
                   app.easyColor, app.medColor, app.hardColor, app.cyanBorder, app.pinkBorder,
                   app.greenBorder, app.coralBorder, app.cornBorder, app.plumBorder, app.highScore1,
                   app.highScore2, app.highScore3, app.starCount, app.attempts)
        app.welcomeScreen = False
        app.paused = False
        app.attempts += 1
    
    if app.switchZone:
        if key == 'up' or key == 'space':
            if app.down:
                if app.characterBlock.y < app.currGroundHeight - app.characterBlock.width:
                    return
            app.switching = True
        if key == 'down' or key == 'space':
            if app.up:
                if app.characterBlock.y > app.ceil:
                    return
            app.switching = True
    else:
        if key == 'up' or key == 'space':
            if app.characterBlock.y < app.currGroundHeight - app.characterBlock.width:
                return
            app.jumping = True

    if app.paused and key.isalpha() and key != 'p' and key != 'r':
        restartApp(app, app.blockFill, app.difficulty, app.switchDirections, app.flyDirections,
                   app.easyColor, app.medColor, app.hardColor, app.cyanBorder, app.pinkBorder,
                   app.greenBorder, app.coralBorder, app.cornBorder, app.plumBorder, app.highScore1,
                   app.highScore2, app.highScore3, app.starCount, app.attempts)
        app.welcomeScreen = False
        app.paused = False

def onKeyHold(app, keys):
    if keys == ['space', 'up'] or keys == ['up', 'space']:
        app.holding = True

def onKeyRelease(app, key):
    if key == 'space':
        app.holding = False
    if key == 'up':
        app.holding = False

def main():
    runApp(width=400, height=400)

main()