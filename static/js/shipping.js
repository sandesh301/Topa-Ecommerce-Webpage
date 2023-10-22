function phoneInfo() {
    alert('Enter your home phone number in the following format: (xxx) xxx-xxxx.');
}

function check(shippingForm) {

    var valid = true,
        error = new Image(),
        fnError = document.getElementById('firstName_error'),
        lnError = document.getElementById('lastName_error'),
        adError = document.getElementById('streetAddress_error'),
        ctError = document.getElementById('city_error'),
        stError = document.getElementById('state_error'),
        zcError = document.getElementById('zipCode_error'),
        e1Error = document.getElementById('emailAddress1_error'),
        e2Error = document.getElementById('emailAddress2_error'),
        pnError = document.getElementById('phoneNumber_error'),
        errorIcon = '<img src="img/cross.png" alt="Error" width="22" height="22" />';
    validEmail = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{3})+$/;
    error.src = 'img/cross.png';


    //first name
    if (document.shippingForm.firstName.value === '') {
        //Empty first name.
        firstName.style.backgroundColor = "#CD9B9B";
        fnError.innerHTML = errorIcon + " Please complete name.";
        valid = false;
    } else {
        firstName.style.backgroundColor = "#ffffff";
        fnError.innerHTML = '';
    }

    //last name
    if (document.shippingForm.lastName.value === '') {
        //Empty last name.
        lastName.style.backgroundColor = "#CD9B9B";
        fnError.innerHTML = errorIcon + " Please complete name.";
        valid = false;
    } else {
        lastName.style.backgroundColor = "#ffffff";
        fnError.innerHTML = '';
    }

    //address 1
    if (document.shippingForm.streetAddress1.value === '') {
        //Empty street address.	
        streetAddress1.style.backgroundColor = "#CD9B9B";
        adError.innerHTML = errorIcon + " Please enter address.";
        valid = false;
    } else {
        streetAddress1.style.backgroundColor = "#ffffff";
        adError.innerHTML = '';
    }

    //city
    if (document.shippingForm.city.value === '') {
        //Empty city.
        city.style.backgroundColor = "#CD9B9B";
        ctError.innerHTML = errorIcon + " Please enter a city.";
        valid = false;
    } else {
        city.style.backgroundColor = "#ffffff";
        ctError.innerHTML = '';
    }

    //state
    if (document.shippingForm.state.selectedIndex === 0) {
        //Empty state.
        state.style.backgroundColor = "#CD9B9B";
        stError.innerHTML = errorIcon + " Please select a state.";
        valid = false;
    } else {
        state.style.backgroundColor = "#ffffff";
        stError.innerHTML = '';
    }

    //zip code
    if (document.shippingForm.zipCode.value === '') {
        //Empty zip code.
        zipCode.style.backgroundColor = "#CD9B9B";
        zcError.innerHTML = errorIcon + " Please enter a zip code.";
        valid = false;
    } else if (isNaN(document.shippingForm.zipCode.value)) {
        //Zip code must be numeric.
        zipCode.style.backgroundColor = "#CD9B9B";
        zcError.innerHTML = errorIcon + " Zip code must be numeric.";
        valid = false;
    } else if (document.shippingForm.zipCode.value.length < 5) {
        //Zip less than 5.
        areaCode.style.backgroundColor = "#CD9B9B";
        zcError.innerHTML = errorIcon + " Zip code must be 5 characters.";
        valid = false;
    } else {
        zipCode.style.backgroundColor = "#ffffff";
        zcError.innerHTML = '';
    }

    //emails
    if (document.shippingForm.emailAddress1.value === '') {
        //Empty email
        emailAddress1.style.backgroundColor = "#CD9B9B";
        e1Error.innerHTML = errorIcon + " Please enter email.";
        valid = false;
    } else {
        emailAddress1.style.backgroundColor = "#ffffff";
        e1Error.innerHTML = '';
    }

    if (document.shippingForm.emailAddress2.value === '') {
        //Empty confirm email.
        emailAddress2.style.backgroundColor = "#CD9B9B";
        e2Error.innerHTML = errorIcon + " Please confirm email.";
        valid = false;
    } else {
        emailAddress2.style.backgroundColor = "#ffffff";
        e2Error.innerHTML = '';
    }

    if (document.shippingForm.emailAddress1.value !== document.shippingForm.emailAddress2.value) {
        //Emails do not match.
        emailAddress1.style.backgroundColor = "#CD9B9B";
        emailAddress2.style.backgroundColor = "#CD9B9B";
        e1Error.innerHTML = errorIcon + " Emails do not match.";
        valid = false;
    } else if (emailAddress1.value.match(validEmail)) {
        //Valid email
        emailAddress1.style.backgroundColor = "#ffffff";
        emailAddress2.style.backgroundColor = "#ffffff";
        e1Error.innerHTML = '';
        e2Error.innerHTML = '';
    } else {
        emailAddress1.style.backgroundColor = "#CD9B9B";
        emailAddress2.style.backgroundColor = "#CD9B9B";
        e1Error.innerHTML = errorIcon + " Invalid email format.";
    }

    //phone
    if (document.shippingForm.areaCode.value === '' || document.shippingForm.phoneNumber1.value === '' || document.shippingForm.phoneNumber2.value === '') {
        //Empty fields.
        areaCode.style.backgroundColor = "#CD9B9B";
        phoneNumber1.style.backgroundColor = "#CD9B9B";
        phoneNumber2.style.backgroundColor = "#CD9B9B";
        pnError.innerHTML = errorIcon + " Please complete phone number.";
        valid = false;
    } else if (document.shippingForm.areaCode.value.length < 3 || document.shippingForm.phoneNumber1.value.length < 3 || document.shippingForm.phoneNumber2.value.length < 4) {
        //Number check
        areaCode.style.backgroundColor = "#CD9B9B";
        phoneNumber1.style.backgroundColor = "#CD9B9B";
        phoneNumber2.style.backgroundColor = "#CD9B9B";
        pnError.innerHTML = errorIcon + " Invalid format. (###-###-####)";
        valid = false;
    } else if (isNaN(document.shippingForm.areaCode.value) || isNaN(document.shippingForm.phoneNumber1.value) || isNaN(document.shippingForm.phoneNumber2.value)) {
        //Area code must be numeric.
        areaCode.style.backgroundColor = "#CD9B9B";
        phoneNumber1.style.backgroundColor = "#CD9B9B";
        phoneNumber2.style.backgroundColor = "#CD9B9B";
        pnError.innerHTML = errorIcon + " Phone number must be numeric.";
        valid = false;
    } else {
        areaCode.style.backgroundColor = "#ffffff";
        phoneNumber1.style.backgroundColor = "#ffffff";
        phoneNumber2.style.backgroundColor = "#ffffff";
        pnError.innerHTML = '';
    }

    //redirect
    if (valid === true) {
        alert("You entered: \nName: " + lastName.value + ", " + firstName.value + "\nAddress: " + streetAddress1.value + " " + streetAddress2.value + ", " +
            city.value + ", " + state.value + " " + zipCode.value + "\nEmail: " + emailAddress1.value +
            "\nPhone: (" + areaCode.value + ") " + phoneNumber1.value + " - " + phoneNumber2.value);
        window.location = "return.html";
    } else {
        return false;
    }
}