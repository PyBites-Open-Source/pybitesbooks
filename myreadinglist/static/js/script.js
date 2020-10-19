var pomodoroTimer;


function countDown(){
  var timer = document.getElementById("timer")
  timer.disabled = true;
  var cancelTimer = document.getElementById("cancelTimer")
  cancelTimer.style.display = "inline";

  var now = new Date().getTime();
  var end = new Date(now)
  // test
  // var countDownDate = end.setSeconds(end.getSeconds() + 3);
  var countDownDate = end.setMinutes(end.getMinutes() + 25);

  console.log(countDownDate);

  pomodoroTimer = setInterval(function() {

      now = new Date().getTime();
      var distance = countDownDate - now;

      var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      var seconds = Math.floor((distance % (1000 * 60)) / 1000);

      timer.innerHTML = "Time left: " + minutes + "m " + seconds + "s ";

      if (distance < 0) {
        cancelPomodoro();
        logPomodoro();
      }
  }, 1000);
}


function cancelPomodoro(){
  clearInterval(pomodoroTimer);
  var timer = document.getElementById("timer")
  timer.innerHTML = "Start Pomodoro";
  timer.disabled = false;
  var cancelTimer = document.getElementById("cancelTimer")
  cancelTimer.style.display = "none";
}


function logPomodoro(){
  document.getElementById("addPomo").submit();
}


$(document).ready(function(){
    $("#searchTitles").autocomplete( "/query_books/", { minChars:3 });  
    
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

$(function() {
    $( "#id_completed" ).datepicker({
        dateFormat: "yy-mm-dd"
    });
});
