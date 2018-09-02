$(function(){
  $.ajax({
    url : "http://127.0.0.1:5000/",
    type : "GET",
    success : function(response){
      $('#title').text(response);
      console.log(response);
    },
    error : function(error){
      console.log("Error: " + error);
    }
  });
}); 