const events = {
    search: {
        selector: ".searchButton",
        trigger: "click",
        callback: handleSearchButtonEvent
    },
    comment: {
        selector: "textarea[name='comment']",
        trigger: "keydown",
        callback: handleCommentEvent
    },
    revise: {
        selector: ".reviseButton",
        trigger: "click",
        callback: handleReviseButtonEvent
    },
    reject: {
        selector: ".rejectButton",
        trigger: "click",
        callback: handleRejectButtonEvent
    },
    liveSearch: {
        selector: "input[name='keywords']",
        trigger: "input",
        callback: handleLiveSearchEvent
    }
};

function timer(seconds, element) {
    element.innerText = `Tiempo aproximado: ${seconds} segundos.`;
    if (seconds > 0) {
        setTimeout(() => timer(seconds - 1, element), 1000);
    }
}

function fetchUrl(url, refresh=false, options={}) {
    fetch(url, options)
        .then(response => {
            if (response.ok && refresh) {
                location.href = location.href;
            } else {
                console.log(response.status);
            }
        })
        .catch(error => {
            console.log(error.message);
        });
}

function handleCommentEvent(event) {
    if (event.key !== 'Enter') return;
    event.target.parentElement.submit();
}

function handleRejectButtonEvent(event) {
    if (!window.confirm(event.target.defaultValue+"?")) {
        event.preventDefault();
    }
}

function handleReviseButtonEvent(event) {
    console.log("Revised");
}

function handleSearchButtonEvent(event) {
    event.preventDefault();

    const loader = document.createElement("div");
    const spinner = document.createElement("div");
    const message = document.createElement("p");

    loader.appendChild(spinner);
    loader.appendChild(message);
    document.body.appendChild(loader);

    loader.classList.add("loader");
    document.body.classList.add("loading");

    const seconds = event.target.dataset.seconds;
    timer(seconds, message);

    fetchUrl(event.target.href, true);
}

function handleLiveSearchEvent(event) {
    const words = event.target.value.split(" ");
    const list = document.querySelector("#props");

    list.querySelectorAll("li.item").forEach(item => {
        const match = words.some(word =>
            item.innerText.toLowerCase().includes(word.toLowerCase())
        );
        item.style.display = match ? 'block' : 'none';
    });
}

document.addEventListener("DOMContentLoaded", () => {
    Object.values(events).forEach((event) => {
        const buttons = document.querySelectorAll(event.selector);
        buttons.forEach(button => {
            button.addEventListener(event.trigger, e => event.callback(e));
        });
    });
});
