jQuery(document).ready(function ($) {
    $('.user-avatar').on('click', function () {
        $(this).next().slideToggle()
    })
})