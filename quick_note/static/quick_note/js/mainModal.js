	
	//modal = document.getElementById('modal');

	document.getElementById('closeBtn').addEventListener('click', closeModal);
	
	window.addEventListener('click', outsideClick);
	
	function openModal(){
		
		document.getElementById('modal').style.display = 'block';
	}
	
	
	function closeModal(){
		document.getElementById('modal').style.display = 'none';
	}
	
	function outsideClick(e){
		console.log(e.target);
		console.log(e);
		if(e.target == modal){
			document.getElementById('modal').style.display = 'none';
		}
	}