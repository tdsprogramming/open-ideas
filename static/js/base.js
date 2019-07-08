$(document).ready(function(){
   $('select').formSelect();
   $('.parallax').parallax();
   $("#chatbox-btn").click(function(){
       $("#chatbox").css('display', 'block');
       $("#chat").css('height', 'auto');
       $("#chatbox-btn").css('display', 'none');
   });
   $("#chatbox-close").click(function(){
       $("#chatbox").css('display', 'none');
       $("#chat").css('height', '3rem');
       $("#chatbox-btn").css('display', 'block');
   });

 });
