const access_key = window.location.hash.substring(1);

if (access_key == "") {
    document.getElementById("controlPanel").style.display = "none";
    document.getElementById("askForPassphrase").style.display = "block";
}

// Basic socket.io stuff
var socket = io();
socket.on('connect', () => {
    socket.emit('newAdmin', {'password': access_key});
});

// Update question
document.getElementById("pushQuestion").onclick = () => {
    socket.emit('admin', {'question': document.getElementById("question").value, 'password': access_key});
}

// Add new question box
document.getElementById("newQ").onclick = () => {
    const opt = document.querySelector(".options");
    let el = document.createElement("div")
    el.innerHTML = `<div value="${opt.children.length}">
    <p>Option #${opt.children.length+1}</p>
    <input placeholder="Option..." type="text" >
</div>`;
    opt.appendChild(el);
    saveToBackend();
}

// Save options to backend
document.getElementById("saveQ").onclick = saveToBackend;

function saveToBackend() {
    const opt = document.querySelectorAll(".options > div");
    let resp = [];
    for (let i = 0; i < opt.length; i++) {
        // Question text.
        const textBox = opt[i].querySelector("input");
        if (textBox.value !== "") {
            resp.push(textBox.value);
        }
    }
    socket.emit('admin', {'options': resp, 'password': access_key});
}

// Unlock active clients
document.getElementById("unlock").onclick = () => {
    socket.emit('admin', {'lock': false, 'password': access_key});
}

// Lock active clients
document.getElementById("locker").onclick = () => {
    socket.emit('admin', {'lock': true, 'password': access_key});
}

// """Log In""" button
document.getElementById("quoteOnQuoteLogin").onclick = () => {
    window.location.href = `${window.location.href.substring(0, window.location.href.indexOf("#"))}#${document.getElementById("quoteOnQuoteAuth").value}`;
    window.location.reload();
}