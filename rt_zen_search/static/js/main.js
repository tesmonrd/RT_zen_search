$(document).ready(function(){

  $(".sidebar").hide();

  $("#toggleAdv").click(function(){
      if($(".sidebar").is(":visible")){
        $(".sidebar").hide();
    } else {
        $(".sidebar").show();
    }
  });
});