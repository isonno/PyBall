//
// Browse images captured by PyBall
//

// Note the server doesn't have keywords yet; these would be of the form
//  browse/key?param=value&param2=value
//
$(function() {

    var server = "http://eyeball/cgi-bin/browse?"
    var imagePath = "http://eyeball/lapse/";

    var images = [];
    var curImage = 0;

    function parseImages( serverData, status )
    {
        var imageNameList = serverData;
        $("#imageCount").text(String(imageNameList.length));
        var progress = new ProgressIndicator( "Loading images...", imageNameList.length);
        for (var i in imageNameList)
        {
            images[i] = new Image();
            images[i].src = imagePath + imageNameList[i];
            $(images[i]).load( progress.stepProgress );
        }
        $("#picture").attr("src", images[curImage].src);
        $("#slider").attr("max", imageNameList.length-1);
        $("#slider").attr("value", curImage);
    }

    function loadImageNames()
    {
        $.getJSON( server + "date-start=16-03-19&date-end=16-03-19", parseImages )
    }
    
    function display()
    {
        if (curImage >= images.length)
            curImage = 0;
        if (curImage < 0)
            curImage = images.length-1;
        $("#picture").attr("src", images[curImage].src);
        $("#slider").attr("value", curImage);
        // Stupid hack to get the slider to update
        $("#slider").attr("max", 2000);
        $("#slider").attr("max", Number(images.length-1));
    }

    function displayStep(delta)
    {
        curImage += delta;
        display();
    }

    $("#next").click(function () { displayStep(+1);} );
    $("#prev").click(function () { displayStep(-1); });
    $("#slider").change(function () {curImage = Number($("#slider").val()); display();});

    $(document).keydown(function(event)
    {
    //  var modKeys = ['shiftKey', 'metaKey', 'altKey', 'ctrlKey'];
        var step = 1;
        if (event['shiftKey']) step = 10;
        if (event.keyCode == 37) { displayStep(-step);}	// left arrow
        if (event.keyCode == 39) { displayStep(+step);} // right arrow
    });

    function resizePage()
    {
        ProgressIndicator.setToWindowWidth();
        var width = window.innerWidth - 10;;
        var height = width * 0.75;  // 3:4 images
        $("#picture").width(width);
        $("#picture").height(height);
    }

    window.onresize = resizePage;
    resizePage();

    $("#load").click( loadImageNames );
    ProgressIndicator.trackWindowWidth();
});
