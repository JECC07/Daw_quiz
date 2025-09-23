const nombreUsuarioEl = document.querySelector('#nombre_usuario');
const emailEl = document.querySelector('#email');
const passwordEl = document.querySelector('#contraseña');
const confirmPasswordEl = document.querySelector('#confirmar-contraseña');
const rolEl = document.querySelector('#rol');
const fechaNacimientoEl = document.querySelector('#fecha_nacimiento');

const form = document.querySelector('#signup');

const isRequired = value => value === '' ? false : true;
const isBetween = (length, min, max) => length < min || length > max ? false : true;
const isEmailValid = (email) => {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
};
const isPasswordSecure = (password) => {
    const re = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
    return re.test(password);
};

const showError = (input, message) => {
    const formField = input.parentElement;
    formField.classList.remove('success');
    formField.classList.add('error');
    const error = formField.querySelector('small');
    error.textContent = message;
};

const showSuccess = (input) => {
    const formField = input.parentElement;
    formField.classList.remove('error');
    formField.classList.add('success');
    const error = formField.querySelector('small');
    error.textContent = '';
}

const checkNombreUsuario = () => {
    let valid = false;
    const min = 3, max = 25;
    const username = nombreUsuarioEl.value.trim();

    if (!isRequired(username)) {
        showError(nombreUsuarioEl, 'Nombre de usuario no debe estar vacío.');
    } else if (!isBetween(username.length, min, max)) {
        showError(nombreUsuarioEl, `Nombre de usuario debe contener entre ${min} y ${max} caracteres.`)
    } else {
        showSuccess(nombreUsuarioEl);
        valid = true;
    }
    return valid;
}

const checkEmail = () => {
    let valid = false;
    const email = emailEl.value.trim();
    if (!isRequired(email)) {
        showError(emailEl, 'Email no puede estar vacío');
    } else if (!isEmailValid(email)) {
        showError(emailEl, 'Email no es válido.')
    } else {
        showSuccess(emailEl);
        valid = true;
    }
    return valid;
}

const checkPassword = () => {
    let valid = false;
    const password = passwordEl.value.trim();
    if (!isRequired(password)) {
        showError(passwordEl, 'Contraseña no puede estar vacía.');
    } else if (!isPasswordSecure(password)) {
        showError(passwordEl, 'Contraseña debe presentar una minúscula, mayúscula, número y caracter especial');
    } else {
        showSuccess(passwordEl);
        valid = true;
    }
    return valid;
};

const checkConfirmPassword = () => {
    let valid = false;
    const confirmPassword = confirmPasswordEl.value.trim();
    const password = passwordEl.value.trim();

    if (!isRequired(confirmPassword)) {
        showError(confirmPasswordEl, 'Por favor ingrese la contraseña');
    } else if (password !== confirmPassword) {
        showError(confirmPasswordEl, 'La confirmación de contraseña sin éxito');
    } else {
        showSuccess(confirmPasswordEl);
        valid = true;
    }
    return valid;
};

const checkRol = () => {
    let valid = false;
    if (!isRequired(rolEl.value)) {
        showError(rolEl, 'Debe seleccionar un rol.');
    } else {
        showSuccess(rolEl);
        valid = true;
    }
    return valid;
};

const checkFechaNacimiento = () => {
    let valid = false;
    if (!isRequired(fechaNacimientoEl.value)) {
        showError(fechaNacimientoEl, 'Debe ingresar una fecha de nacimiento.');
    } else {
        showSuccess(fechaNacimientoEl);
        valid = true;
    }
    return valid;
};

const debounce = (fn, delay = 500) => {
    let timeoutId;
    return (...args) => {
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        timeoutId = setTimeout(() => {
            fn.apply(null, args)
        }, delay);
    };
};

form.addEventListener('input', debounce(function (e) {
    switch (e.target.id) {
        case 'nombre_usuario':
            checkNombreUsuario();
            break;
        case 'email':
            checkEmail();
            break;
        case 'contraseña':
            checkPassword();
            break;
        case 'confirmar-contraseña':
            checkConfirmPassword();
            break;
        case 'rol':
            checkRol();
            break;
        case 'fecha_nacimiento':
            checkFechaNacimiento();
            break;
    }
}));

form.addEventListener('submit', function (e) {
    e.preventDefault();

    let isNombreUsuarioValid = checkNombreUsuario(),
        isEmailValid = checkEmail(),
        isPasswordValid = checkPassword(),
        isConfirmPasswordValid = checkConfirmPassword(),
        isRolValid = checkRol(),
        isFechaNacimientoValid = checkFechaNacimiento();

    let isFormValid = isNombreUsuarioValid &&
        isEmailValid &&
        isPasswordValid &&
        isConfirmPasswordValid &&
        isRolValid &&
        isFechaNacimientoValid;

    if (isFormValid) {
        form.submit();
    }
});