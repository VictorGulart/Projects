
let width = 750;
let height = 750;
let canvasHeight = 850;
let values = [];
let myCanvas;
let i = 0;
let w = 10;
let run = true;

function setup(){
    // get canvas parent
    var parent = document.getElementById('canvas-body');
    
    // create the canvas and set the parent the section
    myCanvas = createCanvas(parent.clientWidth, canvasHeight);
    myCanvas.parent('canvas-body');
    //mycanvas.style('margin', 'auto');


    // set the array with the size of half the width    
    values = new Array(floor(parent.clientWidth/w));

    // set values to be drawn on screen as random 
    for (let i=0; i<values.length; i++){
        values[i] = random(height);
    }

    frameRate(10);
}

let lineColor = 0;

function draw() {
    // this method is called over and over again
    background(223);
    
    if (i < values.length){
        for (let j = 0; j < values.length - i - 1; j++){
            if (values[j] < values[j+1]){
                swap(values, j, j+1);
            }
        }
    } else {
        run = false;
    }
    
    
    // increment i because the next iteration is going to run one less time.
    i++;

    for (let i=1; i<values.length-1; i++){
        stroke(0);
        fill(254);
        rect(i*w, height + (canvasHeight - height)/2, w-3, -1 * (height - values[i]));
    } 

    if (!run){
        noloop();
    }
}

function swap(values, a, b){
    let temp = values[a];
    values[a] = values[b];
    values[b] = temp;
}

