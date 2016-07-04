//
// Browse images captured by PyBall
//

// Note the server doesn't have keywords yet; these would be of the form
//  browse/key?param=value&param2=value
//
$(function() {

var server = "http://eyeball/cgi-bin/browse?"
var imageList = [];

function parseImages( serverData, status )
{
    imageList = serverData;
    $("#imageCount").text(String(imageList.length));
}


function loadImageNames()
{
    $.getJSON( server + "date-start=16-03-19&date-end=16-03-20", parseImages )
}


$("#load").click( loadImageNames );

});
