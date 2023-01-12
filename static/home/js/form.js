jQuery(document).ready(function ($) {
    const loginForm = $('#loginform')
    const signUpForm = $('#signup-form')
    const changePassword = $('#change-password')
    const errorColor = '#eb3730'
    const successColor = '#75DAFFFF'
    const whiteColor = '#ffffff'
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
        const formHelper = signUpForm.find('.helper-list').children();
        const agreement = signUpForm.find('.agreement-checkbox')
        let user_exit = ''
        let email_exit = ''
        let agreement_status = ''

        agreement.find('input').on('change', function () {
            if ($(this).is(':checked')) {
                agreement_status = true
                agreement.removeClass('error')
                agreement.css({color: whiteColor})
                agreement.find('a').css({color: successColor})
                agreement.find('i').css({color: successColor})
                $(this).parent().find('i').removeClass('fa-check').addClass('fa-circle-check')
            } else {
                agreement_status = false
                agreement.addClass('error')
                agreement.css({color: errorColor})
                agreement.find('a').css({color: errorColor})
                agreement.find('i').css({color: errorColor})
                $(this).parent().find('i').removeClass('fa-circle-check').addClass('fa-circle')
            }
        })
        userName.on('input', function () {
            userName.attr('value', $(this).val())
            if (userName.val() && userName.val().match(/\W/g)) {
                userName.css({borderColor: errorColor})
                userName.parent().next().html('<span class="error">Username only contain Letters, digits and _ only.</span>')
            } else if (userName.val() && userName.val().length < 3) {
                userName.css({borderColor: errorColor})
                userName.parent().next().html('<span class="error">The Username length must be greater than or equal 3</span>')
            } else {
                userName.css({borderColor: successColor})
                userName.parent().next().empty()
                $.ajax({
                    url: '/auth/user-validation',
                    method: 'post',
                    data: {
                        type: 'username',
                        user_value: $(this).val()
                    },
                    success: function (data) {
                        let getResult = JSON.stringify(data)
                        let result = JSON.parse(getResult)
                        user_exit = result['user_exit']
                        if (user_exit === true) {
                            userName.css({borderColor: errorColor})
                            userName.parent().next().html('<span class="error">Username already exits</span>')
                        } else {
                            userName.css({borderColor: successColor})
                            userName.parent().next().empty()
                        }
                    }
                })
            }
        })
        email.on('input', function () {
            email.attr('value', $(this).val())
            if (email.val() && !email.val().match(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,5}$/g)) {
                email.css({borderColor: errorColor})
                email.parent().next().html('<span class="error">Invalid email address</span>')
            } else {
                email.css({borderColor: successColor})
                email.parent().next().empty()
                $.ajax({
                    url: '/auth/user-validation',
                    method: 'post',
                    data: {
                        type: 'email',
                        user_value: $(this).val()
                    },
                    success: function (data) {
                        let getResult = JSON.stringify(data)
                        let result = JSON.parse(getResult)
                        email_exit = result['email_exit']
                        if (email_exit === true) {
                            email.parent().next().html('<span class="error">Email already exits</span>')
                        } else {
                            email.parent().next().empty()
                        }
                    }
                })
            }
        })

        password.on('input', function () {
            password.attr('value', $(this).val())
            let passwordVal = password.val()
            if (!passwordVal){
                password.css({borderColor: errorColor})
            }
            if (password.val()) {
                const matchCapLetter = passwordVal.match(/[A-Z]/g)
                const matchSmLetter = passwordVal.match(/[a-z]/g)
                const matchSymbol = passwordVal.match(/[!@#$%&*.()_-]/g)

                if (passwordVal.length > 8) {
                    formHelper.eq(0).css({color: successColor})
                } else {
                    formHelper.eq(0).css({color: errorColor})
                }
                if (matchCapLetter && matchSmLetter && matchCapLetter.length >= 1 && matchSmLetter.length >= 1) {
                    formHelper.eq(1).css({color: successColor})
                } else {
                    formHelper.eq(1).css({color: errorColor})
                }
                if (matchSymbol && matchSymbol.length >= 1) {
                    formHelper.eq(2).css({color: successColor})
                } else {
                    formHelper.eq(2).css({color: errorColor})
                }
                if (!password.val().match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%&*.()_-])[A-Za-z\d!@#$%&.*()_-]{8,32}$/g)) {
                    formHelper.parent().closest('.form-helper').css({display: 'flex'})
                } else {
                    formHelper.parent().closest('.form-helper').css({display: 'none'})
                    password.css({borderColor: successColor})
                }
            }
        })

        $('#first-name, #lname, #password, #c-password').on('input', function () {
            $(this).attr('value', $(this).val())
        })

        $('#signup-button').on('click', function () {
            if (!firstName.val()) {
                firstName.css({borderColor: errorColor})
                firstName.parent().next().html('<span class="error">First Name didn\'t empty</span>')
            } else {
                firstName.css({borderColor: successColor})
                firstName.parent().next().empty()
            }

            if (!lastName.val()) {
                lastName.css({borderColor: errorColor})
                lastName.parent().next().html('<span class="error">Last Name didn\'t empty</span>')
            } else {
                lastName.css({borderColor: successColor})
                lastName.parent().next().empty()
            }

            if (!userName.val()) {
                userName.css({borderColor: errorColor})
                userName.parent().next().html('<span class="error">Username didn\'t empty</span>')
            } else if (userName.val() && userName.val().match(/\W/g)) {
                userName.css({borderColor: errorColor})
                userName.parent().next().html('<span class="error">Username only contain Letters, digits and _ only.</span>')
            } else if (user_exit === true) {
                userName.css({borderColor: errorColor})
                userName.parent().next().html('<span class="error">Username already exits</span>')
            } else if (userName.val() && userName.val().length < 3) {
                userName.css({borderColor: errorColor})
                userName.parent().next().html('<span class="error">The Username length must be greater than or equal 3</span>')
            } else {
                userName.css({borderColor: successColor})
                userName.parent().next().empty()
            }
            if (!email.val()) {
                email.css({borderColor: errorColor})
                email.parent().next().html('<span class="error">Email didn\'t empty</span>')
            } else if (email.val() && !email.val().match(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,5}$/g)) {
                email.css({borderColor: errorColor})
                email.parent().next().html('<span class="error">Invalid email address</span>')
            } else if (email_exit === true) {
                email.css({borderColor: errorColor})
                email.parent().next().html('<span class="error">Email already exits</span>')
            } else {
                email.css({borderColor: successColor})
                email.parent().next().empty()
            }
            if (!password.val()) {
                password.css({borderColor: errorColor})
                password.parent().next('.form-error').html('<span class="error">Password didn\'t empty</span>')
            } else if (!password.val().match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%&*.()_-])[A-Za-z\d!@#$%&.*()_-]{8,32}$/g)) {
                password.css({borderColor: errorColor})
                formHelper.parent().closest('.form-helper').css({display: 'flex'})
            }else {
                password.css({borderColor: successColor})
                password.parent().next('.form-error').empty()
                formHelper.parent().closest('.form-helper').css({display: 'none'})
            }
            if (!cPassword.val()) {
                cPassword.css({borderColor: errorColor})
                cPassword.parent().next().html('<span class="error">Confirm password didn\'t empty</span>')
            } else {
                cPassword.css({borderColor: successColor})
                cPassword.parent().next().empty()
            }

            if (password.val() && cPassword.val() && password.val() !== cPassword.val()) {
                password.css({borderColor: errorColor})
                cPassword.css({borderColor: errorColor})
                cPassword.parent().next().html('<span class="error">Password didn\'t match</span>')
            } else {
                password.css({borderColor: successColor})
                cPassword.css({borderColor: successColor})
                if (cPassword.val()) {
                    cPassword.parent().next().empty()
                }
            }
            if (agreement_status === false || !agreement.find('input').is(':checked')) {
                agreement.addClass('error')
                agreement.css({color: errorColor})
                agreement.find('a').css({color: errorColor})
                agreement.find('i').css({color: errorColor})
            } else {
                agreement.removeClass('error')
                agreement.css({color: whiteColor})
                agreement.find('a').css({color: successColor})
                agreement.find('i').css({color: successColor})
            }
            if (!firstName.val() || !lastName.val() || !userName.val() || userName.val().match(/\W/g) || user_exit === true || !email.val() || !email.val().match(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,5}$/g) || email_exit === true || !password.val() || !cPassword.val() || password.val() !== cPassword.val() || !password.val().match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%&*.()_-])[A-Za-z\d!@#$%&.*()_-]{8,32}$/g) || agreement_status === false) {
                return false
            }
        })
    }

    
    if (changePassword.length > 0) {
        const password = changePassword.find('#password')
        const cPassword = changePassword.find('#cpassword')
        const formHelper = changePassword.find('.helper-list').children()
        password.on('input', function () {
            password.attr('value', $(this).val())
            let passwordVal = password.val()
            if (password.val()) {
                const matchCapLetter = passwordVal.match(/[A-Z]/g)
                const matchSmLetter = passwordVal.match(/[a-z]/g)
                const matchSymbol = passwordVal.match(/[!@#$%&*.()_-]/g)
                if (passwordVal.length > 8) {
                    formHelper.eq(0).css({color: successColor})
                } else {
                    formHelper.eq(0).css({color: errorColor})
                }
                if (matchCapLetter && matchSmLetter && matchCapLetter.length >= 1 && matchSmLetter.length >= 1) {
                    formHelper.eq(1).css({color: successColor})
                } else {
                    formHelper.eq(1).css({color: errorColor})
                }
                if (matchSymbol && matchSymbol.length >= 1) {
                    formHelper.eq(2).css({color: successColor})
                } else {
                    formHelper.eq(2).css({color: errorColor})
                }
                if (!password.val().match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%&*.()_-])[A-Za-z\d!@#$%&.*()_-]{8,32}$/g)) {
                    console.log('password not match')
                    formHelper.parent().closest('.form-helper').css({display: 'flex'})
                } else {
                    console.log('password match')
                    formHelper.parent().closest('.form-helper').css({display: 'none'})
                }
            }
        })
        $('.form-submit').find('button').on('click', function () {
            if (!password.val()) {
                password.css({borderColor: errorColor})
                password.parent().next('.form-error').html('<span class="error">Password didn\'t empty</span>')
            } else {
                password.css({borderColor: successColor})
                password.parent().next('.form-error').empty()
            }
            if (!password.val().match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%&*.()_-])[A-Za-z\d!@#$%&.*()_-]{8,32}$/g)) {
                password.css({borderColor: errorColor})
                formHelper.parent().closest('.form-helper').css({display: 'flex'})
            } else {
                formHelper.parent().closest('.form-helper').css({display: 'none'})
            }
            if (!cPassword.val()) {
                cPassword.css({borderColor: errorColor})
                cPassword.parent().next().html('<span class="error">Confirm password didn\'t empty</span>')
            } else {
                cPassword.css({borderColor: successColor})
                cPassword.parent().next().empty()
            }

            if (password.val() && cPassword.val() && password.val() !== cPassword.val()) {
                password.css({borderColor: errorColor})
                cPassword.css({borderColor: errorColor})
                cPassword.parent().next().html('<span class="error">Password didn\'t match</span>')
            } else {
                password.css({borderColor: successColor})
                cPassword.css({borderColor: successColor})
                if (cPassword.val()) {
                    cPassword.parent().next().empty()
                }
            }

            return false
        })
    }
})