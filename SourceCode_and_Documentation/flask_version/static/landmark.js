// About
var about = document.getElementById("about_element");
var fetch_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + document.getElementById("lm_name").innerHTML;

var fetchData;
fetch(fetch_url, fetchData)
.then(response => response.json())
.then(data => {
    if (data.extract == null) {
        about.innerText = "No Information about this landmark.";
    }
    else {
        about.innerText = data.extract;
    }    
})

//Image
var image = document.getElementById("lm_img");
console.log(document.getElementById("lm_name").innerHTML)
fetch_url = "https://en.wikipedia.org/api/rest_v1/page/media-list/" + document.getElementById("lm_name").innerHTML;
console.log(fetch_url)
fetch(fetch_url, fetchData)
.then(response => {
    if (response.ok) {
        return response.json()
    } else {
        return Promise.reject('some error happend maybe 404') 
    }
})
.then(data => {
    console.log(data)
    image.setAttribute("src", data.items[0].srcset[0].src);
})
.catch(error => console.log('error is', error));

var lm_name = document.getElementById("lm_name").innerHTML;
apiKey = "e8bf85737a554b158b25de6857b8de10"
newsAPIurl = "https://newsapi.org/v2/everything?qintitle=" + document.getElementById("news_name").innerHTML + "&apiKey=" + apiKey
fetch(newsAPIurl, fetchData)
.then(response => response.json())
.then(data => {
    console.log("newsapi")
    console.log(data)
    newsUl = document.getElementById('news_list')
    if (data.totalResults == 0) {
        const newsLi = document.createElement("li");
        newsLi.className = "list-group-item";
        newsLi.innerText = "No news about this landmark"
        newsUl.appendChild(newsLi)
    } else {
        // For each article 
        for (i = 0; i < data.totalResults && i < 5; i++) {
            article = data.articles[i]
            const articleLi = document.createElement("li");
            articleLi.className = "list-group-item li_item";
            const a = document.createElement("a");
            a.href = article.url
            const title = document.createElement("h5");
            title.innerText = article.title 
            const description = document.createElement("p");
            description.innerText = article.description

            a.appendChild(title)
            a.appendChild(description)
            articleLi.appendChild(a)
            // articleLi.appendChild(description)
            newsUl.appendChild(articleLi)
            console.log(data.articles[i].title)
        }
    }
})

$("#bookmark_btn").click(function(e) {
    e.preventDefault()
    var landmark = document.getElementById("lm_name").innerHTML;
    var category = document.getElementById("categoryhidden").value;
    $.post("/bookmark", {
        landmark: landmark,
        "category": category
    });
});

function add_event(e, name, date, url){
    $.post("/events", {
        name: name,
        date: date,
        url: url
    });
};

$(".add-review").click(function() {
    $(".option-error").html("");
    if (!$("input[name='rating']:checked").val()) {
        $(".option-error").html("Please rate this landmark");
        $(".option-error").addClass("alert alert-danger")
    }
});
