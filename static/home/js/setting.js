jQuery(function ($) {
    $('.pen-setting').on('click', function () {
        $('#setting-options').slideToggle()
    })

    $('.toggle').on("click", function (e) {
        $(this).toggleClass('on')
        let inputToggle = $(this).siblings('input[type="checkbox"]');
        if (inputToggle.is(":checked")) {
            inputToggle.checked = false;
            inputToggle.val('off')
            inputToggle.attr('data-button-value', '')
        } else {
            inputToggle.checked = true
            inputToggle.val('on')
            inputToggle.attr('data-button-value', 'Auto')
        }

        inputToggle = $(this).siblings('input[type="checkbox"]');
        const inputToggleVal = inputToggle.val()
        let fieldValue = null
        if (inputToggleVal === 'on') {
            fieldValue = 1
        } else {
            fieldValue = 0
        }

        if (inputToggleVal.trim() !== '') {
            $.ajax({
                url: '/setting/update/',
                method: "post",
                data: {
                    setting_name: inputToggle.attr('data-setting-name'),
                    field_name: inputToggle.attr('data-field-name'),
                    field_value: fieldValue
                },
                beforeSend: function () {
                    inputToggle.next('label').css({'pointer-events': 'none', opacity: 0.7})
                },
                success: function (data) {
                    let getResult = JSON.stringify(data)
                    let result = JSON.parse(getResult)
                    if (result['status'] === true) {
                        const toggleTargetId = inputToggle.attr('data-target-id')
                        if (toggleTargetId === '10') {
                            const buttonTargetId = $(`button[data-target-id="${toggleTargetId}"]`)
                            if (buttonTargetId.text().trim() === 'Auto Run') {
                                buttonTargetId.text('Run')
                            } else {
                                buttonTargetId.text('Auto Run')
                            }

                        } else if (toggleTargetId === '20') {
                            const buttonTargetId = $(`button[data-target-id="${toggleTargetId}"]`)
                            if (buttonTargetId.text().trim() === 'Auto Save') {
                                buttonTargetId.text('Save')
                            } else {
                                buttonTargetId.text('Auto Save')
                            }
                        }
                    } else {
                        alertCentered("Something Went to wrong. Pen didn't save. Please try again")
                    }
                },
                complete: function () {
                    inputToggle.next('label').css({'pointer-events': 'auto', opacity: 1})
                },
                error: function (xhr, status, error) {
                    alertCentered("Something Went to wrong. Pen didn't save. Please try again")
                    console.log(error);
                }
            })
        }
    });

    const editorContentWrap = $('.editor-content-wrap')
    const editorContentWrapWidth = editorContentWrap.width()
    console.log(editorContentWrapWidth)
    const editorControlResizer = $(".editor-control-resizer");
    const editorCssContentHeader = $('.css-editor-header');
    const editorJsContentHeader = $('.js-editor-header');

    let isDragging = false;
    let currentX;
    let initialPosition;
    let currentY;
    let initialX;
    let initialY;
    let xOffset = 0;
    let yOffset = 0;

    // Event listener for mousedown
    editorControlResizer.mousedown(function (e) {
        initialX = e.clientX - xOffset;
        initialPosition = initialX
        console.log(initialPosition)

        if (e.target === this) {
            isDragging = true;
        }
    });

    editorCssContentHeader.mousedown(function (e) {
        initialY = e.clientY - xOffset;
        console.log(initialPosition)

        if (e.target === this) {
            isDragging = true;
        }
    });

    editorCssContentHeader.mousemove(function (e) {
        console.log(e.clientY)
    })

    // Event listener for mousemove
    $(document).mousemove(function (e) {
        if (isDragging) {
            e.preventDefault();

            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY
            console.log(currentX)
            console.log(currentY)

            xOffset = currentX;

            if (-100 <= currentX <= 150) {
                setEditorWidth(currentX);
            } else if (-50 <= currentY <= 50) {
                setEditorHeight(currentY)
            } else {
                return false;
            }
        }
    });

    // Event listener for mouseup
    $(document).mouseup(function (e) {
        initialX = currentX;
        initialY = currentY
        isDragging = false;
    });

    function setEditorWidth(xPos) {
        editorContentWrap.width(editorContentWrapWidth + (xPos))
    }

    function setEditorHeight(YPos) {

    }

    // End jQuery
})