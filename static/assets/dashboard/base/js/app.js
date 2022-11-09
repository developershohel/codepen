jQuery(document).ready(function ($) {
    $('.dashboard-top-menu').on('click', function () {
        $('.user-setting').slideToggle()
    })

    // Sub-Menu Current class
    if ($('.sub-menu').find('.current-child').length > 0) {
        $('.sub-menu').css({display: 'flex'}).parent().addClass('current')
    }
    // File upload
    const uploader = $('.media-uploader'),
        uploaderButton = uploader.find("#upload-button"),
        uploaderInput = uploader.find("#input-files"),
        uploadingError = $('.uploading-errors'),
        mediaList = $('.media-list');
    // uploaderButton.on('click', function () {
    //     uploaderInput.click()
    // })
    //
    uploaderInput.on("change", function (e) {
        let get_file = e.target.files;
        if (get_file.length > 0) {
            uploader.addClass("active");
            for (let i = 0; i < get_file.length; i++) {
                let file_name = get_file[i].name
                let file_size = get_file[i].size
                let fileExtension = get_extension(file_name)
                if (check_extension(fileExtension) === true) {
                    if (file_size > 10 * 1024 * 1024) {
                        uploadingError.parent().fadeIn()
                        let errorContent = `<div class="upload-error">
                        <span class="upload-error-filename">${file_name}</span>
                        <span class="upload-error-message">Sorry, your file exceeds the maximum upload size for this site.</span>
                        </div>`
                        uploadingError.append(errorContent)
                        return false
                    }
                } else {
                    uploadingError.parent().fadeIn()
                    let errorContent = `<div class="upload-error">
                        <span class="upload-error-filename">${file_name}</span>
                        <span class="upload-error-message">Sorry, you are not allowed to upload this file type.</span>
                        </div>`
                    uploadingError.append(errorContent)
                    return false
                }
            }
            uploadAndTrackFiles(get_file)
        }
    });

    uploader.on("drop", (event) => {
        event.preventDefault();
        $(this).css({borderColor: 'var(--button-primary)'})
        let file = event.originalEvent.dataTransfer.files;
        if (file.length > 0) {
            uploader.addClass("active");
            for (let i = 0; i < file.length; i++) {
                let file_name = file[i].name
                let file_size = file[i].size
                let fileExtension = get_extension(file_name)
                if (file_size.length < 100) {
                    if (check_extension(fileExtension) === true) {
                        if (file_size > 10 * 1024 * 1024) {
                            uploadingError.parent().fadeIn()
                            let errorContent = `<div class="upload-error">
                        <span class="upload-error-filename">${file_name}</span>
                        <span class="upload-error-message">Sorry, your file exceeds the maximum upload size for this site.</span>
                        </div>`
                            uploadingError.append(errorContent)
                            return false
                        }
                    } else {
                        uploadingError.parent().fadeIn()
                        let errorContent = `<div class="upload-error">
                        <span class="upload-error-filename">${file_name}</span>
                        <span class="upload-error-message">Sorry, you are not allowed to upload this file type.</span>
                        </div>`
                        uploadingError.append(errorContent)
                        return false
                    }
                } else {
                    uploadingError.parent().fadeIn()
                    let errorContent = `<div class="upload-error">
                        <span class="upload-error-filename">${file_name}</span>
                        <span class="upload-error-message">Sorry, your file name is too large for upload. File name must be less than 100 character</span>
                        </div>`
                    uploadingError.append(errorContent)
                    return false
                }
            }
            uploadAndTrackFiles(file)
        }
    });
})

const uploaderContainer = document.querySelector('.media-uploader')

