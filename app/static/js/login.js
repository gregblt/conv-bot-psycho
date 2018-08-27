
window.fbAsyncInit = function() {
FB.init({
appId      : '170159587033924',
cookie     : true,
xfbml      : true,
version    : 'v3.0'
});

FB.AppEvents.logPageView();   

};

(function(d, s, id){
var js, fjs = d.getElementsByTagName(s)[0];
if (d.getElementById(id)) {return;}
js = d.createElement(s); js.id = id;
js.src = "https://connect.facebook.net/en_US/sdk.js";
fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function loggedin() {

	document.getElementById('login-form').style.display='none'
	token=null;
	$('#login').replaceWith('<button id="logout" onclick="logout()" class="login-button">Logout</button>')
	FB.getLoginStatus(function(response) {
	    console.log(response);
	    token=response.authResponse.accessToken;
		FB.api('/me', {fields: 'first_name'}, function(response) {
		  console.log(response);
			var txt = "Hi "+response.first_name+"! How can I help you today?"
		  $("#chatlogs").append($('<div class="chat friend"><p class="chat-message">'+txt+'</p></div>').hide().fadeIn(500))
			$("#chatlogs")[0].scrollTop=$("#chatlogs")[0].scrollHeight
				      $.ajax({
	        url: '/login',
	        type: 'POST',
	        data:JSON.stringify({
	          'data':{'type':'FB',
	          'user':{'FB_id':response.id,
	      			'first_name':response.first_name}}
	        }),
	        contentType: 'application/json; charset=utf-8',
	        dataType: 'json',
	        success: function(response) {
	          console.log(response);

	        }
	    }); 
		});
 
	})

}

function logout() {
	
	first_name='';
	FB.api('/me', {fields: 'first_name'}, function(response) {
		  console.log(response);
		 first_name=response.first_name
var txt = "I hope to see you soon "+first_name+"!"

	FB.logout(function(response) {
		$('#logout').replaceWith('<button id="login" onclick="document.getElementById(\'login-form\').style.display=\'block\'" class="login-button">Login</button>')
		  $("#chatlogs").append($('<div class="chat friend"><p class="chat-message">'+txt+'</p></div>').hide().fadeIn(500))
			$("#chatlogs")[0].scrollTop=$("#chatlogs")[0].scrollHeight
	});
		});
	

}

function loggedout() {

	document.getElementById('login-form').style.display='none'
	$('#login').text("Login")

}
