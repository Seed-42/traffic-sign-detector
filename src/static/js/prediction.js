$(document).ready(function(){

    $("#but_upload").click(function(){

      var fd = new FormData();
      var files = $('#file')[0].files;

      // Check file selected or not
      if(files.length > 0 ){
         fd.append('file',files[0]);

         $.ajax({
            url: '/predict',
            type: 'post',
            data: fd,
            contentType: false,
            processData: false,
            success: function(response){
               if(response != 0){
                 res = response
                 bytestring = response['location']
                 image = bytestring.split('\'')[1]
                  $("#img").attr("src",'data:image/jpeg;base64,'+image);
//                  $("#prediction").text("Object Prediction: "+res.predict);
                  $(".preview img").show(); // Display image element


                  $("#imgDetected").attr("src", 'data:image/jpeg;base64,'+image);
               }else{
                  alert('file not uploaded');
               }
            },
         });
      }else{
         alert("Please select a file.");
      }
    });
});
