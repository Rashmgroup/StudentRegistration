function showOtherCourseField() {
    const courseDropdown = document.getElementById("Course");
    const otherCourseField = document.getElementById("otherCourseField");
    if (courseDropdown.value === "Other") {
        otherCourseField.style.display = "block";
    } else {
        otherCourseField.style.display = "none";
    }
}
     // Step navigation functions
     function nextStep(currentStep) {
        const current = document.getElementById(`step-${currentStep}`);
        const next = document.getElementById(`step-${currentStep + 1}`);

        // Validate the current step before moving to the next
        if (validateStep(currentStep)) {
            current.classList.remove('active');
            next.classList.add('active');
        }
    }

    function prevStep(currentStep) {
        const current = document.getElementById(`step-${currentStep}`);
        const prev = document.getElementById(`step-${currentStep - 1}`);

        current.classList.remove('active');
        prev.classList.add('active');
    }

    // Validate each step
    function validateStep(step) {
        let isValid = true;
        const inputs = document.querySelectorAll(`#step-${step} input, #step-${step} select`);
        const errorMessages = [];

        inputs.forEach(input => {
            // Check if the field is required and not empty
            if (input.hasAttribute('required') && !input.value.trim()) {
                isValid = false;
                input.style.borderColor = 'red';
                errorMessages.push(`${input.previousElementSibling.innerText} is required.`);
            } else {
                input.style.borderColor = '';
            }

            // Email validation (if input type is email)
            if (input.type === 'email' && input.value) {
                const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
                if (!emailPattern.test(input.value)) {
                    isValid = false;
                    input.style.borderColor = 'red';
                    errorMessages.push(`Please enter a valid email address.`);
                }
            }

            // Phone number validation (if input type is phone)
            if (input.id === 'Phone' || input.id === 'Whatsapp' || input.id === 'GuardianPhone') {
                const phonePattern = /^[0-9]{10}$/;
                if (input.value && !phonePattern.test(input.value)) {
                    isValid = false;
                    input.style.borderColor = 'red';
                    errorMessages.push(`Please enter a valid 10-digit phone number for ${input.placeholder}.`);
                }
            }

            // Signature validation
            if (input.id === 'Sign' && input.value) {
                const signaturePattern = /^[a-zA-Z\s]+$/;
                if (!signaturePattern.test(input.value)) {
                    isValid = false;
                    input.style.borderColor = 'red';
                    errorMessages.push(`Signature should contain only letters and spaces.`);
                }
            }
        });

        // Show error messages if any validation fails
        if (!isValid) {
            alert(errorMessages.join("\n"));
        }

        return isValid;
    }

    // Full form validation on submit
    function validateForm() {
        const form = document.getElementById('registrationForm');
        const email = document.getElementById('Email').value;
        const phone = document.getElementById('Phone').value;
        const whatsapp = document.getElementById('Whatsapp').value;
        const guardianPhone = document.getElementById('GuardianPhone').value;
        const name = document.getElementById('Name').value;
        const fname = document.getElementById('Fname').value;

        // Email validation
        const emailPattern = /^[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com|outlook\.com)$/;
        if (!emailPattern.test(email)) {
            alert("Please enter a valid email address from Gmail, Yahoo, or Outlook.");
            return false;
        }

        // Phone and WhatsApp number validation (10 digits)
        const phonePattern = /^[0-9]{10}$/;
        if (!phonePattern.test(phone)) {
            alert("Please enter a valid 10-digit phone number for Phone.");
            return false;
        }

        if (!phonePattern.test(whatsapp)) {
            alert("Please enter a valid 10-digit phone number for WhatsApp.");
            return false;
        }

        if (!phonePattern.test(guardianPhone)) {
            alert("Please enter a valid 10-digit phone number for Guardian's Phone.");
            return false;
        }

        // Check if Guardian's phone and Student's phone are the same
        if (phone === guardianPhone) {
            alert("Guardian's phone number cannot be the same as the student's phone number.");
            return false;
        }

        // Name validation (should not contain numbers or special characters)
        const namePattern = /^[a-zA-Z\s]+$/;
        if (!namePattern.test(name)) {
            alert("Please enter a valid name (only letters and spaces).");
            return false;
        }

        // Father's Name validation (should not contain numbers or special characters)
        if (!namePattern.test(fname)) {
            alert("Father's Name should contain only letters and spaces.");
            return false;
        }

        // Signature validation (only letters and spaces allowed)
        const signature = document.getElementById('Sign').value;
        const signaturePattern = /^[a-zA-Z\s]+$/;
        if (!signaturePattern.test(signature)) {
            alert("Signature should contain only letters and spaces.");
            return false;
        }

        // All other validations (Step-wise validation)
        for (let step = 1; step <= 4; step++) {
            if (!validateStep(step)) {
                return false;
            }
        }

        // Generate registration number if form is valid
        generateRegistrationNumber();
        return true;
    }

   