if (uploaderContainer !== null) {
    uploaderContainer.addEventListener("dragover", (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploaderContainer.classList.add("active");
        uploaderContainer.style.borderColor = 'var(--button-primary)'
    });

    uploaderContainer.addEventListener("dragleave", (e) => {
        e.preventDefault()
        e.stopPropagation();
        uploaderContainer.classList.add("active");
        uploaderContainer.style.borderColor = 'var(--content-bg)'
    });
}
const penDetailsWheel = document.querySelector('.pens, .comments');
const penBodyDetailsWheel = document.querySelector('.pens tbody, .comments tbody');
if (penDetailsWheel !== null) {
    penDetailsWheel.addEventListener('wheel', function (e) {
        const race = 50; // How many pixels to scroll
        if (e.deltaY > 0) // Scroll right
            penDetailsWheel.scrollTop += race;
        else // Scroll left
            penDetailsWheel.scrollTop -= race;
        e.preventDefault();
    });
}

function get_extension(file) {
    let file_name = `${file}`
    return file_name.split('.').pop()
}

function check_extension(file) {
    const file_ext = document.querySelector('#input-files').getAttribute('accept')
    const pure_ext = file_ext.replaceAll('.', '')
    return !!pure_ext.includes(file);
}

const mediaList = document.querySelector('.media-list')
const uploaderButton = document.querySelector('#upload-button')
const uploaderInput = document.querySelector('#input-files')

if (uploaderButton !== null) {
    uploaderButton.addEventListener('click', function () {
        uploaderInput.click()
    })
}

const uploadFiles = (() => {
    const defaultOptions = {
        url: '/dashboard/upload-file/',
        onProgress() {
        },
        onComplete() {
        }
    }
    const uploadFile = (file, options) => {
        const req = new XMLHttpRequest()
        const formData = new FormData()
        formData.append('file', file)
        req.open('POST', options.url, true)
        req.onload = (e) => options.onComplete(e, file)
        req.upload.onprogress = (e) => options.onProgress(e, file)
        req.send(formData);
    }
    return (files, options) => {
        [...files].forEach((file => uploadFile(file, {...defaultOptions, ...options})))
    }
})()

