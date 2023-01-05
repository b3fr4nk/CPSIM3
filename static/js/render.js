const steps = [];

const tree = document.getElementById("sim");

sim = {}

fetch("/sim")
    .then((response) => response.json())
    .then((data) => render(data));
    
function render(sim){

    console.log(sim)

    for (let i = 1; i < sim['num_steps']; i++) {
        const title = document.createElement("h3");
        title.innerHTML = sim[`${i}`]["step"];

        const addButton = document.createElement("button");
        addButton.innerHTML = "+";

        const subtractButton = document.createElement("button");
        subtractButton.innerHTML = "-";

        const editButtons = document.createElement("div");
        editButtons.appendChild(addButton)
        editButtons.appendChild(subtractButton)
        editButtons.setAttribute("class", "edit");

        const time = document.createElement("p");
        time.innerHTML = sim[`${i}`]["time"];
        time.setAttribute("class", "time")

        const cost = document.createElement("p");
        cost.innerHTML = sim[`${i}`]["cost"];
        cost.setAttribute("class", "cost")

        const step = document.createElement("div");
        step.setAttribute("class", "step");
        step.setAttribute("id", i)

        step.appendChild(title);
        step.appendChild(cost);
        step.appendChild(time);
        step.appendChild(editButtons);

        tree.appendChild(step);

        steps.push(step);
    }

}
