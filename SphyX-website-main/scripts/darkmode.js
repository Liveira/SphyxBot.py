
var isEnabled = true; // o tema esta ativado?



function darkmode() {
    let paragraphs = document.getElementsByClassName('text');

    isEnabled = !isEnabled;
    
    if (isEnabled == true) {
        document.body.style.backgroundImage = "url(https://w.wallhaven.cc/full/6q/wallhaven-6qx916.png)";
        document.body.style.backgroundColor = "#23272A";
        for (let i = 0; i < paragraphs.length; i++) {

            paragraphs[i].style.color = 'white';

        }
    } else {
        document.body.style.backgroundColor = "aliceblue";
        document.body.style.backgroundImage = "none";
        for (let i = 0; i < paragraphs.length; i++) {

            paragraphs[i].style.color = 'black';

        }
    }
}

