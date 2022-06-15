$('.button').on('click', function () {
    $('.login').addClass('loading').delay(2200).queue(function () {
        $(this).addClass('active')
    });
});


function LoginData(username,passwd){
    /*
      It sends the user credentials to the server
      and set auth token in cookies.

      If the cerdentials is invalid it give the message.
    */
      const XHR = new XMLHttpRequest();
      // Bind the FormData object and the form element\
      const FD = new FormData();
      FD.append("grant_type","")
      FD.append("username",username);
      FD.append("password",passwd);

      // Define what happens in case of error
      XHR.addEventListener( "error", function( event ) {
        alert( 'Oops something went wrong' );

      } );
      // Define whaLoginDatat happens on successful data submission
      XHR.addEventListener( "load", function(event) {

        if(XHR.status == 200){
            // redirect to home page.
          window.location.replace(window.location.origin+"/");
        }
        else{
          alert(" Invalid user credentials");
        }
      } );

      // Set up our request
      XHR.open( "POST", window.location.origin+"/login_user");

      XHR.setRequestHeader("Access-Control-Allow-Origin",window.location.origin);
      XHR.setRequestHeader("Access-Control-Allow-Credentials", "true");
      XHR.setRequestHeader("Access-Control-Allow-Methods", "POST");
      XHR.setRequestHeader("Access-Control-Allow-Headers", "Content-Type");
      // The data sent is what the user provided in the form
      XHR.send( FD );
  }



function submit(){
    username = document.getElementById("username").value;
    password = document.getElementById("password").value;
    LoginData(username,password)

}
