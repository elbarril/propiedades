const searchButtonSelector = ".searchButton"; 
const commentButtonSelector = ".commentButton";
const reviseButtonSelector = ".reviseButton";
const rejectButtonSelector = ".rejectButton";
const liveSearchButtonSelector = "input[name='keywords']";

function timer(seconds, element) {
    element.innerText = "Tiempo aproximado: " + seconds + " segundos.";
    setTimeout(() => timer(seconds - 1, element), 1000);
}

function addSearchButtonEvent(searchButton){
    searchButton.addEventListener("click", event=>{
        event.preventDefault();

        var loader = document.createElement("div");
        var spinner = document.createElement("div");
        var message = document.createElement("p");

        loader.appendChild(spinner);
        loader.appendChild(message);
        document.body.appendChild(loader);

        loader.classList.add("loader");
        document.body.classList.add("loading");

        var seconds = event.target.dataset.seconds;
        timer(seconds, message);
        
        fetch(event.target.href)
        .then(
            response => {
                if (response.ok) {
                    location.href = location.href;
                }else{
                    console.log(response.status);
                }
            }
        ).catch(function (error) {
          console.log(error.message);
        });;
    });
}

function addCommentButtonEvent(commentButton){
    commentButton.addEventListener("click", ()=>{
        console.log("Se agrego comentario.");
    });
}

function addReviseButtonEvent(reviseButton){
    reviseButton.addEventListener("click", event=>{
        action = event.target.value == 'Revisado' ? 'revisada' : 'restaurada';
        console.log(`Publicacion ${action}.`);
    });
}

function addRejectButtonEvent(rejectButton){
    rejectButton.addEventListener("click", event=>{
        action = event.target.value == 'Rechazar' ? 'rechazada' : 'restaurada';
        if (!window.confirm("Rechazar?")) {
            event.preventDefault();
        }
    });
}

function addliveSearchButtonEvent(button){
    button.addEventListener("input", event => {
        const words = event.target.value.split(" ");
        const list = document.querySelector("#props");

        list.querySelectorAll("li.item").forEach(item => {
            let match = false;

            words.forEach(word => {
                if (item.innerText.toLowerCase().includes(word.toLowerCase())){
                    match = true;
                }
            });

            if (!match) {
                item.style.display = 'none';
            }else{
                item.style.display = 'block';
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", ()=> {
    var searchButton = document.querySelectorAll(searchButtonSelector);
    searchButton.length && searchButton.forEach(b => addSearchButtonEvent(b));

    var commentButton = document.querySelectorAll(commentButtonSelector);
    commentButton.length && commentButton.forEach(b => addCommentButtonEvent(b));
    
    var reviseButton = document.querySelectorAll(reviseButtonSelector);
    reviseButton.length && reviseButton.forEach(b => addReviseButtonEvent(b));
    
    var rejectButton = document.querySelectorAll(rejectButtonSelector);
    rejectButton.length && rejectButton.forEach(b => addRejectButtonEvent(b));

    var liveSearchButton = document.querySelectorAll(liveSearchButtonSelector);
    liveSearchButton.length && liveSearchButton.forEach(b => addliveSearchButtonEvent(b));
});