class Maze {
    constructor(stage, posX, posY, W, H, queue, maze, turnList) {
        this.stage = stage;
        this.maze = maze;
        this.turnList = turnList;
        this.posX = posX;
        this.posY = posY;
        this.maze_height = this.maze.length;
        this.maze_width = this.maze[0].length;
        /*this.mem = new Array(this.maze.height);
        for(var i = 0; i < this.maze_height; i++) {
            this.mem[i] = new Array(this.maze_width);
            this.mem[i].fill(0);
        }*/

        this.shape = new createjs.Shape();
        this.grid_size_x = parseInt(W / this.maze_width);
        this.grid_size_y = parseInt(H / this.maze_height);
        console.log(this.grid_size_x);
        console.log(this.grid_size_y);

        this.icon_list = [];
        for(var i = 0; i < queue.getItems().length ;i++) {
            var bmp = new createjs.Bitmap(queue.getResult(i));
            bmp.scaleX = this.grid_size_x / bmp.getBounds().width;
            bmp.scaleY = this.grid_size_y / bmp.getBounds().height;
            this.icon_list.push(bmp);
        }
        this.old_bmp = this.icon_list[0];
    }

    getGridSize() {
        return [this.grid_size_x, this.grid_size_y];
    }

    drawMaze() {
        for(var y = 0; y < this.maze_height; y++){
            for(var x = 0; x < this.maze_width; x++) {
                if(this.maze[y][x] == 0) {
                    this.shape.graphics.beginFill("white");
                }
                else if(this.maze[y][x] == 1) {
                    this.shape.graphics.beginFill("gray");
                }
                else if(this.maze[y][x] == 2) {
                    this.shape.graphics.beginFill("green");
                }
                else if(this.maze[y][x] == 3) {
                    this.shape.graphics.beginFill("red");
                }
                else {
                    this.shape.graphics.beginFill("white");
                }
                this.shape.graphics.drawRect(this.posX + x*this.grid_size_x, this.posY + y*this.grid_size_y, this.grid_size_x, this.grid_size_y);
            }
        }
        return this.shape;
    }

    drawPlayer(turn, step) {
        var action = this.turnList[turn][step][1];
        var pos_x = this.turnList[turn][step][2];
        var pos_y = this.turnList[turn][step][3];
        var bmp = this.icon_list[action];

        if(this.old_bmp != null) {
            this.stage.removeChild(this.old_bmp);
        }

        bmp.x = this.posX + this.grid_size_x * pos_x;
        bmp.y = this.posY + this.grid_size_y * pos_y;
        this.old_bmp = bmp;
        return bmp;
    }
}