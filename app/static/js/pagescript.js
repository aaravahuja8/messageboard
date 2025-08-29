var pagenum = 1;
var pages
var pagecount

function displayFirst() {
    pages = document.getElementsByClassName("pages");
    pagecount = pages.length

    if (pagecount > 0) {
        pages[pagenum-1].style.display = "block";
        for (i=1; i < pagecount; i++) {
            pages[pagenum].style.display = "none";
        }
        document.getElementById("status").innerHTML = "Page 1/" + pagecount.toString()
    } else {
        document.getElementById("status").innerHTML = "This user has no posts"
        document.getElementById("status").style.fontSize = "20px"
        document.getElementsByClassName("control")[0].style.display = "none";
        document.getElementsByClassName("control")[1].style.display = "none";
    }
}

function prevPage() {
    var nextpage;

    if (pagenum != 1) {
        nextpage = pagenum-1;
    } else {
        nextpage = 1;
    }

    pages[pagenum-1].style.display = "none";
    pages[nextpage-1].style.display = "block";

    document.getElementById("status").innerHTML= "Page " + nextpage.toString() + "/" + pagecount.toString();

    pagenum = nextpage;
}

function nextPage() {
    var nextpage;

    if (pagenum != pagecount) {
        nextpage = pagenum+1;
    } else {
        nextpage = pagecount;
    }

    pages[pagenum-1].style.display = "none";
    pages[nextpage-1].style.display = "block";

    document.getElementById("status").innerHTML= "Page " + nextpage.toString() + "/" +pagecount.toString()

    pagenum = nextpage;
}