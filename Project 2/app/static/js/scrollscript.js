var i=0;
var end = false;

const xhttp = new XMLHttpRequest();
xhttp.onload = function() {
    var data = JSON.parse(this.responseText);
    if (data.titles != null) {
        var length = data.titles.length;
        for (j=0; j < length; j++) {
            document.getElementById("post" + i.toString()).style.display = "block";
            document.getElementById("title" + i.toString()).innerHTML = data.titles[j];
            document.getElementById("subtitle" + i.toString()).innerHTML = data.subtitles[j];
            document.getElementById("content" + i.toString()).innerHTML = data.content[j];
            document.getElementById("comment" + i.toString()).innerHTML = data.comments[j];
            i=i+1;
        }

        if (length == 0) {
            end = true;
        }
    } else {
    end = true;
    }
}


window.onscroll = function(e) {
    if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight) {
        if (end == false) {
            xhttp.open("GET", "/load" + i.toString(), true);
            xhttp.send();
        }
    }
};

window.onload = function(e) {
    var k = 5;
    while (document.getElementById("post" + k.toString()) != null) {
        document.getElementById("post" + k.toString()).style.display = "none";
        k++;
    }
    xhttp.open("GET", "/load0", true);
    xhttp.send();
};