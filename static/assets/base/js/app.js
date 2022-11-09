jQuery(document).ready(function ($) {
    $('.user-avatar').on('click', function () {
        $(this).next().slideToggle()
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
