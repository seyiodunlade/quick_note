let userLinks = document.querySelectorAll('#div1 ul li a');

        userLinks.forEach((userLink)=>{

            userLink.addEventListener('click', function(){


                for(let i = 0; i < userLinks.length; i++){


                    userLinks[i].classList.remove('active');

                }

                userLink.classList.add('active');

            });


        });