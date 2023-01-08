jQuery(document).ready(function ($) {
    const loginForm = $('#loginform')
    const signUpForm = $('#signup-form')
    if (loginForm.length > 0) {
        const username = loginForm.find('#username');
        const password = loginForm.find('#password');
        const rememberme = loginForm.find('.remember-me')
        const formSubmit = loginForm.find('#form-submit-button')
        let userVal = username.val()
        let userRegex = ''
        let userRegexVal = 0

        password.on('input', function () {
            password.attr('value', $(this).val())
        })
        username.on('input', function () {
            username.attr('value', $(this).val())
            userVal = $(this).val()
            userRegex = userVal
        })
        rememberme.on('click', function () {
            const checkbox = $(this).find('#checkbox');
            $(this).toggleClass('checked')
            checkbox.prop('checked', !checkbox.prop('checked'))
            if ($(this).hasClass('checked')) {
                $(this).find('i').removeClass('fa-circle').addClass('fa-circle-check')
            } else {
                $(this).find('i').removeClass('fa-circle-check').addClass('fa-circle')
            }
        })
        formSubmit.on('click', function () {
            const formError = username.parent().next('.form-error');
            userRegex = userVal.match(/\w/g)
            const emailRegex = userVal.match(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,5}$/g)
            if (userRegex) {
                userRegexVal = userRegex.length
            } else {
                userRegexVal = 0
            }
            if (!userVal) {
                if (formError.length > 0) {
                    username.parent().next('.form-error').html('<span class="error">Username din\'t empty</span>')
                } else {
                    username.parent().after(`<div class="form-error"><span class="error">Username din\'t empty</span></div>`)
                }
            } else {
                if (formError.length > 0) {
                    formError.empty()
                }
            }
            if (userVal && !userVal.match(/@/g) && userVal.length > userRegexVal) {
                if (formError.length > 0) {
                    username.parent().next('.form-error').html('<span class="error">Username only contain Letters, digits and _ only.</span>')
                } else {
                    username.parent().after(`<div class="form-error"><span class="error">Username only contain Letters, digits and _ only.</span></div>`)
                }
            } else {
                if (formError.length > 0) {
                    formError.empty()
                }
            }
            if (userVal && userVal.match(/@/g) && !emailRegex) {
                if (formError.length > 0) {
                    username.parent().next('.form-error').html('<span class="error">Invalid email address</span>')
                } else {
                    username.parent().after(`<div class="form-error"><span class="error">Invalid email address</span></div>`)
                }
            } else {
                if (formError.length > 0) {
                    formError.empty()
                }
            }
            if (!password.val()) {
                const formError = password.parent().next('.form-error');
                if (formError.length > 0) {
                    formError.html('<span class="error">Password din\'t empty </span>')
                } else {
                    password.parent().after('<div class="form-error"> <span class="error">Password din\'t empty </span></div>')
                }
            } else {
                const formError = password.parent().next('.form-error');
                if (formError.length > 0) {
                    formError.empty()
                }
            }
            if (!userVal || (userVal.match(/@/g) && !emailRegex) || !password || userVal.length > userRegexVal) {
                console.log("it's working")
                return false
            }
        });
    }


    if (signUpForm.length > 0) {
        const firstName = signUpForm.find('#first-name')
        const lastName = signUpForm.find('#lname')
        const userName = signUpForm.find('#username')
        const email = signUpForm.find('#email')
        const password = signUpForm.find('#password')
        const cPassword = signUpForm.find('#c-password')
        const agreement = signUpForm.find('.agreement-checkbox')

        agreement.find('input').on('change', function () {
            if ($(this).is(':checked')) {
                $(this).parent().find('i').removeClass('fa-check').addClass('fa-circle-check')
            } else {
                $(this).parent().find('i').removeClass('fa-circle-check').addClass('fa-circle')
            }
        })

        userName.on('input', function(){
            userName.attr('value', $(this).val())
            if(userName){
                $.ajax({
                    url: '/auth/user-validation',
                    method: 'post',
                    data: {
                        type: 'username',
                        user_value: $(this).val()
                    },
                    success: function(data){
                        console.log(data)
                    }
                })
            }
        })

        $('#first-name, #lname, #password, #c-password').on('input', function () {
            $(this).attr('value', $(this).val())
        })

        $('#signup-button').on('click', function () {
            if (!firstName.val()) {
                firstName.parent().next().html('<span class="error">First Name didn\'t empty</span>')
            } else {
                firstName.parent().next().empty()
            }

            if (!lastName.val()) {
                lastName.parent().next().html('<span class="error">Last Name didn\'t empty</span>')

            } else {
                lastName.parent().next().empty()
            }

            if (!userName.val()) {

                userName.parent().next().html('<span class="error">Username didn\'t empty</span>')

            } else if (userName.val() && userName.val().match(/\W/g)) {

                userName.parent().next().html('<span class="error">Username only contain Letters, digits and _ only.</span>')

            } else {
                userName.parent().next().empty()
            }
            if (!email.val()) {
                email.parent().next().html('<span class="error">Email didn\'t empty</span>')
            } else if (email.val() && !email.val().match(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,5}$/g)) {
                email.parent().next().html('<span class="error">Invalid email address</span>')

            } else {
                email.parent().next().empty()
            }
            if (!password.val()) {

                password.parent().next().html('<span class="error">Password didn\'t empty</span>')
            } else {
                password.parent().next().empty()
            }

            if (!cPassword.val()) {
                cPassword.parent().next().html('<span class="error">Confirm password didn\'t empty</span>')
            } else {
                cPassword.parent().next().empty()
            }

            if (password.val() && cPassword.val() && password.val() !== cPassword.val()) {
                cPassword.parent().next().html('<span class="error">Password didn\'t match</span>')
            } else {
                if(cPassword.val()){
                    cPassword.parent().next().empty()
                }
            }
            
            return false
        })

    }
})