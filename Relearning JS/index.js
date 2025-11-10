let username;

// Method 1 of getting user input - through prompt window lmao
/*
username = window.prompt('Enter your username: ');
document.getElementById('myH1').textContent = `Hello there ${username}! Hope you're doing well.`
console.log(username) // just to check
*/

// Method 2: more professional using html textbox

let username2;
document.getElementById('button-1').onclick = function(){
    username2 = document.getElementById('user-input').value;
    console.log(username2) // to check
    document.getElementById('myH1').textContent = `Hello ${username2}!`
}








/*
console.log('HELLOOOOOOOOOO');
console.log(`these paranthesese used for this text are helpful for variables`)

/*
window.alert('THIS IS AN ALERT!');
window.alert('ANOTHER ALERT BROOOO!');

// yoooo wass uppp its a comment broskiii laposki lmao


document.getElementById('myH2').textContent = 'HELLO AGAIN';
document.getElementById('myP2').textContent = 'WASS UP LOL!';

///////////////////////////

let x = 123; 
console.log(x);

let fullName = 'Adeeb Haidari';
let student = true;

document.getElementById('1').textContent = 'SOME NEW REPLACED TEXT WITH JS';

let age = 17;
let price = 10.99;
let y = 'SOME RANDOM TEXT HERE'

console.log(age);
console.log(price);
console.log(`You are ${age} years old lmao`)
console.log(`The price of pizza rn is $${price}`)

console.log(typeof price); // outputs the data type!!!

console.log(`This variable has this value --> ${y} <-- and is a ${typeof y} data type!`)
*/
