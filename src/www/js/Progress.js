//
// Progress indicator
//

// Expects HTML of:
//  <progress id="progress" max="1" value="0" width="100" height="20"></progress>
//  <span id="progressLabel" style="font-style: italic;margin-left:8px;"></span>

function ProgressIndicator( title, maxStep )
{
    $("#progress").attr( "max", maxStep );
    $("#progress").val(0);
    $("#progressLabel").text(title);
}

ProgressIndicator.prototype.stepProgress = function()
{
    $("#progress").val($("#progress").val() + 1);
    if ($("#progress").val() == $("#progress").attr("max")) // String to number compare
        $("#progressLabel").text("");
};
