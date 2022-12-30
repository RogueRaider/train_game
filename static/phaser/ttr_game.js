

//1 map depicting the United States
//240 Colored Train Cars (48 each in Blue, Red, Green, Yellow & Black)
//96 Train Cards (12 each in Red, Orange, Yellow, Green, Blue, Purple, Black & White)
//14 Locomotive Wild Cards (Multicolored)
//1 Scoring Summary Card
//30 Destination Ticket Cards
//1 Longest Route Bonus Card
//2 Days of Wonder Advertisement Cards
//5 Wooden Scoring Markers (1 each in Blue, Red, Green, Yellow & Black)

class Track extends Phaser.GameObjects.Rectangle {
    constructor(scene, x, y, width, height, color, angle, routeName) {
        super(scene, x, y, width, height);
        this.baseColor = color;
        this.setAngle(angle);
        this.setStrokeStyle(3, color);
        this.setInteractive();
        this.routeName = routeName;

        // on click, highlight black
        this.on('pointerdown', function () {
            for (var track of this.parentContainer.list) {
                if (track.routeName == this.routeName) {
                    track.setStrokeStyle(4, black); // black
                }
            }
        })
        // on unclick, return to original color
        this.on('pointerup', function () {
            for (var track of this.parentContainer.list) {
                if (track.routeName == this.routeName) {
                    track.setStrokeStyle(3, this.baseColor); // black
                }
            }
        })
    }
    testFunction() {
        console.log("test function")
    }
}

class TrainCard extends Phaser.GameObjects.Image {
    constructor(scene, x, y, sprite) {
        super(scene, x, y, sprite);
        scene.add.existing(this);
        this.setInteractive();
        this.setScale(0.2, 0.2);
    }

}

class Player {
    constructor(displayName) {
    this.displayName = displayName;
    this.cards = null;
    }
}




class PlacementTrack {
    constructor(scene) {
        this.render = (x, y, width, height, color, angle) => {
            let track = scene.add.rectangle(x, y, width, height, color).setAngle(angle).setInteractive();
            scene.input.setDraggable(track);
            return track;
        };
    }
}



class Zone {
    constructor(scene) {
        this.renderZone = () => {
            let dropZone = scene.add.zone(700, 375, 900, 250).setRectangleDropZone(900, 250);
            dropZone.setData({ cards: 0 });
            return dropZone;
        };
        this.renderOutline = (dropZone) => {
            let dropZoneOutline = scene.add.graphics();
            dropZoneOutline.lineStyle(4, 0xff69b4);
            dropZoneOutline.strokeRect(dropZone.x - dropZone.input.hitArea.width / 2, dropZone.y - dropZone.input.hitArea.height / 2, dropZone.input.hitArea.width, dropZone.input.hitArea.height)
        }
    }
}



class Example extends Phaser.Scene
{
    constructor ()
    {
        super();
    }

    preload ()
    {
        this.load.image('ttrBoard', 'static/images/train_game_america.jpg');
        this.load.image('trainCardYellow', 'static/phaser/assets/TrainCardYellow.png');
        this.load.image('trainCardBlue', 'static/phaser/assets/TrainCardBlue.png');
        this.load.image('trainCardGreen', 'static/phaser/assets/TrainCardGreen.png');
    }

    create ()
    {

        // load board image
        this.add.image(425, 315, 'ttrBoard').setScale(0.85, 0.85);


        // sample track for testing
        let t0 = new PlacementTrack(this).render(84, 544, 30, 10, 0xff6699, 15);


        // create track pieces
        var trackList = [];
        for (const track of trackData) {
            trackList.push(
                new Track(this, track.x, track.y, track.length, track.height, track.color, track.angle, track.routeName)
            );
        }

        var trackContainer = this.add.container(0, 0, trackList);

        // create dummy cards
        var c1 = new TrainCard(this, 925, 100, 'trainCardYellow');
        c1.setAngle(270);
        this.input.setDraggable(c1);
        var c2 = new TrainCard(this, 925, 200, 'trainCardBlue');
        c2.setAngle(270);
        this.input.setDraggable(c2);

        //Set up dummy player
        var p1 = new Player('Dummy1');
        console.log(p1);


        //Player HUD
        this.make.text({
            x: 20,
            y: 590,
            text: 'Player: ' + p1.displayName,
            style: {
                fontSize: '12px',
                fontFamily: 'Arial',
                color: '#ffffff',
            }
        });
//        var playerHUD =



		let self = this;





//		this.dealText.on('pointerdown', function () {
//            self.dealCards();
//        })



        this.input.on('drag', function (pointer, gameObject, dragX, dragY) {
            gameObject.x = dragX;
            gameObject.y = dragY;
        })

        this.input.on('dragstart', function (pointer, gameObject) {
            self.children.bringToTop(gameObject);
        })

        this.input.on('dragend', function (pointer, gameObject, dropped) {
            if (!dropped) {
//                gameObject.x = gameObject.input.dragStartX;
//                gameObject.y = gameObject.input.dragStartY;
                console.log('x: ' + gameObject.x)
                console.log('y: ' + gameObject.y)
            }
        })

        this.input.on('drop', function (pointer, gameObject, dropZone) {
            dropZone.data.values.cards++;
            gameObject.x = (dropZone.x - 350) + (dropZone.data.values.cards * 50);
            gameObject.y = dropZone.y;
//            gameObject.disableInteractive();
        })

    }

    update ()
    {

    }
}




var config = {
    type: Phaser.AUTO,
    parent: 'phaser-canvas',
    pixelArt: true,
    width: 1000,
    height: 690,
    scene: [ Example ]
};

const game = new Phaser.Game(config);

