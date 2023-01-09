const steps = [];

const tree = document.getElementById("sim");

sim = {}

const days = document.getElementById("days");
const tCost = document.getElementById("cost")


fetch("/sim")
    .then((response) => response.json())
    .then((data) => render(data));
    
function render(sim){
    // add steps
    for (let i = 1; i < sim['num_steps']+1; i++) {
        // set up each html element
        const title = document.createElement("h3");
        if(i == 44){
          title.innerHTML = "End";
        }
        else{
          title.innerHTML = sim[`${i}`]["step"];
        }
        

        const addButton = document.createElement("button");
        addButton.innerHTML = "+";
        addButton.setAttribute("id", `${sim[`${i}`]["step"]}-`);
        addButton.setAttribute("class", `${sim[`${i}`]["step"]}`);
        addButton.setAttribute("onClick", `add(this.getAttribute("class"))`)

        const subtractButton = document.createElement("button");
        subtractButton.innerHTML = "-";
        subtractButton.setAttribute("id", `${sim[`${i}`]["step"]}+`)
        subtractButton.setAttribute("class", `${sim[`${i}`]["step"]}`);
        subtractButton.setAttribute("onClick", `reduce(this.getAttribute("class"))`)


        const editButtons = document.createElement("div");
        editButtons.appendChild(addButton)
        editButtons.appendChild(subtractButton)
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
    }

    days.innerHTML = `Days:${sim["days"]}`;
    tCost.innerHTML = `$${sim["cost"]}`
    
    // add lines
    for(let i = 1; i < sim['num_steps']; i++){
        from = document.getElementById(`s${sim[`${i}`]["step"]}`);
        next = sim[`${i}`]["next"];
        isRed = false
        
        for(let j = sim["path"].length-1; j >= 0; j--){
            if (Number(sim[`${i}`]["step"]) == Number(sim["path"][j])) {
              isRed = true;
            }
        }
        
        for(let j=0; j < next.length; j++){
            line = document.createElement("div")
            line.setAttribute("class", "line")
            line.setAttribute("id", `${sim[`${i}`]["step"]}-${next[j]["step"]}`)           

            tree.appendChild(line);

            to = document.getElementById(`s${next[j]["step"]}`)

            adjustLine(from, to, line)

            linePath = next[j]["step"]

            // if (isRed) {
            //     for(let k = sim["path"].length -1; k >= 0; k--){
            //         if (Number(linePath) == Number(sim["path"][k])) {
            //           line.style.backgroundColor = "red";
            //         } 
            //     }
            //     if(Number(linePath) == 44){
            //         line.style.backgroundColor = "red";
            //     }
            // }
        } 
    }

    drawCriticalPath(sim)
}

function drawCriticalPath(sim){
  lines = document.getElementsByClassName("line") 
  for(let i = 0; i < lines.length; i++){
    lines[i].style.backgroundColor = "black";
  }
  
  for(let j = 1; j < sim["path"].length; j++){
    lineID = `${sim["path"][j]}-${sim["path"][j - 1]}`;
    line = document.getElementById(`${lineID}`)
    line.style.backgroundColor = "red"
  }
  lineID = `${sim["path"][0]}-44`
  line = document.getElementById(lineID)
  line.style.backgroundColor = "red"
}

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

  days.innerHTML = `Days:${sim["days"]}`;

  // let sbutton = document.getElementById(`${step_num}+`);
  // let abutton = document.getElementById(`${step_num}-`)
  //less than or equal because this is called after being pressed therefore is 1 more than actual
  // if (sim[`${step_num}`]["reductions"] <= 1) {
  //   abutton.setAttribute("disabled", "true")
  //   sbutton.setAttribute("disabled", "false")
  // }
  // if (sim[`${step_num}`]["reductions"] > 1){
  //   abutton.setAttribute("disabled", "false");
  //   sbutton.setAttribute("disabled", "true");
  // }

  drawCriticalPath(sim);
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
      .then((response) => console.log(response));
}
