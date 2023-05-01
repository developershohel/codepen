jQuery('#save-button').on('click', function () {
    const htmlVal = HtmlEditor.getValue()
    const encodeHtml = he.encode(htmlVal)
    const cssVal = CssEditor.getValue()
    const encodeCss = he.encode(cssVal)
    const jsVal = JsEditor.getValue()
    console.log(jsVal)
    const encodeJs = he.encode(jsVal)
    const penId = jQuery('[data-pen-id]').attr('data-pen-id')
    const penType = jQuery('#pen-type').val()
    const penSlug = jQuery('#input-pen-slug').val()
    const penUserId = jQuery('[data-pen-user-id]').val()
    const login_user_id = jQuery('[data-user-id]').val()
    const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    const spinner = jQuery(this).children('.fa-spinner')
    let data = {}

    if (htmlVal.trim() !== '') {
        const formatHtmlVal = formatCode(htmlVal, 'html')
        HtmlEditor.setValue(formatHtmlVal)
        data['html_value'] = formatHtmlVal.replace(/\n/g, "\\n")
    }
    if (cssVal.trim() !== '') {
        const formatCssVal = formatCode(cssVal, 'css')
        CssEditor.setValue(formatCssVal)
        data['css_value'] = formatCssVal.replace(/\n/g, "\\n")
    }
    if (jsVal.trim() !== '') {
        const formatJsVal = formatCode(jsVal, 'babel')
        JsEditor.setValue(formatJsVal)
        const newJsEditorValue = JsEditor.getValue()
        if (/'/g.test(newJsEditorValue)) {
            console.log(newJsEditorValue)
            const newJsValue = newJsEditorValue.replace(/'/g, '"')
            console.log(newJsValue)
            const inlineValue = string_replace(newJsValue)
            console.log(inlineValue)
            data['js_value'] = inlineValue.replace(/\n/g, "\\n")
        } else{
            const inlineValue = string_replace(newJsEditorValue)
            data['js_value'] = inlineValue.replace(/\n/g, "\\n")
        }
    }
    if (penId.trim() !== '') {
        data['pen_id'] = penId
        jQuery.ajax({
            url: '/pen/save/',
            method: 'post',
            data: data,
            beforeSend: function () {
                spinner.css({display: 'block'})
            },
            success: function (data) {
                let getResult = JSON.stringify(data)
                let result = JSON.parse(getResult)
                if (result['status'] === true) {
                    if (penType.trim() !== '' && penType === 'new-pen') {
                        window.location.href = penSlug;
                    }
                } else {
                    alertCentered("Something Went to wrong. Pen didn't save. Please try again")
                }
            },
            complete: function () {
                spinner.css({display: 'none'})
            },
            error: function (xhr, status, error) {
                alertCentered("Something Went to wrong. Pen didn't save. Please try again")
                console.log(error);
            }
        })
    } else {
        alertCentered("Something Went to wrong. Pen didn't save. Please try again")
    }
});

function pen_live_edit() {
    const htmlVal = HtmlEditor.getValue();
    const cssVal = CssEditor.getValue();
    const jsVal = JsEditor.getValue();
    const penId = jQuery('#pen_details').val()
    const penPlatform = jQuery('#pen-platform').val()
    const pen_new_slug = jQuery('#pen-new-slug').val()
    const pen_old_slug = jQuery('#pen-old-slug').val()
    const penUserId = jQuery('[data-pen-username]').attr('data-pen-username')
    const login_user_id = jQuery('[data-user-id]').val()
    const updateArea = jQuery('.output-area');
    const pen_link = jQuery('#pen-preview-link').val()

    let data = {}

    if (htmlVal.trim() !== '') {
        data['html_value'] = htmlVal
    }
    if (cssVal.trim() !== '') {
        data['css_value'] = cssVal
    }
    if (jsVal.trim() !== '') {
        data['js_value'] = jsVal
    }
    if (penId.trim() !== '') {
        data['pen_id'] = penId
    }
    if (penPlatform.trim() !== '') {
        data['platform'] = penPlatform
    }
    if (pen_new_slug.trim() !== '') {
        data['new_pen_slug'] = pen_new_slug
    }
    if (pen_old_slug.trim() !== '') {
        data['old_pen_slug'] = pen_old_slug
    }

    if (penUserId.trim() !== '') {
        data['pen_user'] = penUserId
    }
    let htmlTemplate = `
    <!DOCTYPE html>
    <html lang=en>
    <head>
    <meta charset=UTF-8>
    <meta content="width=device-width, initial-scale=1.0" name=viewport>
    <title>{{ pens.get.pen_title }} - VMS Editor</title>
    <meta content="index, follow, max-snippet:-1, max-video-preview:-1, max-image-preview:large" name=robots>
    <link rel=canonical href=https://vmseditor.com/>
    <meta content=en_US property=og:locale>
    <meta content=website property=og:type>
    <meta content="{{ pens.get.pens.get.pen_title }} - VMS Editor" property=og:title>
    <meta content=https://vmseditor.com/ property=og:url>
    <meta content="VMS Editor" property=og:site_name>
    <meta content=summary_large_image name=twitter:card>
    <meta content="{{ pens.get.pen_title }} - VMS Editor" name=twitter:title>
    <meta content="{{ pens.get.pen_description }}" name=twitter:description>
    <meta content="Written by" name=twitter:label1>
    <meta content=developershohel name=twitter:data1>
    <meta content="Time to read" name=twitter:label2>
    <meta content="2 minutes" name=twitter:data2>
    <link rel=wlwmanifest href=https://vmseditor.com/static/icon/wlwmanifest.xml type=application/wlwmanifest+xml>
    <link rel=icon href=https://vmseditor.com/static/icon/cropped-android-chrome-512x512-1-1-32x32.png sizes=32x32>
    <link rel=icon href=https://vmseditor.com/static/icon/cropped-android-chrome-512x512-1-1-192x192.png sizes=192x192>
    <link rel=apple-touch-icon href=https://vmseditor.com/static/icon/cropped-android-chrome-512x512-1-1-180x180.png>
    <style id="editor-css">${cssVal}</style>
    </head>
    <body>
    ${htmlVal}
    <script id="editor-js">${jsVal}</script>
    </body>
    </html>
    `
    let preview = jQuery('#preview')
    preview.attr('srcdoc', htmlTemplate)
}

function alertCentered(message) {
    // Create a div to hold the message
    var $div = jQuery("<div>").text(message);

    // Set the CSS styles to center the div on the screen
    $div.css({
        "position": "fixed",
        "top": "50%",
        "left": "50%",
        "transform": "translate(-50%, -50%)",
        "background-color": "white",
        "padding": "20px",
        "border": "1px solid black",
        "border-radius": "5px",
        "box-shadow": "0px 0px 10px rgba(0, 0, 0, 0.5)",
        "z-index": "9999"
    });

    // Add the div to the body and show the alert
    jQuery("body").append($div);
    setTimeout(function () {
        $div.fadeOut(500, function () {
            jQuery(this).remove();
        });
    }, 3000); // hide the message after 3 seconds
}