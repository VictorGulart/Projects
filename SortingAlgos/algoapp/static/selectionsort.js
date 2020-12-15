
// variables for the project
let width = 750;
let height = 750;
let canvasHeight = 850;
let values = []; // this will hold the values
let myCanvas;
let w = 10;
let run = true;


function setup () {
    var parent = document.getElementById('canvas-body');
    myCanvas = createCanvas(parent.clientWidth, canvasHeight);
    myCanvas.parent(parent);

    values = new Array(floor(parent.clientWidth/(2*w))-2);
    colors = new Array(floor(parent.clientWidth/(2*w))-2);
    
    for (let j=0; j<values.length; j++){
        values[j] = random(height);
        colors[j] = color(0,0,0);
    }
}


let i = 0; // these vars will run the loop
let j = 0;
let smaller = i;
function draw (){
    background(223);
    
    if (values[smaller] >= values[j]){
            colors[smaller] = color(0,0,0); // there is something smaller than this so set it back to black
            smaller = j;
    }
    
    if (i<values.length){
        if (j>=values.length){
            colors[i] = color(152,206,107); // the smaller in the right places is set to green
            swap(values, smaller, i);
            if (smaller!=i){
                colors[smaller] = color(0,0,0); // there is something smaller than this so set it back to black
            }
            i++;
            smaller = i; // comparison starts a the next value
            j = i;
        }else{
            j++;
        }
    } else{
        console.log('Finished')
        run = false;
    } 


    colors[smaller] = color(239,153,40); // the smaller at the moment turns orange

    for (let j = 0; j <values.length; j++){
        //stroke(colors[j]);
        //line(j*(w*2)+25, canvasHeight-50, j*(w*2)+25, height - values[j]);
        fill(colors[j]);
        rect(j*(w*2)+25, canvasHeight-50, w-3, -1*(height-values[j]));
    }

    if (!run){
        noloop();
    }
}

function mousePressed(){
    run = false;
}

function swap(values, smaller, i){
    temp = values[i];
    values[i] = values[smaller];
    values[smaller] =  temp;
}