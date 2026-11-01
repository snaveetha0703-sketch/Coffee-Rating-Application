
// Display all coffees
async function loadCoffees() {

    const response = await fetch("/api/coffees");
    const coffees = await response.json();

    const list = document.getElementById("coffee-list");

    list.innerHTML = "";

    coffees.forEach(coffee => {

        list.innerHTML += `
            <div class="card">
                <img src="${coffee.image}" alt="${coffee.name}">
                <h3>${coffee.name}</h3>
                <p>${coffee.description}</p>
                <p>Votes: ${coffee.votes}</p>

                <button onclick="vote(${coffee.id})">
                    Vote ☕
                </button>
            </div>
        `;

    });

    loadLeaderboard();
}


// Add a vote
async function vote(id) {

    const response = await fetch("/api/vote/" + id, {
        method: "POST"
    });

    if (response.ok) {
        loadCoffees();
    } else {
        alert("Unable to vote!");
    }
}


// Display top 5 coffees
async function loadLeaderboard() {

    const response = await fetch("/api/leaderboard");
    const data = await response.json();

    const board = document.getElementById("leaderboard");

    board.innerHTML = "";

    data.forEach((coffee, index) => {

        board.innerHTML += `
            <div class="leader">
                ${index + 1}. ${coffee.name}
                - ${coffee.votes} votes
            </div>
        `;

    });
}


// Load application
loadCoffees();
