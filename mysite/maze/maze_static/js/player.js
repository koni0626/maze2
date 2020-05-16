    class Player {
        constructor(grid_size) {
            this.turn_list = {{turn_list}};
            this.turn = 0;
            this.step = 0;
            this.old_bmp = null;
            this.grid_size_x = grid_size[0];
            this.grid_size_y = grid_size[1];
            this.icon_list = [];

            for(var i = 0; i < queue.getItems().length ;i++) {
                var bmp = new createjs.Bitmap(queue.getResult(i));
                bmp.scaleX = this.grid_size_x / bmp.getBounds().width;
                bmp.scaleY = this.grid_size_y / bmp.getBounds().height;
                this.icon_list.push(bmp);
            }
            this.old_bmp = this.icon_list[0];
        }


        drawIcon(){
            var turn_num = 0;
            var step_num = 0;
            try{
                step_num = this.turn_list[this.turn].length;
                if(step_num == 0) {
                    return null;
                }
            }
            catch(e) {
                //ターン数オーバー
                return null;
            }

            var action = this.turn_list[this.turn][this.step][1];
            var pos_x = this.turn_list[this.turn][this.step][2];
            var pos_y = this.turn_list[this.turn][this.step][3];
            this.step += 1;
            if(this.step >= step_num) {
                this.turn += 1;
                this.step = 0;
            }

            var bmp = this.icon_list[action];

            if(this.old_bmp != null) {
                stage.removeChild(this.old_bmp);
            }

            bmp.x = this.grid_size_x * pos_x;
            bmp.y = this.grid_size_y * pos_y;
            this.old_bmp = bmp;

            return bmp;
        }
    }