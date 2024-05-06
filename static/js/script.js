const searchButtonSelector = ".searchButton"; 
const commentButtonSelector = ".commentButton";
const reviseButtonSelector = ".reviseButton";
const rejectButtonSelector = ".rejectButton";

function addSearchButtonEvent(searchButton){
    searchButton.addEventListener("click", event=>{
        event.preventDefault();
        var loader = document.createElement("div");
        loader.classList.add("loader");
        var spinner = document.createElement("div");
        var message = document.createElement("p");
        message.innerText = "Esto puede tardar algunos minutos...";
        loader.appendChild(spinner);
        loader.appendChild(message);
        document.body.appendChild(loader);
        document.body.classList.add("loading");
        
        fetch(event.target.href)
        .then(
            response => {
                if (response.ok) {
                    location.href = location.href
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
        alert(`Publicacion ${action}.`);
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
});