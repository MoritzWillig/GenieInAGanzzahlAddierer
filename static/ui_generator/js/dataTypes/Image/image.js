function ImageDataType() {

}

ImageDataType.prototype = Object.create(DataType.prototype);

ImageDataType.prototype.generateGUIElement = function generateGUIElement(argument) {
    let filedrop = document.createElement("div");
    filedrop.classList.add("image_datatype");

    let placeholder = document.createElement("div");
    placeholder.innerHTML = "Drop picture or take a picture from the webcam view below.";
    placeholder.classList.add("image_datatype_placeholder");
    let progressbar = document.createElement("progress");
    progressbar.value = 100;
    let filechooser = document.createElement("input");
    filechooser.type = "file";
    filechooser.innerText = "Upload file";
    let capturebutton = document.createElement("button");
    capturebutton.innerText = "Capture image";

    filedrop.appendChild(placeholder);
    filedrop.appendChild(capturebutton);
    filedrop.appendChild(filechooser);
    filedrop.appendChild(document.createElement("br"));
    filedrop.appendChild(progressbar);


    let browserSupport = {
        draggable: 'draggable' in document.createElement('span'),
        formdata: !!window.FormData,
        progress: "upload" in new XMLHttpRequest()
    };

    function uploadFiles(session_name, name, files) {
        if (!browserSupport.formdata) {
            console.log("Form data not supported");
            //TODO notify user
        }
        let formData = new FormData();


        if (files.length !== 1) {
            console.log("Multiple files selected, but only a single file will be uploaded");
        }

        try {
            formData.append('file', files[i]);
        } catch (e) {
            throw e;
        }

        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/session/' + session_name + '/upload/' + name);
        xhr.onload = function (e) {
            if (progressbar) progressbar.value = progressbar.innerHTML = 100;
            var response = JSON.parse(this.response);
            if (response.success) {
                //onsuccess(response.filename);
                //TODO notify user
                console.log("upload successful");
            } else {
                alert(response.error);
            }
        };

        if (browserSupport.progress) {
            xhr.upload.onprogress = function (event) {
                if (event.lengthComputable) {
                    let progress = (event.loaded / event.total * 100 | 0);
                    if (progressbar) progressbar.value = progressbar.innerHTML = progress;
                }
            };
        }

        xhr.onreadystatechange = function () {
            if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                console.log(this.responseText); //TODO notify user
                result_form.innerHTML = this.responseText;
            }
        };

        xhr.send(formData);
    }


    // add drag and drop events
    if (browserSupport.draggable) {
        filedrop.ondragover = function () {
            this.addClass('hover');
            return false;
        };
        filedrop.ondragend = function () {
            this.removeClass('hover');
            return false;
        };
        filedrop.ondrop = function (e) {
            this.removeClass('hover');
            e.preventDefault();
            session_name = get_session_name();
            uploadFiles(session_name, argument.name, e.dataTransfer.files);
        };
    }

    // add change event for filechooser
    filechooser.onchange = function () {
        session_name = get_session_name();
        uploadFiles(session_name, argument.name, this.files);
    };

    // open file chooser on click
    filedrop.onclick = function (e) {
        if (e.target !== capturebutton) {
            filechooser.click();
        }
    };

    return filedrop;
};

ImageDataType.prototype.hasSimpleLayout = function hasSimpleLayout() {
    return false;
};