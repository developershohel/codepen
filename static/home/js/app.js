jQuery(document).ready(function ($) {
    $('.user-avatar').on('click', function () {
        $(this).next().slideToggle()
    })

    $('.main-menu').find('.current-child').children('.fa-angle-down').on('click', function () {
        $(this).next('.sub-menu').toggleClass('expanded')
        $(this).next('.sub-menu').slideToggle()
        if ($(this).next('.sub-menu').hasClass('expanded')) {
            $(this).css({transform: 'rotate(180deg)'})
        } else {
            $(this).css({transform: 'rotate(0deg)'})
        }
    });
    $('.fa-ellipsis').on('click', function () {
        $(this).next('ul').fadeToggle()
    })
    $('.pen-header-author-image').on('click', function () {
        $(this).next('.main-menu-wrap').slideToggle().addClass('expanded')
    })
})

function scrollH(e) {
    e.preventDefault()
    e = window.event || e;
    let delta = Math.max(-1, Math.min(1, (e.whellDelta || -e.details)));
    document.querySelector('.pens').scrollLeft -= (delta * 40);
    console.log(delta)
}

if (document.querySelector('.pens')) {
    document.querySelector('.pens').addEventListener('wheel', scrollH, false)
    document.querySelector('.pens').addEventListener('mousewheel', scrollH, false)
    document.querySelector('.pens').addEventListener('DOMMouseScroll', scrollH, false)
    document.querySelector('.pens').addEventListener('MozMousePixelScroll', scrollH, false)
}
