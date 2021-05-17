// Username variables
const usernameField = document.querySelector('#usernameField') //selector by id
const feedBackArea = document.querySelector('.usernameFeedBackArea') //selector by class
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput')
// Email variables
const emailField = document.querySelector('#emailField')
const emailFeedBackArea = document.querySelector('.emailFeedBackArea')
// Show password
const showPassword = document.querySelector('.showPassword')
const passwordField = document.querySelector('#passwordField')
const passwordToggle=(e)=>{
    if (showPassword.textContent === "SHOW") {
        passwordField.setAttribute("type", "text");
        showPassword.textContent = "HIDE";
      } else {
        passwordField.setAttribute("type", "password");
        showPassword.textContent = "SHOW";
      }
};
showPassword.addEventListener('click', passwordToggle);
// Register button
const submitBtn= document.querySelector('.submit-btn')


// Email Validation
emailField.addEventListener('keyup', (e)=>{
    const emailVal = e.target.value;
    emailField.classList.remove('is-invalid')
    emailFeedBackArea.textContent = null
    if(emailVal.length > 0){
        fetch('/authentication/validate-email/',{
            body:JSON.stringify({email:emailVal}),
            method:'POST',
        })
            .then(res=>res.json())
            .then(data=>{
                // console.log('data', data)
                if (data.email_error){
                    submitBtn.disabled = true;
                    emailField.classList.add('is-invalid')
                    emailFeedBackArea.style.display = "block";
                    emailFeedBackArea.innerHTML= `<p>${data.email_error}</p>`
                } else {
                    submitBtn.removeAttribute("disabled");
                    emailField.classList.remove('is-invalid')
                    emailFeedBackArea.style.display = "none";
                }
            })
    }
});


// Username Validation
usernameField.addEventListener('keyup', (e)=> {
    const usernameVal = e.target.value;
    usernameField.classList.remove('is-invalid', 'is-valid')
    usernameSuccessOutput.textContent= null
    feedBackArea.style.display = "none";
    submitBtn.removeAttribute("disabled");
    if(usernameVal.length > 0){
         setTimeout(() => {
             fetch('/authentication/validate-username/', {
                 body: JSON.stringify({username: usernameVal}),
                 method: 'POST',
             })
                 .then(res => res.json())
                 .then(data => {
                     // console.log('data', data);
                     if (data.username_error) {
                         submitBtn.disabled = true;
                         usernameField.classList.add('is-invalid')
                         feedBackArea.style.display = "block";
                         usernameSuccessOutput.textContent = null
                         feedBackArea.innerHTML = `<p>${data.username_error}</p>`
                     } else {
                         usernameField.classList.remove('is-invalid')
                         usernameField.classList.add('is-valid')
                         feedBackArea.style.display = "none";
                         usernameSuccessOutput.textContent = 'Username valid'
                         submitBtn.removeAttribute("disabled");
                     }
                 });
         }, 100);
    }
});