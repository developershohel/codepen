// const input = document.getElementById("select");
//
// function selectTheme() {
//     const theme = input.options[input.selectedIndex].textContent;
//     editor.setOption("theme", theme);
//     location.hash = "#" + theme;
// }
//
// const choice = (location.hash && location.hash.slice(1)) ||
//     (document.location.search &&
//         decodeURIComponent(document.location.search.slice(1)));
// if (choice) {
//     input.value = choice;
//     editor.setOption("theme", choice);
// }
// CodeMirror.on(window, "hashchange", function () {
//     const theme = location.hash.slice(1);
//     if (theme) {
//         input.value = theme;
//         selectTheme();
//     }
// });
//
// (function (mod) {
//     if (typeof exports == "object" && typeof module == "object") // CommonJS
//         mod(require("../../lib/codemirror"));
//     else if (typeof define == "function" && define.amd) // AMD
//         define(["../../lib/codemirror"], mod);
//     else // Plain browser env
//         mod(CodeMirror);
// })
//
// (function (CodeMirror) {
//     "use strict";
//
//     CodeMirror.registerHelper("lint", "html", function (text) {
//         let found = [], message;
//         if (!window.HTMLHint) return found;
//         const messages = HTMLHint.verify(text, ruleSets);
//         for (let i = 0; i < messages.length; i++) {
//             message = messages[i];
//             const startLine = message.line - 1, endLine = message.line - 1, startCol = message.col - 1,
//                 endCol = message.col;
//             found.push({
//                 from: CodeMirror.Pos(startLine, startCol),
//                 to: CodeMirror.Pos(endLine, endCol),
//                 message: message.message,
//                 severity: message.type
//             });
//         }
//         return found;
//     });
// });
//
// // ruleSets for HTMLLint
// var ruleSets = {
//     "tagname-lowercase": true,
//     "attr-lowercase": true,
//     "attr-value-double-quotes": true,
//     "doctype-first": false,
//     "tag-pair": true,
//     "spec-char-escape": true,
//     "id-unique": true,
//     "src-not-empty": true,
//     "attr-no-duplication": true
// };
//


// function live_update() {
//     const htmlVal = HtmlEditor.getValue();
//     const cssVal = CssEditor.getValue();
//     const jsVal = JsEditor.getValue();
//     const previewFrame = jQuery('#preview');
//     console.log(previewFrame)
//     const previewDocument = previewFrame.contents();
//     previewDocument[0].open();
//     previewDocument[0].write(html_platform_output());
//     previewDocument[0].close();
//     const previewBody = previewDocument.find('body');
//     const previewCss = previewDocument.find('#editor-css');
//     console.log(previewBody)
//     console.log(previewCss)
//     if (cssVal) {
//         previewCss.html(cssVal);
//     }
//     if (previewBody) {
//         previewBody.html(htmlVal)
//         previewBody.append('<script id="editor-js"></script>');
//     }
//     const previewJs = previewDocument.find('#editor-js');
//     console.log(previewJs)
//     if (jsVal) {
//         previewJs.html(jsVal);
//     }
// }

// Add a beforeunload event listener to the window

let interval = null;
let delay = null;
let hintTimeout = null

function live_update() {
    pen_live_edit()
}

function formatCode(code, parser) {
    try {
        const formatter = prettier.format(code, {
            parser: parser,
            singleQuote: false,
            jsxSingleQuote: false,
            plugins: prettierPlugins,
        });
        return formatter
    } catch (e) {
        console.error(e);
        return code;
    }
}

jQuery('#js-formatting').on('click', function () {
    formatCode(JsEditor.getValue(), 'babel');
})

function updateCss() {
    const cssVal = CssEditor.getValue();
    const updateArea = jQuery('.output-area');
    const pen_link = jQuery('#pen-preview-link').val()
}

function updateJs() {
    const jsVal = JsEditor.getValue();
    const updateArea = jQuery('.output-area');
    const pen_link = jQuery('#pen-preview-link').val()
}

