console.log('IN livesearch');

let submitSearchBtn = document.querySelector('#div2 #dashboard_header #submitSearchBtn')
let searchInput = document.querySelector('#div2 #dashboard_header input#search');

    searchInput.addEventListener('keyup', function(e){

        let searchValue = e.target.value;
        console.log(searchValue);
        if(searchValue.length == 0){
            console.log('NOthing');
            submitSearchBtn.style.display = 'none';

        }else{
            console.log('You typed something');
            submitSearchBtn.style.display = 'inline-block';
        }
    });


    submitSearchBtn.addEventListener('click', function(){

        searchInputValue = searchInput.value;
        searchInput.value = '';
        window.location.href = '/mynotes/search?keyword=' + searchInputValue;

    })