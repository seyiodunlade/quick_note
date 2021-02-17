let notesContainer = document.querySelector('section#notes_container');
			let sortBy = document.querySelector('#sort_notes');
			let notes = document.querySelectorAll('.note');
			let notes1 = document.getElementsByClassName('note');
			let titleContainer = document.querySelectorAll('.note-header');
			let titles = Array.from(titleContainer);
			let sortedTitles = [];
			let notes2 = Array.from(notes1);
			let notes3 = [];
			let compareNoteArray = [];
			let shareDeleteIcons = document.querySelectorAll('#shareDeleteIcon');



			for (shareDeleteIcon of shareDeleteIcons){

				shareDeleteIcon.children[0].title = 'share this note';
				shareDeleteIcon.children[1].title = 'delete this note';
				shareDeleteIcon.children[0].setAttribute('onclick', 'shareNote(this)');
				shareDeleteIcon.children[1].setAttribute('onclick', 'deleteNote(this)');

			}

			//Adds unique ID to each note
			notes2.forEach((note)=>{

				note.setAttribute('id', `note${notes2.indexOf(note)}`)

			});

			function shareNote(element){

				console.log('you just shared a note');
				console.log(element);

			}

			function deleteNote(element){

				console.log('you just deleted a note');
				console.log(element);
				if(window.confirm("Are you sure you want to delete this note?")){

					console.log(element.parentElement.parentElement.parentElement);
					console.log(element.parentElement.parentElement.parentElement.id);


				}

			}

			function sortTitles(arr1, arr2){

				let titles = []; let sortedNotesByTitle = [];
				for(let i = 0; i < arr1.length; i++){

					titles.push(arr1[i].firstElementChild.innerText);

				}

				console.log(titles);
				console.log(titles.length);

				titles.sort();

				console.log(titles);
				console.log(titles.length);
				console.log(typeof(titles[0]));

				for(let i=0; i < titles.length; i++){

					for(let j=0; j < titles.length; j++){

						if(arr2[j].firstElementChild.innerText == titles[i]){

							sortedNotesByTitle.push(arr2[j].innerHTML);
							break;

						}

					}

				}


				console.log(sortedNotesByTitle);
				console.log(sortedNotesByTitle.length);

				return sortedNotesByTitle;

			}


			//notes[0].innerHTML = 'hello';
			//console.log(notes[0]);
			//console.log(notes[0].children[2].children[0].innerText);

			//let dates = ['Sept 12 2019 5:11', 'Sept 12 2019 5:12', 'Sept 12 2019 5:13', 'Sept 12 2019 5:14', 'Sept 12 2019 5:15']
			let dates = []
			let dadates = document.querySelectorAll('section#notes_container .note .note-footer > span:first-of-type')

			//slicing the dates
			for(let date of dadates){

				let newDate = date.innerText.slice(0,8) + date.innerText.slice(10,-3)
				dates.push(newDate)

			}

			console.log(dates);

			//converting the dates
			for(let date of dates){

				dates[dates.indexOf(date)] = new Date(date);

			}

			console.log(dates);

			let dateCheck = [...dates];

			let timeArr = dates.map(date=>{return date.getTime()});
			//console.log(timeArr);

			/*function checkMinTime(arr){
				let dArr = [];
				if(arr){
					minValue = Math.min.apply(Math, arr)
					dArr.push(minValue);
					return checkMinTime(arr.shift());
				}
				else{
					return dArr;
				}

			}*/

			let sortedTimeArr = [];
			for(let i=timeArr.length; i > 0; i--){


				if(timeArr.length > 0){
					//console.log('timeArr.length ', timeArr.length);
					//console.log(timeArr);
					minValue = Math.min.apply(Math, timeArr);
					sortedTimeArr.push(minValue);
					timeArr.splice(timeArr.indexOf(minValue),1);

				}

				else{
					//console.log('DONE!!!');
				}

			}


			console.log('sortedTimeArr ',sortedTimeArr);



			// Arrange notes by title, date and category

			// Arrange date
			function sortByDate(arr1, arr2){
				let sortedNotesByDate = []
				for(let i= 0;i < arr1.length; i++){

					for(let j = 0;j < arr1.length; j++){

						let arr1Date = arr1[j].children[2].children[0].innerText.slice(0,8) + arr1[j].children[2].children[0].innerText.slice(10,-3)
						console.log(arr1Date);

						if(arr2[i] == new Date(arr1Date).getTime()){
							notes3[i] = arr1[j].innerHTML;
							sortedNotesByDate.push(arr1[j]);
							compareNoteArray.push(arr1[j]);
							//console.log('sorted');
							console.log('index ', i);
							console.log('INDEX ', j);
							console.log('arr2[i] ', arr2[i]);
							console.log('arr1[j] ', arr1[j]);
							console.log('arr1Date ', arr1Date);
							break;
						}

					}

				}
				console.log('sortedNotesByDate ', sortedNotesByDate);

				return sortedNotesByDate;

			}

			sortBy.addEventListener('change', function(event){

				sortByOptions = Array.from(sortBy.options)
				console.log(sortByOptions);


				for(let option of sortByOptions){

					if(option.selected){


						if(option.value === 'date'){

							console.log(option.value);
							let sortedNotesArray = Array.from(sortByDate(notes, sortedTimeArr));
							console.log(sortedNotesArray);
							console.log(sortedNotesArray[0]);

							for(let i = 0;i < notes3.length; i++){

								notes[i].innerHTML = notes3[i];
								console.log(sortedNotesArray[i]);

							}




						}

						if(option.value === 'category'){

							console.log(option.value)

						}

						if(option.value === 'title'){

							console.log(option.value);
							let sortedNotesByTitle = sortTitles(notes, notes2);
							console.log(sortedNotesByTitle);
							console.log(sortedNotesByTitle.length);
							for(let i=0; i < sortedNotesByTitle.length; i++){

								notes[i].innerHTML = sortedNotesByTitle[i];

							}

						}

					}

				}

			});