const HtmlEditor = CodeMirror(document.getElementById('html-editor'), {
    lineNumbers: true,
    styleActiveLine: true,
    mode: 'htmlmixed',
    theme: 'the-matrix',
    smartIndent: true,
    keyMap: 'sublime',
    lineWrapping: true,
    scrollbarStyle: 'overlay',
    inputStyle: 'textarea',
    showCursorWhenSelecting: true,
    undoDepth: 500,
    autofocus: true,
    autocorrect: true,
    matchBrackets: true,
    autoCloseBrackets: true,
    showTrailingSpace: true,
    toggleComment: true,
    autoCloseTags: true,
    newlineAndIndent: false,
    whenClosing: "",
    emptyAttrs: false,
    foldGutter: true,
    gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"],
    lint: true,
    hint: true,
    electricChars: true,
    hintOptions: {
        theme: "idea",
        hint: CodeMirror.hint.html,
        completeSingle: false
    },
    extraKeys: {
        "F11": function (cm) {
            cm.setOption("fullScreen", !cm.getOption("fullScreen"));
        },
        "Esc": function (cm) {
            if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
        },
        "Ctrl-Space": function (cm) {
            if (cm.state.completionActive || cm.getDoc().getCursor()["ch"] < 1) return CodeMirror.Pass;
            cm.execCommand("autocomplete");
        },
    },
});

HtmlEditor.on('change', function (cm, change) {
    clearInterval(delay)
    delay = setTimeout(function () {
        live_update()
    }, 1500)
});

HtmlEditor.on("keypress", function (cm, event) {
    let isTagging = false;

    document.addEventListener("keypress", function (event) {
        if (event.key === "<") {
            isTagging = true;
        } else if (event.key === ">") {
            isTagging = false;
        }
        if (isTagging === true) {
            const codeMirrorHints = jQuery('.CodeMirror-hints')
            HtmlEditor.showHint()
            clearTimeout(hintTimeout);
            hintTimeout = setTimeout(function () {
                codeMirrorHints.css({display: 'none'});
            }, 2000);
        }
    });
});

emmetCodeMirror(HtmlEditor);

const CssEditor = CodeMirror(document.getElementById('css-editor'), {
    lineNumbers: true,
    mode: 'css',
    theme: 'the-matrix',
    smartIndent: true,
    indentUnit: 4,
    electricChars: true,
    tabSize: 4,
    keyMap: 'sublime',
    lineWrapping: true,
    scrollbarStyle: 'overlay',
    inputStyle: 'textarea',
    showCursorWhenSelecting: true,
    undoDepth: 500,
    autocorrect: true,
    matchBrackets: true,
    autoCloseBrackets: true,
    showTrailingSpace: true,
    toggleComment: true,
    autoCloseTags: true,
    autoComplete: true,
    foldGutter: true,
    gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"],
    lint: true,
    hint: true,
    hintOptions: {
        theme: "idea",
        hint: CodeMirror.hint.css,
        completeSingle: false
    },
    extraKeys: {
        "F11": function (cm) {
            cm.setOption("fullScreen", !cm.getOption("fullScreen"));
        },
        "Esc": function (cm) {
            if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
        },
        "Ctrl-Space": function (cm) {
            if (cm.state.completionActive || cm.getDoc().getCursor()["ch"] < 1) return CodeMirror.Pass;
            cm.execCommand("autocomplete");
        },
    }
});


CssEditor.on('change', function (cm, change) {
    clearInterval(delay)
    delay = setTimeout(function () {
        live_update()
    }, 1500)
});

CssEditor.on("keydown", function (cm, e) {
    let isTagging = false;
    if (e.key === "Enter") {
        isTagging = true;
    } else if (e.key === ";" || e.key === ':') {
        isTagging = false;
    }

    if (isTagging === true) {
        setTimeout(function () {
            const codeMirrorHints = jQuery('.CodeMirror-hints')
            CssEditor.showHint()
            clearTimeout(hintTimeout);
            hintTimeout = setTimeout(function () {
                codeMirrorHints.css({display: 'none'});
            }, 2000);
        }, 1000)
    }
});

emmetCodeMirror(CssEditor, {
    syntax: 'css' // "xml", "xsl", "jsx", "css", "scss", "less", "stylus", "pug", "slim", "haml"
});

const JsEditor = CodeMirror(document.getElementById('js-editor'), {
    lineNumbers: true,
    mode: 'text/javascript',
    theme: 'the-matrix',
    indentUnit: 4,
    smartIndent: true,
    keyMap: 'sublime',
    lineWrapping: true,
    scrollbarStyle: 'overlay',
    inputStyle: 'textarea',
    showCursorWhenSelecting: true,
    undoDepth: 500,
    autocorrect: true,
    matchBrackets: true,
    autoCloseBrackets: true,
    showTrailingSpace: true,
    toggleComment: true,
    autoCloseTags: true,
    foldGutter: true,
    gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"],
    lint: {
        "eslint": true, // use eslint instead of jshint
        "options": {
            "esversion": 6 // set esversion to 6 for ES6 support
        }
    },
    hint: true,
    addToConsole: true,
    hintOptions: {
        theme: "idea",
        hint: CodeMirror.hint.javascript,
        completeSingle: false
    },
    extraKeys: {
        "F11": function (cm) {
            cm.setOption("fullScreen", !cm.getOption("fullScreen"));
        },
        "Esc": function (cm) {
            if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
        },
        "Ctrl-Space": function (cm) {
            if (cm.state.completionActive || cm.getDoc().getCursor()["ch"] < 1) return CodeMirror.Pass;
            cm.execCommand("autocomplete");
        },
    }
});
JsEditor.on('change', function (cm, change) {
    clearInterval(delay)
    delay = setTimeout(function () {
        live_update()
    }, 1500)
});

