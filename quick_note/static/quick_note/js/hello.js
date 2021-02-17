console.log('hello there');

		<script>

/*
				// Errors
				let is_invalid = document.querySelectorAll('is_invalid');
				let noUserEmailError = document.getElementById('noUserEmailError');
				let WrongUserEmailError = document.getElementById('WrongUserEmailError');
				let noPasswordError = document.getElementById('noPasswordError');

				// Form fields
				let loginForm = document.getElementById("myform");
				let user_emailField = loginForm.elements.username_email;
				let passwordField = loginForm.elements.password;
				let hidePassword = document.getElementById('hidePassword');
				let viewPassword = document.getElementById('viewPassword');
				hidePassword.style.display = 'none';

				let passwordIcons = document.querySelectorAll('#passwordIcons img');

				passwordIcons.forEach(function(passwordIcon){

					passwordIcon.addEventListener('click', function(event){

						console.log(event.target.id);
						if(event.target === passwordIcon && event.target === viewPassword && event.target.id === 'viewPassword'){

							passwordField.type = "text";
							viewPassword.style.display = 'none';
							hidePassword.style.display = 'inline';

						}else{

							passwordField.type = "password";
							hidePassword.style.display = 'none';
							viewPassword.style.display = 'inline';

						}

					});

				});

				loginForm.addEventListener("submit", function(event){

					event.preventDefault();

					let xhttp = new XMLHttpRequest();

					xhttp.onreadystatechange = function(){

						if(this.readyState == 4 && this.status == "200"){
							if(this.responseText){
							let serverResponse = JSON.parse(this.responseText);
<!--							if(serverResponse.login_successful){-->

<!--								is_invalid.forEach((is_invalidP)=>{-->

<!--									is_invalidP.style.display = 'none';-->

<!--								});-->

<!--								noPasswordError.style.display = 'none';-->
<!--								noUserEmailError.style.display = 'none';-->
<!--								WrongUserEmailError.style.display = 'none';-->
<!--								user_emailField.style.borderBottom = '2px solid rgb(23, 190, 0)';-->
<!--								passwordField.style.borderBottom = '2px solid rgb(23, 190, 0)';-->
<!--								console.log('login_successful ', serverResponse);-->
<!--								loginForm.reset();-->

<!--								window.location.replace(" {% url 'quick_note:mynotes' %} ");-->

<!--							}else{-->

								if(serverResponse.no_user_email){

									console.log('no_user_email ', serverResponse);
									noUserEmailError.style.display = 'block';
									user_emailField.style.borderBottom = '2px solid #af0606';

								}else{

									noUserEmailError.style.display = 'none';
									user_emailField.style.borderBottom = '2px solid rgb(23, 190, 0)';


								}

								if(serverResponse.no_password){

									console.log('no_password ', serverResponse);
									noPasswordError.style.display = 'block';
									passwordField.style.borderBottom = '2px solid #af0606';

								}else{

									noPasswordError.style.display = 'none';
									passwordField.style.borderBottom = '2px solid rgb(23, 190, 0)';

								}

								if(serverResponse.wrong_user_email){

									console.log('wrong_user_email ', serverResponse);
									WrongUserEmailError.style.display = 'block';
									user_emailField.style.borderBottom = '2px solid #af0606';

								}else{

									WrongUserEmailError.style.display = 'none';
									user_emailField.style.borderBottom = '2px solid rgb(23, 190, 0)';

								}

								if(serverResponse.error_login){

									console.log('error_login ', serverResponse);
									openModal();

								}
							}

						};

					};

					xhttp.open("POST", "{% url 'quick_note:verifylogin' %}", true);

					xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

					let params = "user_email="+user_emailField.value+"&password="+passwordField.value;

					xhttp.send(params);

				});
*/
			</script>