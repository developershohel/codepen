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

    // End jquery
})

function scrollH(e) {
    e.preventDefault()
    e = window.event || e;
    let delta = Math.max(-1, Math.min(1, (e.whellDelta || -e.details)));
    document.querySelector('.pens').scrollLeft -= (delta * 40);
}

if (document.querySelector('.pens')) {
    document.querySelector('.pens').addEventListener('wheel', scrollH, false)
    document.querySelector('.pens').addEventListener('mousewheel', scrollH, false)
    document.querySelector('.pens').addEventListener('DOMMouseScroll', scrollH, false)
    document.querySelector('.pens').addEventListener('MozMousePixelScroll', scrollH, false)
}

function string_replace(value) {
    let replaceValue = value
    if (/\b's\b/g.test(replaceValue)) {
        replaceValue = replaceValue.replace(/\b's\b/g, "\\'s")
    } else if (/\b"s\b/g.test(replaceValue)) {
        replaceValue = replaceValue.replace(/\b"s\b/g, "\\'s")
    }

    if (/\b"d\b/g.test(replaceValue)) {
        replaceValue = replaceValue.replace(/\b"d\b/g, "\\'d")
    } else if (/\b'd\b/g.test(replaceValue)) {
        replaceValue = replaceValue.replace(/\b'd\b/g, "\\'d")
    }

    if (/\b"ll\b/g.test(replaceValue)) {
        replaceValue = replaceValue.replace(/\b"ll\b/g, "\\'ll")
    } else if (/\b'll\b/g.test(replaceValue)) {
        replaceValue = replaceValue.replace(/\b'll\b/g, "\\'ll")
    }
    if (/\b"re\b/g.test(replaceValue)) {
        replaceValue = replaceValue.replace(/\b"re\b/g, "\\'re")
    } else if (/\b're\b/g.test(replaceValue)) {
        replaceValue = replaceValue.replace(/\b're\b/g, "\\'re")
    }
    if (/\b"ve\b/g.test(replaceValue)) {
        replaceValue = replaceValue.replace(/\b"ve\b/g, "\\'ve")
    } else if (/\b've\b/g.test(replaceValue)) {
        replaceValue = replaceValue.replace(/\b've\b/g, "\\'ve")
    }
    if (/\b"m\b/g.test(replaceValue)) {
        replaceValue = replaceValue.replace(/\b"m\b/g, "\\'m")
    } else if (/\b'm\b/g.test(replaceValue)) {
        replaceValue = replaceValue.replace(/\b'm\b/g, "\\'m")
    }
    if (/\b"t\b/g.test(replaceValue)) {
        replaceValue = replaceValue.replace(/\b"t\b/g, "\\'t")
    } else if (/\b't\b/g.test(replaceValue)) {
        replaceValue = replaceValue.replace(/\b't\b/g, "\\'t")
    }
    return replaceValue
}