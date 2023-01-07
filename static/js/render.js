const steps = [];

const tree = document.getElementById("sim");

sim = {}

fetch("/sim")
    .then((response) => response.json())
    .then((data) => render(data));
    
function render(sim){

    for (let i = 1; i < sim['num_steps']+1; i++) {
        const title = document.createElement("h3");
        title.innerHTML = sim[`${i}`]["step"];

        const addButton = document.createElement("button");
        addButton.innerHTML = "+";
        addButton.setAttribute("class", sim[`${i}`]["step"])
        addButton.setAttribute("onClick", `add(this.getAttribute("class"))`)

        const subtractButton = document.createElement("button");
        subtractButton.innerHTML = "-";
        subtractButton.setAttribute("class", sim[`${i}`]["step"])
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

        step.appendChild(title);
        step.appendChild(cost);
        step.appendChild(time);
        step.appendChild(editButtons);

        tree.appendChild(step);

        steps.push(step);
    }
    for(let i = 1; i < sim['num_steps']; i++){
        from = document.getElementById(`s${sim[`${i}`]["step"]}`);
        next = sim[`${i}`]["next"];
        for(let j=0; j < next.length; j++){
            line = document.createElement("div")
            line.setAttribute("class", "line")

            tree.appendChild(line);

            to = document.getElementById(`s${next[j]["step"]}`)

            adjustLine(from, to, line)
            
        }
        
    }

}

function adjustLine(from, to, line) {
  var fT = from.offsetTop + from.offsetHeight / 2;
  var tT = to.offsetTop + to.offsetHeight / 2;
  var fL = from.offsetLeft + from.offsetWidth / 2;
  var tL = to.offsetLeft + to.offsetWidth / 2;

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

  line.style["-webkit-transform"] = "rotate(" + ANG + "deg)";
  line.style["-moz-transform"] = "rotate(" + ANG + "deg)";
  line.style["-ms-transform"] = "rotate(" + ANG + "deg)";
  line.style["-o-transform"] = "rotate(" + ANG + "deg)";
  line.style["-transform"] = "rotate(" + ANG + "deg)";
  line.style.top = top + "px";
  line.style.left = left + "px";
  line.style.height = H + "px";
}

function add(step){
    updateSim(step, true)
}

function reduce(step) {
    
    updateSim(step, false);
}

function updateSim(step_num, isAdd){
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

function updateStep(step_num, sim){
    cost = document.getElementById(`${step_num}cost`)
    time = document.getElementById(`${step_num}time`)

    console.log(sim[step_num])

    cost = sim[step_num]["cost"]
    time = sim[`${step_num}`]["time"]
}
