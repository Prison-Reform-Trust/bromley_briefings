window.addEventListener("message", function (event) { 
    console.log("Received message:", event.data); // Debug log
    
    if (event.data && event.data["plotly-height"]) { 
        var iframes = document.querySelectorAll("iframe"); 
        console.log("Found", iframes.length, "iframes"); // Debug log
        
        for (var chartId in event.data["plotly-height"]) {
            console.log("Processing chart ID:", chartId); // Debug log
            
            for (var i = 0; i < iframes.length; i++) {
                // Check if this iframe's source URL matches or if it's the message source
                var iframe = iframes[i];
                var isMatchingIframe = iframe.contentWindow === event.source;
                
                console.log("Checking iframe", i, "- matches source:", isMatchingIframe); // Debug log
                
                if (isMatchingIframe) { 
                    var height = event.data["plotly-height"][chartId] + "px"; 
                    console.log("Setting height to:", height); // Debug log
                    
                    // Set the style.height property, not the height attribute
                    iframe.style.height = height;
                    break;
                } 
            }
        }
    } 
});