const uploadAndTrackFiles = (() => {
    const FILE_STATUS = {
        PENDING: 'pending',
        UPLOADING: 'uploading',
        PAUSED: 'paused',
        COMPLETE: 'completed',
        FAILED: 'failed',
    }
    const files = new Map()
    const setFileElement = file => {
        let file_ext = get_extension(file.name)
        const img_ext = ['gif', 'jpg', 'jpe', 'jpeg', 'png', 'webp', 'svg']
        const video_ext = ['mp4', 'mpeg', 'm1v', 'mpa', 'mpe', 'mpg', 'mov', 'qt', 'webm', 'avi', 'movie']
        const media_content = document.createElement('li')
        media_content.className = 'media-file'
        if (img_ext.includes(file_ext)) {
            media_content.innerHTML = `<div class="file-preview">
                            <div class="thumbnail">
                                <div class="file">
                                    <img src="" class="icon"  alt="">
                                </div>
                            </div>
                        </div>
                        <button type="button" class="select"><span class="material-symbols-outlined">check_box_outline_blank</span><input type="checkbox" value="filename" hidden></button>
                        <div class="progress-bar-section">
                            <div class="progress-bar"><span class="progress"></span></div>
                        </div>
                        <input type="hidden" id="file-url" name="file_url" value="">`
        } else if (video_ext.includes(file_ext)) {
            media_content.innerHTML = `<div class="file-preview">
                            <div class="thumbnail">
                                <div class="file">
                                    <i class="fa-solid fa-file-video"></i>
                                </div>
                                <div class="filename"></div>
                            </div>
                        </div>
                        <button type="button" class="select"><span class="material-symbols-outlined">check_box_outline_blank</span><input type="checkbox" value="filename" hidden></button>
                        <div class="progress-bar-section">
                            <div class="progress-bar"><span class="progress"></span></div>
                        </div>
                        <input type="hidden" id="file-url" name="file_url" value="">`
        } else if (file_ext === 'txt') {
            media_content.innerHTML = `<div class="file-preview">
                            <div class="thumbnail">
                                <div class="file">
                                    <span class="material-symbols-outlined">description</span>
                                </div>
                                <div class="filename"></div>
                            </div>
                        </div>
                        <button type="button" class="select"><span class="material-symbols-outlined">check_box_outline_blank</span><input type="checkbox" value="filename" hidden></button>
                        <div class="progress-bar-section">
                            <div class="progress-bar"><span class="progress"></span></div>
                        </div>
                        <input type="hidden" id="file-url" name="file_url" value="">`
        } else if (file_ext === 'json') {
            media_content.innerHTML = `<div class="file-preview">
                            <div class="thumbnail">
                                <div class="file">
                                    <span class="material-symbols-outlined">data_object</span>
                                </div>
                                <div class="filename"></div>
                            </div>
                        </div>
                        <button type="button" class="select"><span class="material-symbols-outlined">check_box_outline_blank</span><input type="checkbox" value="filename" hidden></button>
                        <div class="progress-bar-section">
                            <div class="progress-bar"><span class="progress"></span></div>
                        </div>
                        <input type="hidden" id="file-url" name="file_url" value="">`
        } else if (file_ext === 'xml') {
            media_content.innerHTML = `<div class="file-preview">
                            <div class="thumbnail">
                                <div class="file">
                                    <span class="material-symbols-outlined">code</span>
                                </div>
                                <div class="filename"></div>
                            </div>
                        </div>
                        <button type="button" class="select"><span class="material-symbols-outlined">check_box_outline_blank</span><input type="checkbox" value="filename" hidden></button>
                        <div class="progress-bar-section">
                            <div class="progress-bar"><span class="progress"></span></div>
                        </div>
                        <input type="hidden" id="file-url" name="file_url" value="">`
        }
        files.set(file, {
            status: 'pending',
            size: file.size,
            percentage: 0,
            media_content
        })
        mediaList.prepend(media_content)
    }
    const updateFileElement = fileObj => {
        const progressBarSection = fileObj.media_content.children[2]
        const progressBar = progressBarSection.firstElementChild.firstElementChild
        requestAnimationFrame(() => {
            progressBarSection.classList.add('progressing')
            progressBar.style.width = fileObj.percentage + '%';
        })
    }

    const onProgress = (e, file) => {
        const fileObj = files.get(file)
        fileObj.status = FILE_STATUS.UPLOADING
        fileObj.percentage = e.loaded / e.total * 100
        updateFileElement(fileObj)
    }

    const onComplete = (e, file) => {
        let file_ext = get_extension(file.name)
        const img_ext = ['gif', 'jpg', 'jpe', 'jpeg', 'png', 'webp', 'svg']
        const resFile = JSON.parse(e.target.response)
        const fileObj = files.get(file)
        const fileImg = fileObj.media_content.children[0].firstElementChild.firstElementChild.firstElementChild
        const progressBarSection = fileObj.media_content.children[2]
        const progressBar = progressBarSection.firstElementChild.firstElementChild
        const fileUrl = fileObj.media_content.children[3]
        if (!img_ext.includes(file_ext)) {
            const fileName = fileObj.media_content.children[0].firstElementChild.children[1]
            if (resFile.file_name.length > 25) {
                fileName.textContent = resFile.file_name.toString().slice(0, 25) + '....' + file_ext
            } else {
                fileName.textContent = resFile.file_name
            }
        } else {
            fileImg.setAttribute('src', resFile.file_url)
        }
        fileUrl.value = [{'id': resFile.file_id, 'file_url': resFile.file_url}]
        progressBarSection.classList.remove('progressing')
        progressBar.setAttribute('style', 'width: 0')
    }
    return (uploadedFiles) => {
        [...uploadedFiles].forEach(setFileElement)
        uploadFiles(uploadedFiles, {
            url: '/dashboard/upload-file/',
            onComplete,
            onProgress,
        })
    }
})()