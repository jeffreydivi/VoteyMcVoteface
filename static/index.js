// Lock user out after vote, enable results mode.
function lock() {
    window.localStorage.setItem("lock", 1);
    document.getElementById("lock").style.display = "block";
    document.getElementById("vote").style.display = "none";
}

// Unlock user when requested by server
function unlock() {
    window.localStorage.setItem("lock", 0);
    document.getElementById("lock").style.display = "none";
    document.getElementById("vote").style.display = "block";
}

// Page navigation buttons
const nextPageBtns = document.querySelectorAll("#pageNav");
for (let i = 0; i < nextPageBtns.length; i++) {
    nextPageBtns[i].onclick = (evt) => {
        const pages = document.querySelectorAll(".page");
        // Hide current pages
        for (let n = 0; n < pages.length; n++) {
            pages[n].style.display = "none";
        }
        // Show value page
        document.getElementById(evt.target.getAttribute("next")).style.display = "block"
    }
}

// Set up Socket + say hi to the server.
var socket = io();
socket.on('connect', () => {
    socket.emit('newUser', {});
});

// Configuration from server
socket.on('conf', (data) => {
    // !!! XSS Potential !!!
    const questions = document.querySelectorAll("#question");
    for (let i = 0; i < questions.length; i++) {
        questions[i].innerText = data['question']
    }

    // Set v-buck count
    document.getElementById("quadVoteCount").innerText = data['vbucks'];

    // Create elements: FPTP
    const opt = data['options'];
    for (let i = 0; i < opt.length; i++) {
        document.getElementById("fptpList").innerHTML += `<label value="${i}">
        <input type="radio" name="fptp">
        <span>${opt[i]}</span>
    </label>`;
    }

    // Create Borda list elements
    for (let i = 0; i < opt.length; i++) {
        document.getElementById("bordaList").innerHTML += `<span value="${i}" class="bordaEl">${opt[i]}</span>`;
    }

    // Create score-voting sliders
    for (let i = 0; i < opt.length; i++) {
        document.getElementById("scoreSliders").innerHTML += `<b>${opt[i]}</b>
        <input index="${i}" type="range" min="0" max="10" value="0">`
    }
    
    // Create quadratic steppers
    for (let i = 0; i < opt.length; i++) {
        document.querySelector(".vbuck-shop").innerHTML += `<div class="stepper">
        <div class="up">+</div>
        <div class="mid">
            <h3>${opt[i]}</h3>
            <span>Votes: <span>0</span></span>
        </div>
        <div class="down">-</div>
    </div>`;
    }
    // I hate this but it's needed.
    for (let i = 0; i < opt.length; i++) {
        document.querySelectorAll(".stepper")[i].value = 0;
    }


    // Borda list: Run this *after* placing the elements in.
    const borda = new Sortable(document.getElementById("bordaList"), {
        animation: 150,
        ghostClass: 'ghost'
    });

    // Quadratic stepper functionality
    const stepperList = document.querySelectorAll(".stepper");
    for (let i = 0; i < stepperList.length; i++) {
        stepperList[i].querySelector(".up").onclick = (evt) => {
            const el = evt.target.parentElement.querySelector(".mid > span > span");
            let vbucks = Number(document.getElementById("quadVoteCount").innerText);
            let curr = Number(el.innerText);
            let vbucks_dec = ((curr + 1) ** 2) - (curr ** 2);

            if (vbucks - vbucks_dec >= 0) {
                vbucks -= vbucks_dec;
                evt.target.parentElement.value = ++curr;
                el.innerText = evt.target.parentElement.value;
                document.getElementById("quadVoteCount").innerText = String(vbucks);
            }
        }
        stepperList[i].querySelector(".down").onclick = (evt) => {
            const el = evt.target.parentElement.querySelector(".mid > span > span");
            let vbucks = Number(document.getElementById("quadVoteCount").innerText);
            let curr = Number(el.innerText);
            let vbucks_inc = (curr ** 2) - ((curr - 1) ** 2);

            // Change "25" if config.vbucks is ever changed
            if (vbucks + vbucks_inc <= 25 && curr - 1 >= 0) {
                vbucks += vbucks_inc;
                evt.target.parentElement.value = --curr;
                el.innerText = evt.target.parentElement.value;
                document.getElementById("quadVoteCount").innerText = String(vbucks);
            }
        }
    }

    // document.querySelector('.up').parentElement.querySelector(".mid > span > span")
})

// Lock/unlock screen after vote (or whenever the server says so)
socket.on('status', (data) => {
    // This isn't really the most secure way to do this. You can change this in Burp Suite trivially, or, well, call unlock().
    if (data['data'] === "unlock") {
        if(data['invalid']) {
            alert("Invalid submission. Please try again.")
        }
        unlock();
    }
    else if (data['data'] === "lock") {
        lock();
    }
})

// Change question if the server requests such.
socket.on('question', (data) => {
    // !!! XSS Potential !!!
    const questions = document.querySelectorAll("#question");
    for (let i = 0; i < questions.length; i++) {
        questions[i].innerText = data['data']
    }
})

socket.on('updateResults', (data) => {
    console.info("Updating table...")
    
    document.getElementById("liveResults").innerHTML = data;;
})

// Pushing vote data from client to server.
document.getElementById("submit").onclick = () => {
    // Collect all vote information and send them to server.
    lock();

    // Count FPTP rankings
    const radios = document.querySelectorAll("[type=radio]");
    let fptp = -1;
    for (let i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            fptp = i;
            break;
        }
    }

    // Return Borda rankings
    const bordaRanks = document.querySelectorAll("#bordaList > span");
    let borda = [];
    for (let i = 0; i < bordaRanks.length; i++) {
        borda.push(Number(bordaRanks[i].getAttribute("value")));
    }

    // Return score-voting values
    const scoreRanks = document.querySelectorAll("#scoreSliders > input");
    let scoreVote = []
    for (let i = 0; i < scoreRanks.length; i++) {
        scoreVote.push(Number(scoreRanks[i].value));
    }

    // Return quadratic rankings
    const quadStep = document.querySelectorAll(".vbuck-shop > .stepper");
    let quad = [];
    for (let i = 0; i < quadStep.length; i++) {
        quad.push(Number(quadStep[i].value));
    }

    const data = {
        "data": "User voted.",
        "fptp": fptp,
        "borda": borda,
        "score": scoreVote,
        "quad": quad
    }

    console.info(data);

    socket.emit('voteSubmit', data);
}

if (window.localStorage.getItem("lock") === "1")
    lock();
else
    unlock();