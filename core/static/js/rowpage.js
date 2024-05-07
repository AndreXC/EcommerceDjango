var deshboard = document.getElementById("Buttonsettings");
var users = document.getElementById("ButtonUsers");
var Transacoa = document.getElementById("ButtonTransacao");


var maindesh = document.getElementById("maindesh");
var mainusers = document.getElementById("mainuser");
var maintransacao = document.getElementById("maintransacao");

if (deshboard && maindesh && mainusers && maintransacao ) {
    deshboard.addEventListener('click', function() {
        maindesh.style.display = 'block';
        mainusers.style.display = 'none';
        maintransacao.style.display ="none";
    });
}

if (users && maindesh && mainusers && maintransacao) {
    users.addEventListener('click', function() {
        maindesh.style.display = 'none';
        maintransacao.style.display ="none";
        mainusers.style.display = 'block';
    });
}

if (Transacoa && maindesh && mainusers && maintransacao) {
    Transacoa.addEventListener('click', function() {
        maindesh.style.display = 'none';
        mainusers.style.display = 'none';
        maintransacao.style.display ="block";
    });
}


