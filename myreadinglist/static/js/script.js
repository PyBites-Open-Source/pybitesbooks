$(document).ready(function(){
    $("#searchTitles").autocomplete( "/api/get_books/", { minChars:3 });  
    
    // http://forum.jquery.com/topic/jquery-autocomplete-submit-form-on-result
    $("#searchTitles").result(function (event, data, formatted) {
        $("#searchProgress").append('<img src="img/loader.gif" alt="Loading ..." id="loading" />');
            var searchVal = $("#searchTitles").val();
            $("#searchTitles").val('');
            
            if(formatted.indexOf("notSelectRow") != -1) {    
                $("#loading").hide();
            } else {
                var bookid = formatted.replace(/.*id="([^"]+)".*/gi, "$1");
                location.href= "/books/" + bookid;                
            }
    });

});