JsEditor.on("keypress", function (cm, e) {
    let isTagging = false;
    isTagging = e.key !== ";";
    if (isTagging === true) {
        const codeMirrorHints = jQuery('.CodeMirror-hints')
        JsEditor.showHint()
        clearTimeout(hintTimeout);
        hintTimeout = setTimeout(function () {
            codeMirrorHints.css({display: 'none'});
        }, 1000);
    }
});

emmetCodeMirror(JsEditor, {
    syntax: 'jsx' // "xml", "xsl", "jsx", "css", "scss", "less", "stylus", "pug", "slim", "haml"
});

function handleInput(event) {
    if (event.key === 'Enter') {
        const input = event.target.value.trim(); // trim the input value
// Execute the entered command
        executeCommand(input)
        event.target.value = '';
    }
}


function executeCommand(command) {
    const output = jQuery('#console-output');
    const previewIframe = document.getElementById('preview');
    const previewIframeJquery = jQuery('#preview');
    let result = ''
    let newCommand = ''
    const iframeBody = previewIframe.contentWindow.document.getElementsByTagName('body')[0]
    console.log(iframeBody)
    const cloneIframe = iframeBody.cloneNode(true)
    console.log(cloneIframe)
    const testId = cloneIframe.querySelectorAll('#test')
    console.log(testId)
    try {
        let commandString = "'" + command + "'"
        if (commandString.match(/jQuery|\$/i)) {
            newCommand = command.replace(/jQuery|\$/i, 'find');
            let iFrameCommand = 'previewIframeJquery.contents().' + newCommand
            result = eval(iFrameCommand);
        } else if (commandString.match(/document/i)) {

            // let iFrameCommand = 'previewIframe.contentWindow.' + command;
            // result = eval(iFrameCommand);
            // // const resultClone = result.cloneNode(true)
            // if (result.nodeType === Node.ELEMENT_NODE) {
            //     console.log('The result is an element node');
            //     const cloneResult = result.cloneNode(true)
            //     output.appendChild(cloneResult)
            // } else if (result.nodeType === Node.TEXT_NODE) {
            //     console.log('The result is a text node');
            // } else {
            //     console.log('The result is another type of node');
            //
            // }
            // console.log(`nodeType: ${result.nodeType}`)
        } else {
            result = eval(command);
        }
        console.log(typeof result)
        const randonNumber = Math.floor(Math.random() * 100)
        output.append(`<div class="console-command"><pre>${command}</pre></div>`)

        if (result.length > 0) {
            if (result === '[object Object]') {
                console.log('you are right')
            }
            output.append(`<div class="console-code" id="console-code-${randonNumber}"></div>`)
            CodeMirror(document.getElementById(`console-code-${randonNumber}`), {
                value: JSON.stringify(result, null, 2),
                lineNumbers: false,
                mode: 'application/json',
                readOnly: true,
                theme: 'the-matrix',
                indentUnit: 2,
                smartIndent: true,
                lineWrapping: true,
                scrollbarStyle: 'overlay',
            })
        } else {
            if (typeof result !== 'object') {
                output.append(`<div class="console-code"><pre>${result}</pre></div>`)
            } else {
                output.append(`<div class="console-code" id="console-code-${randonNumber}">${result}</div>`)
                CodeMirror(document.getElementById(`console-code-${randonNumber}`), {
                    value: JSON.stringify(result, null, 2),
                    lineNumbers: false,
                    mode: 'text/html',
                    readOnly: true,
                    theme: 'the-matrix',
                    indentUnit: 2,
                    smartIndent: true,
                    lineWrapping: true,
                    scrollbarStyle: 'overlay',
                })
            }

        }

    } catch (error) {
        output.append(`<div class="console-command error-command"><pre>${error}</pre></div>`);
        output.append(`<div class="console-command error-command"><pre>${result}</pre></div>`);
    }
}

// const consoleInput = document.getElementById('console-input');
// consoleInput.addEventListener('keyup', handleInput);
