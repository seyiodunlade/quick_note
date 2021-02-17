console.log('IN validateSignup AND WORKING');

let formToValidate = document.querySelector('form');
let emailFieldToValidate = formToValidate.elements.email;
let usernameFieldToValidate = formToValidate.elements.username;
let passwordField1ToValidate = formToValidate.elements.password1;
let passwordField2ToValidate = formToValidate.elements.password2;
let phonenumberToValidate = formToValidate.elements.phonenumber.value;
let lastnameToValidate = formToValidate.elements.lastname.value;
let firstnameToValidate = formToValidate.elements.firstname.value;
let countryToValidate = formToValidate.elements.country.value;

console.log(form.elements);