
<template>
  <div>
    <body>
      <p>score: {{ score }}</p>
      <p>combo: {{ combo }}</p>
      <canvas id="snakeboardAI" width="300" height="300"></canvas>
    </body>
    <button v-on:click="SnakeStart()">시작</button>
  </div>
</template>


<script>
import axios from "axios";
import { AI } from "./AI.js";

export default {
  name: "SnakeGameAI",
  data() {
    return {
      testbool: null,
      inputs: [],
      outputs: [],
      outputs2: [],

      tempdir1: -2,
      tempdir2: -2,

      life: 3,
      speed: 50,
      rank: -1,

      DIRECTIONS: [
        [0, -1],
        [1, 0],
        [0, 1],
        [-1, 0],
      ],
      // UDLR

      direction: 0,

      board_border: "black",
      board_background: "black",
      snake_col: "red",
      snake_border: "red",
      snake: [
        { x: 150, y: 260 },
        { x: 150, y: 270 },
        { x: 150, y: 280 },
        { x: 150, y: 290 },
      ],
      score: 0,
      combo: 0,
      // True if changing direction
      changing_direction: false,
      // Horizontal velocity
      food_x: -100,
      food_y: -100,
      dx: 0,
      // Vertical velocity
      dy: -10,
      // Get the canvas element
      snakeboard: "test",
      snakeboard_ctx: "test",
    };
  },
  methods: {
    Main() {
      if (this.life <= 0) {
        return;
      }

      // if (!this.Step(this.direction)) {
      //   console.log("collapsed");
      // }

      // if (this.Has_game_ended()) {
      //   console.log("has ended");
      //   this.ResetTile();
      //   clearInterval(this.testbool);
      // }

      // console.log(this.dx, this.dy);

      this.changing_direction = false;
      setTimeout(() => {
        if (this.Has_game_ended()) {
          console.log("has ended");
          this.ResetTile();
        }
        this.Clear_board();
        this.DrawFood();
        this.Move_Snake();
        this.DrawSnake();
        this.GetGenes();
        this.direction = this.SetOutPuts(this.outputs2);
        // console.log(this.inputs, this.outputs, this.outputs2, this.direction);
        this.SetWay(this.direction);
        // Repeat
        this.Main();
      }, this.speed);

      // this.testbool = setInterval(() => {
      //   // if (this.life <= 0) {
      //   //   clearInterval(this.testbool);
      //   //   return;
      //   // }
      //   this.Clear_board();
      //   this.DrawFood();
      //   this.Move_Snake();
      //   this.DrawSnake();

      //   this.GetGenes();

      //   this.direction = this.SetOutPuts(this.outputs2);
      //   // console.log(this.inputs, this.outputs, this.outputs2, this.direction);
      //   this.SetWay(this.direction);
      //   // Repeat
      //   // this.Main();
      //   if (this.Has_game_ended()) {
      //     console.log("has ended");
      //     this.ResetTile();
      //     // clearInterval(this.testbool);
      //   }
      // }, this.speed);
    },

    ResetTile() {
      this.snake = [
        { x: 150, y: 260 },
        { x: 150, y: 270 },
        { x: 150, y: 280 },
        { x: 150, y: 290 },
      ];
      this.dx = 0;
      this.dy = -10;
      this.Gen_Food();
    },

    SetWay(dir) {
      this.dx = this.DIRECTIONS[dir][0] * 10;
      this.dy = this.DIRECTIONS[dir][1] * 10;
    },

    GetGenes() {
      console.log("getinputs");
      this.inputs = this.GetInputs();
      this.outputs = this.Forward(this.inputs);
      // console.log(this.outputs);
      this.outputs2 = this.ArgMax(this.outputs);
    },

    SetOutPuts(num) {
      var resnum = num;
      // console.log(resnum);
      if (num == 1) {
        resnum = (this.direction + 3) % 4;
        // console.log(resnum);
      }
      if (num == 2) {
        resnum = (this.direction + 1) % 4;
        // console.log(resnum);
      }
      // this.direction = resnum;
      // console.log(resnum);
      return resnum;
    },

    // draw a border around the canvas
    Clear_board() {
      //  Select the colour to fill the drawing
      this.snakeboard_ctx.fillStyle = this.board_background;
      //  Select the colour for the border of the canvas
      this.snakeboard_ctx.strokestyle = this.board_border;
      // Draw a "filled" rectangle to cover the entire canvas
      this.snakeboard_ctx.fillRect(
        0,
        0,
        this.snakeboard.width,
        this.snakeboard.height
      );
      // Draw a "border" around the entire canvas
      this.snakeboard_ctx.strokeRect(
        0,
        0,
        this.snakeboard.width,
        this.snakeboard.height
      );
      return {};
    },

    // Draw the snake on the canvas
    DrawSnake() {
      // Draw each part
      this.snake.forEach((snakePart) => {
        // Set the colour of the snake part
        this.snakeboard_ctx.fillStyle = this.snake_col;
        // Set the border colour of the snake part
        this.snakeboard_ctx.strokestyle = this.snake_border;
        // Draw a "filled" rectangle to represent the snake part at the coordinates
        // the part is located
        this.snakeboard_ctx.fillRect(snakePart.x, snakePart.y, 10, 10);
        // Draw a border around the snake part
        this.snakeboard_ctx.strokeRect(snakePart.x, snakePart.y, 10, 10);
      });
    },

    DrawFood() {
      this.snakeboard_ctx.fillStyle = "lightgreen";
      this.snakeboard_ctx.strokestyle = "darkgreen";
      this.snakeboard_ctx.fillRect(this.food_x, this.food_y, 10, 10);
      this.snakeboard_ctx.strokeRect(this.food_x, this.food_y, 10, 10);
    },

    Has_game_ended() {
      console.log("step");
      for (let i = 4; i < this.snake.length; i++) {
        if (
          this.snake[i].x === this.snake[0].x &&
          this.snake[i].y === this.snake[0].y
        )
          return true;
      }
      const hitLeftWall = this.snake[0].x < 0;
      const hitRightWall = this.snake[0].x > this.snakeboard.width - 10;
      const hitToptWall = this.snake[0].y < 0;
      const hitBottomWall = this.snake[0].y > this.snakeboard.height - 10;
      if (
        (hitLeftWall || hitRightWall || hitToptWall || hitBottomWall) == true
      ) {
        this.combo = 0;
        this.life -= 1;
      }
      return hitLeftWall || hitRightWall || hitToptWall || hitBottomWall;
    },

    Random_food(min, max) {
      return Math.round((Math.random() * (max - min) + min) / 10) * 10;
    },

    Gen_Food() {
      // Generate a random number the food x-coordinate

      this.food_x = this.Random_food(0, this.snakeboard.width - 10);
      // Generate a random number for the food y-coordinate
      this.food_y = this.Random_food(0, this.snakeboard.height - 10);
      // if the new food location is where the snake currently is, generate a new food location

      this.snake.forEach((part) => {
        const has_eaten = part.x == this.food_x && part.y == this.food_y;
        if (has_eaten) this.Gen_Food();
      });
    },

    Relu(x) {
      // console.log(x[0].length);
      var res = [];
      var xx = [];
      var xxx = 0;
      for (var i = 0; i < x[0].length; i++) {
        xxx = x[0][i] * (x[0][i] >= 0);
        // console.log(x[0][i]);
        // console.log(xxx);
        xx.push(xxx);
      }
      res.push(xx);
      return res;
    },

    SoftMax(x) {
      // console.log(x[0]);
      var res = [];
      var xx = [];
      var xxx = 0;
      var exptmp = 0;
      for (var z = 0; z < x[0].length; z++) {
        // console.log(x[0][z]);
        var expfrag = Math.exp(x[0][z]);
        exptmp += expfrag;
      }
      // console.log(exptmp);
      for (var i = 0; i < x[0].length; i++) {
        xxx = Math.exp(x[0][i]) / exptmp;
        xx.push(xxx);
        // console.log(xxx);
      }
      res.push(xx);
      return res;
    },

    MatSum(a) {
      var l = a[0].length;
      var arr1 = Array(l);

      for (var b = 0; b < l; b++) {
        arr1[b] = 0;
      }
      var sol = Array(1);
      sol[0] = arr1;
      // var sol = Array(l);
      // console.log(sol);
      for (var v = 0; v < a.length; v++) {
        // console.log(a[v]);
        for (var c = 0; c < l; c++) {
          // console.log(sol);
          // console.log(a[v][c]);
          // console.log(a[v][c] + 1);
          // console.log(c);
          sol[0][c] += a[v][c];
        }
      }
      // console.log(sol);
      return a;
    },

    Forward(inputs) {
      // console.log(inputs);
      var net1 = this.MatMul(inputs, AI.D3.N3.w1);
      // console.log(net1);
      var net11 = this.Relu(net1);
      //here
      // console.log(net11);

      // here
      var net2 = this.MatMul(net11, AI.D3.N3.w2);
      // console.log(net2);
      var net22 = this.Relu(net2);
      // console.log(net22);

      var net3 = this.MatMul(net22, AI.D3.N3.w3);
      // console.log(net3);
      var net33 = this.Relu(net3);
      // console.log(net33);

      var net4 = this.MatMul(net33, AI.D3.N3.w4);
      // console.log(net4);
      var net44 = this.SoftMax(net4);
      // console.log(net44);

      return net44;
    },

    GuessHeadBool(inputarr) {
      for (var jj = 0; jj < this.snake.length; jj++) {
        // console.log(inputarr, this.snake[jj]);
        if (
          inputarr[0] == this.snake[jj].x &&
          inputarr[1] == this.snake[jj].y
        ) {
          return true;
        }
      }
      return false;
    },

    GetInputs() {
      var head = [this.snake[0].x, this.snake[0].y];
      var result = [1, 1, 1, 0, 0, 0];
      // console.log(this.direction);
      var possible_dirs = [
        this.DIRECTIONS[this.direction],
        this.DIRECTIONS[(this.direction + 3) % 4],
        this.DIRECTIONS[(this.direction + 1) % 4],
      ];
      // console.log(possible_dirs);
      for (var i = 0; i < possible_dirs.length; i++) {
        for (var j = 0; j < 5; j++) {
          var guess_head = [
            head[0] + possible_dirs[i][0] * (j + 1) * 10,
            head[1] + possible_dirs[i][1] * (j + 1) * 10,
          ];

          console.log(guess_head);
          console.log(this.GuessHeadBool(guess_head));
          if (
            guess_head[0] < 0 ||
            guess_head[0] >= 300 ||
            guess_head[1] < 0 ||
            guess_head[1] >= 300 ||
            this.GuessHeadBool(guess_head)
          ) {
            console.log("if checked");
            result[i] = j * 0.2;
            break;
          }
        }
      }
      var bool1 = false;
      // console.log(result);
      for (var pix = 0; pix < 4; pix++) {
        console.log(this.snake[pix], this.food_x, this.food_y);
        if (
          this.snake[pix].x == this.food_x &&
          this.snake[pix].y == this.food_y
        ) {
          console.log("getfind");
          bool1 = true;
          break;
        }
      }
      // console.log(head, possible_dirs);

      if (
        bool1 &&
        this.NpSum(head, possible_dirs[0]) <=
          this.NpSum([this.food_x, this.food_y], possible_dirs[0])
      ) {
        result[3] = 1;
      }
      if (
        this.NpSum(head, possible_dirs[1]) <
        this.NpSum([this.food_x, this.food_y], possible_dirs[1])
      ) {
        result[4] = 1;
      } else {
        result[5] = 1;
      }
      var tmp_res = [];
      tmp_res.push(result);
      console.log(tmp_res);
      return tmp_res;
    },

    NpSum(arr1, arr2) {
      var sum = 0;
      for (var cal = 0; cal < arr1.length; cal++) {
        sum += arr1[cal] * arr2[cal];
      }
      return sum;
    },

    Step(direction) {
      // console.log(direction);
      var old_head = [this.snake[0].x, this.snake[0].y];
      var movement = this.DIRECTIONS[direction];
      this.dx = this.DIRECTIONS[this.direction][0] * 10;
      this.dy = this.DIRECTIONS[this.direction][1] * 10;
      // console.log(old_head);
      // console.log(movement);
      var new_head = [
        old_head[0] + movement[0] * 10,
        old_head[1] + movement[1] * 10,
      ];
      // console.log(new_head);
      if (
        new_head[0] < 0 ||
        new_head[0] >= 300 ||
        new_head[1] < 0 ||
        new_head[1] >= 300 ||
        [new_head[0], new_head[1]] in this.snake
      ) {
        return false;
      }
      return true;
    },

    MatMul(a, b) {
      var mul = [];
      var lena = a[0].length;
      var lenb = b[0].length;
      var row = [];
      for (var i = 0; i < lenb; i++) {
        var x = 0;
        for (var j = 0; j < lena; j++) {
          // console.log(0, j, j, i);
          // console.log(a[0][j], b[j][i]);
          x += Math.round(a[0][j] * b[j][i] * 1e8) / 1e8;
        }
        // console.log(x);
        row.push(x);
        // console.log(row);
      }

      mul.push(row);

      return mul;
    },

    Move_Snake() {
      // Create the new Snake's head
      const head = {
        x: this.snake[0].x + this.dx,
        y: this.snake[0].y + this.dy,
      };
      // Add the new head to the beginning of snake body
      this.snake.unshift(head);
      const has_eaten_food =
        this.snake[0].x === this.food_x && this.snake[0].y === this.food_y;
      if (has_eaten_food) {
        // Increase score, combo
        this.combo += 1;
        this.score += 1 + this.combo;

        // Generate new food location
        this.Gen_Food();
      } else {
        // Remove the last part of snake body
        this.snake.pop();
      }
    },
    ArgMax(arr) {
      var max = -999;
      var ans = 0;
      for (var i = 0; i < arr[0].length; i++) {
        // console.log(i);
        if (arr[0][i] > max) {
          max = arr[0][i];
          ans = i;
        }
      }
      return ans;
    },

    SnakeStart() {
      this.life = 3;
      this.Main();

      this.Gen_Food();
    },
    SubmitGameData() {
      axios
        .post("http://localhost:8080/Play/snake/", {
          gaId: 1,
          plLevel: 5,
          plscore: this.score,
          uiPk: 27,
        })
        .then((res) => {
          this.rank = res.data.rank;
          alert(`${this.rank}위에 랭크인 하셨습니다. 축하드립니다.`);
          // console.log(res);
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  mounted() {
    // document.addEventListener("keydown", this.Change_Direction);

    this.snakeboard = document.getElementById("snakeboardAI");
    this.snakeboard_ctx = this.snakeboard.getContext("2d");
  },
};
</script>