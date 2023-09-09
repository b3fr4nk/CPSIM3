const steps = [];

const tree = document.getElementById("sim");

sim = {}

const remaining = document.getElementById("days");
const tCost = document.getElementById("cost")
const day = document.getElementById("day")
const progressButton = document.getElementById('progress')
progressButton.addEventListener('click', function() {progress()})


fetch("/sim")
    .then((response) => response.json())
    .then((data) => render(data));
    
function render(sim){
    // add steps
    for (let i = 1; i < 44; i++) {
        // set up each html element
        const title = document.createElement("h3");
        if(i == 44){
          title.innerHTML = "End";
        }
        else{
          title.innerHTML = sim[`${i}`]["step"];
        }

        day.innerHTML = `Day ${sim["day"]}`
        
        const addButton = document.createElement("button");
        addButton.innerHTML = "+";
        addButton.setAttribute("id", `${sim[`${i}`]["step"]}+`);
        addButton.setAttribute("class", `${sim[`${i}`]["step"]}`);
        addButton.addEventListener("click", function() { add(sim[`${i}`]["step"])})
        
        const subtractButton = document.createElement("button");
        subtractButton.innerHTML = "-";
        subtractButton.setAttribute("id", `${sim[`${i}`]["step"]}-`)
        subtractButton.setAttribute("class", `${sim[`${i}`]["step"]}`);
        subtractButton.addEventListener("click", function() { reduce(sim[`${i}`]["step"])})

        const editButtons = document.createElement("div");
        editButtons.appendChild(addButton);
        editButtons.appendChild(subtractButton);
        editButtons.setAttribute("class", "edit");

        const time = document.createElement("p");
        time.innerHTML = `${sim[`${i}`]["time"]} Days`;
        time.setAttribute("class", "time")
        time.setAttribute("id", `${i}time`)

        const cost = document.createElement("p");
        cost.innerHTML = `$${sim[`${i}`]["cost"]}`;
        cost.setAttribute("class", "cost")
        cost.setAttribute("id", `${i}cost`)

        const step = document.createElement("div");
        step.setAttribute("class", "step");
        step.setAttribute("id", `s${i}`)

        // combine the html elements into one step
        step.appendChild(title);
        step.appendChild(cost);
        step.appendChild(time);
        step.appendChild(editButtons);

        tree.appendChild(step);

        steps.push(step);

        updateButton(i, sim);

        if (sim[`${i}`]["max_reductions"] == 0) {
          editButtons.remove(addButton)
          editButtons.remove(subtractButton)
        }
    }

    remaining.innerHTML = `Time Remaining:${sim["days"]}`;
    tCost.innerHTML = `$${sim["cost"]}`
    
    
    // add lines
    for(let i = 1; i < 44; i++){
        let from = document.getElementById(`s${sim[`${i}`]["step"]}`);
        let next = sim[`${i}`]["next"];
        let isRed = false
        
        for(let j = sim["path"].length-1; j >= 0; j--){
            if (Number(sim[`${i}`]["step"]) == Number(sim["path"][j])) {
              isRed = true;
            }
        }
        for(let j=0; j < next.length; j++){
            let line = document.createElement("div")
            line.setAttribute("class", "line")
            line.setAttribute("id", `${sim[`${i}`]["step"]}-${next[j]["step"]}`)           

            tree.appendChild(line);
            if(next[j]["step"] === 44){
              break
            }
            let to = document.getElementById(`s${next[j]["step"]}`)

            adjustLine(from, to, line)

            let linePath = next[j]["step"]
        } 
    }

    drawCriticalPath(sim)
}

function render_progress(sim){
  day.innerHTML = `Day ${sim["day"]}`
  tCost.innerHTML = `$${sim["cost"]}`
  remaining.innerHTML = `Time Remaining: ${sim["days"]}`

  for(let i = 1; i < 44; i++){
    const addButton = document.getElementById(`${i}+`)
    const subtractButton = document.getElementById(`${i}-`)
    const step = document.getElementById(`s${i}`)
    const cost = document.getElementById(`${i}cost`)
    const time = document.getElementById(`${i}time`)

    time.innerHTML = `${sim[`${i}`]["time"]} Days`
    cost.innerHTML = `$${sim[`${i}`]["cost"]}`

    if(sim[`${i}`]['is_active'] === false){
      if(addButton !== null && subtractButton !== null){
        addButton.disabled = true
        subtractButton.disabled = true
      }

      step.style.backgroundColor = '#808080'
    }
  }

  if(sim["day"] == sim["days"]){
    window.location.replace('/results')
  }

}

