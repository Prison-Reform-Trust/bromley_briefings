window.addEventListener("message", function (event) { 
    if (event.data && event.data["plotly-height"]) { 
        var iframes = document.querySelectorAll("iframe"); 
        
        for (var chartId in event.data["plotly-height"]) {
            for (var i = 0; i < iframes.length; i++) {
                if (iframes[i].contentWindow === event.source) { 
                    var height = event.data["plotly-height"][chartId] + "px"; 
                    iframes[i].style.height = height;
                    break;
                } 
            }
        }
    } 
});