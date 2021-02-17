
let closeBtns = document.querySelectorAll('.closeBtn');
window.addEventListener('click', outsideClick);
let share_notes = document.querySelectorAll('.shareNote');
let delete_notes = document.querySelectorAll('.deleteNote');
let deleteNoteForm = document.querySelector('#deleteNoteForm');
let shareNoteForm = document.querySelector('#shareNoteForm');
console.log(share_notes[0].parentElement.parentElement.parentElement.dataset.note_count)

let noteToBeShared = document.querySelector('#share_modal #share_modal-content #noteToBeShared');
let noteToBeDeleted = document.querySelector('#delete_modal #delete_modal-content #noteToBeDeleted');

console.log(noteToBeDeleted);

closeBtns.forEach(closeBtn => {

    closeBtn.addEventListener('click', function(){

        if(closeBtn.id == 'closeShareModalBtn'){

            noteToBeShared.innerHTML = '';
            closeModal('share_modal');

        }

        if(closeBtn.id == 'closeDeleteModalBtn'){

            noteToBeDeleted.innerHTML = '';
            closeModal('delete_modal');

        }

    });




});

//Open modal when the share note icon is clicked
share_notes.forEach(share_note => {

    share_note.addEventListener('click', function(e){
        e.stopPropagation();
        noteToBeShared.innerHTML  = share_note.parentElement.parentElement.parentElement.dataset.note_count;
        shareNoteForm.action = '/mynotes/generate_note_link/' + share_note.parentElement.parentElement.parentElement.dataset.note_count + '/';
        openModal('share_modal');

    });

});

//Open delete modal when the delete note icon is clicked
delete_notes.forEach(delete_note => {

    delete_note.addEventListener('click', function(e){
        e.stopPropagation();
        console.log('deleteNoteForm ACTION :', deleteNoteForm.getAttribute('action'));
        console.log('THIS :', this);
        noteToBeDeleted.innerHTML  = delete_note.parentElement.parentElement.parentElement.dataset.note_count;
        deleteNoteForm.action = '/mynotes/delete_note/' + delete_note.parentElement.parentElement.parentElement.dataset.note_count + '/';
        console.log('deleteNoteForm ACTION :', deleteNoteForm.getAttribute('action'));
        openModal('delete_modal');

    });

});


function openModal(id){

    document.getElementById(id).style.display = 'block';

}

function closeModal(id){
    document.getElementById(id).style.display = 'none';
}

function outsideClick(e){
	console.log(e.target);
	console.log(e);

	if(e.target == share_modal){
		document.getElementById('share_modal').style.display = 'none';
	}

	if(e.target == delete_modal){
		document.getElementById('delete_modal').style.display = 'none';
	}
}

console.log(closeBtns);