function drawCriticalPath(sim){
  //change all lines to black
  let lines = document.getElementsByClassName("line") 
  for(let i = 0; i < lines.length; i++){
    lines[i].style.backgroundColor = "black";
  }
  //change critical path to red
  for(let j = 1; j < sim["path"].length; j++){
    let lineID = `${sim["path"][j]}-${sim["path"][j - 1]}`;
    let line = document.getElementById(`${lineID}`)
    line.style.backgroundColor = "red"
  }
  //draw last line red
  let lineID = `${sim["path"][0]}-44`
  let line = document.getElementById(lineID)
  line.style.backgroundColor = "red"

}
//found this function online, modified slightly
function adjustLine(from, to, line) {
    // get start and end point of each line
  var fT = from.offsetTop + from.offsetHeight / 2;
  var tT = to.offsetTop + to.offsetHeight / 2;
  var fL = from.offsetLeft + from.offsetWidth;
  var tL = to.offsetLeft;
    // get angle each line needs 
  var CA = Math.abs(tT - fT);
  var CO = Math.abs(tL - fL);
  var H = Math.sqrt(CA * CA + CO * CO);
  var ANG = (180 / Math.PI) * Math.acos(CA / H);

  if (tT > fT) {
    var top = (tT - fT) / 2 + fT;
  } else {
    var top = (fT - tT) / 2 + tT;
  }
  if (tL > fL) {
    var left = (tL - fL) / 2 + fL;
  } else {
    var left = (fL - tL) / 2 + tL;
  }

  if (
    (fT < tT && fL < tL) ||
    (tT < fT && tL < fL) ||
    (fT > tT && fL > tL) ||
    (tT > fT && tL > fL)
  ) {
    ANG *= -1;
  }
  top -= H / 2;

//   adjust line with math done above
  line.style["-webkit-transform"] = "rotate(" + ANG + "deg)";
  line.style["-moz-transform"] = "rotate(" + ANG + "deg)";
  line.style["-ms-transform"] = "rotate(" + ANG + "deg)";
  line.style["-o-transform"] = "rotate(" + ANG + "deg)";
  line.style["-transform"] = "rotate(" + ANG + "deg)";
  line.style.top = top + "px";
  line.style.left = left + "px";
  line.style.height = H + "px";
}

// for when add button is pressed
function add(step){
    updateSim(step, false)
}
// for when reduce button is pressed
function reduce(step) {
    console.log(step)
    updateSim(step, true);
}
// updates whole sim 
function updateSim(step_num, isAdd){
    // get data from server
    fetch("/update", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({"step_num":step_num, "isAdd":isAdd}),
    })
      .then((response) => response.json())
      .then((response) => updateStep(step_num, response));
}
// change the values inside each step
function updateStep(step_num, sim){
  let cost = document.getElementById(`${step_num}cost`);
  let time = document.getElementById(`${step_num}time`);


  cost.innerHTML = `$${sim[`${step_num}`]["cost"]}`;
  time.innerHTML = `${sim[`${step_num}`]["time"]} Days`;
  
  tCost.innerHTML = `$${sim["cost"]}`

  remaining.innerHTML = `Time Remaining:${sim["days"]}`;

  updateButton(step_num, sim)

  drawCriticalPath(sim);
}
//updates the button to disabled or enabled
function updateButton(step_num, sim){
  try {
    let sbutton = document.getElementById(`${step_num}-`);
    let abutton = document.getElementById(`${step_num}+`);

      // less than or equal because this is called after being pressed therefore is 1 more than actual
    if (Number(sim[`${step_num}`]["reductions"]) < 1) {
      abutton.disabled = false;
      sbutton.disabled = true;
    } else if (Number(sim[`${step_num}`]["reductions"]) > Number(sim[`${step_num}`]["max_reductions"]) - 1) {
      abutton.disabled = true;
      sbutton.disabled = false;
    } else {
      abutton.disabled = false;
      sbutton.disabled = false;
    }
  } catch {
    console.log(`no buttons for step ${step_num}`)
  }

}

function progress(){
    // send progress command to server and get results from server
    fetch("/progress", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({"next":true}),
    })
      .then((response) => response.json())
      .then((response) => render_progress(response))
}