$(function() {
  // Initialize
  var bLazy = new Blazy();
  // filter on the fly
  //http://www.marceble.com/2010/02/simple-jquery-table-row-filter/
  $.expr[':'].containsIgnoreCase = function(n,i,m){
    return jQuery(n).text().toUpperCase().indexOf(m[3].toUpperCase())>=0;
  };


  $(".qVal").click(function(){
    $(this).select();
  });

  $(".qVal").keyup(function(){
    $("#booksWrapper").children().hide();
    var data = this.value.split(" ");
    var jo = $("#booksWrapper").find(".book");
    $.each(data, function(i, v){
      jo = jo.filter("*:containsIgnoreCase('"+v+"')");
    });
    jo.show();
  }).focus(function(){
    this.value="";
    $(this).css({"color":"#999"});
    $(this).unbind('focus');
  }).css({"color":"#C0C0C0"});

  $(".defaultText").focus(function(srcc){
    if ($(this).val() == $(this)[0].title){
      $(this).removeClass("defaultTextActive");
      $(this).val("");
    }
  });
  $(".defaultText").blur(function(){
    if ($(this).val() == ""){
      $(this).addClass("defaultTextActive");
      $(this).val($(this)[0].title);
    }
  });
  $(".defaultText").blur();
});
