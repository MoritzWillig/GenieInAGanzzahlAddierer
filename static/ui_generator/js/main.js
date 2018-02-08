param_form = undefined;
result_form = undefined;

request_fields = [];


const $ = function (q) {
    return document.querySelector(q);
};

// hasClass, addClass and removeClass polyfills
Element.prototype.hasClass = Element.prototype.hasClass || function (className) {
    return (' ' + this.className + ' ').indexOf(' ' + className + '') !== -1;
};
Element.prototype.addClass = Element.prototype.addClass || function (className) {
    if (!this.hasClass(className)) this.className += ' ' + className;
    return this;
};
Element.prototype.removeClass = Element.prototype.removeClass || function (className) {
    this.className = this.className.toLowerCase().replace(className.toLowerCase(), '');
    return this;
};

//AJAX

function formatParams(params) {
    if (params === undefined) {
        return "";
    }

    return "?" + Object
        .keys(params)
        .map(function (key) {
            return key + "=" + encodeURIComponent(params[key])
        })
        .join("&");
}


function perform_ajax(url, args, request_type, parse_json) {
    parse_json = !!parse_json;
    return new Promise(function(fulfill, reject) {
        let xhttp = new XMLHttpRequest();

        xhttp.onreadystatechange = function () {
            if (this.readyState === XMLHttpRequest.DONE) {
                if (this.status === 200) {
                    let response = this.responseText;

                    if (parse_json) {
                        try {
                            response = JSON.parse(this.responseText);
                        } catch(e) {
                            reject(e);
                        }
                    }

                    fulfill(response);
                } else {
                    reject(this.responseText);
                }
            }
        };

        if (request_type.toLowerCase() === "get") {
            console.log(">>", url, args);
            xhttp.open("GET", url + formatParams(args), true);
            xhttp.send();
        } else {
            xhttp.open("POST", url, true);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send(args);
        }
    });
}


function init() {
    param_form = document.getElementById("param_form");
    result_form = document.getElementById("result_form");
    load_loading_form(); //FIXME load loading form ...
    setup_session(function() {
        load_greeter_form();
    });
}

function setup_session(callback) {
    function log_callback() {
        console.log("Session name:", get_session_name());
        callback();
    }

    let session_name = get_session_name();
    if (session_name !== null) {
        //check if session still exists
        session_exists(session_name, function (exists) {
            if (exists === true) {
                log_callback();
            } else {
                reset_session();
                create_session(log_callback);
            }
        });
    } else {
        create_session(log_callback);
    }
}

function session_exists(session_name, callback) {
    perform_ajax("/session/"+session_name+"/exists",undefined,"GET", true).then(function(data) {
        let exists;
        try {
            if (data.success !== "true") {
                load_error_form("server request failed: "+data.toString());
            }

            exists = (data.exists === true);
        } catch (e) {
            load_error_form("malformed response: " + data.toString());
        }
        callback(exists);
    }).catch(function(e) {
        load_error_form(e.toString());
    });
}

function create_session(callback) {
    perform_ajax("/session/create", undefined, "GET", true).then(function (data) {
        try {
            if (data.success !== true) {
                load_error_form("server request failed: " + data.toString());
            }

            save_session_name(data.session);

        } catch (e) {
            load_error_form("malformed response: " + data.toString());
        }
        callback();
    }).catch(function (e) {
        load_error_form(e.toString());
    });
}

function reset_session() {
    localStorage.removeItem("genie_session_name");
}

function get_session_name() {
    let value = localStorage.getItem("genie_session_name");
    return value;
}

function save_session_name(session_name) {
    if (typeof(session_name)!=="string") {
        throw "session name is not a string";
    }
    localStorage.setItem("genie_session_name", session_name);
}


function load_loading_form() {
    param_form.innerHTML = `
        Loading ...
    `;
}

function load_greeter_form() {
    param_form.innerHTML = `
        Hi :D
    `;
}

function load_error_form(message) {
    param_form.innerText = message;
}

function load_create_form() {
    param_form.innerHTML = `
                <button onclick="create_form_action()">CREATE</button>
            `;
}

function load_upload_form() {
    param_form.innerHTML = `
                <div id="upload_target">
                    <progress class="progressbar hidden" max="100" value="0">0</progress>
                    <input type="file" class="filechooser hidden">
                </div>
                <button>UPLOAD</button>
            `;
    initFileUpload("#upload_target", function () {
        console.log("ok");
    })
}

function load_request_form() {
    request_fields = [];
    param_form.innerHTML = `
                <input type="text" value="image_color" id="genie_name"><br>
                <button onclick="request_form_action()">REQUEST</button><br>
                <span>Parameters:</span>
                <div id="add_param_form">
                    <button onclick="add_request_parameter_field()" id="add_param_button">add parameter</button>
                </div>
            `;
    add_request_parameter_field();
    request_fields[0][0].value = "num_images";
    request_fields[0][1].value = "4";
}

function load_serve_form() {
    param_form.innerHTML = `
                name: <input type="text" value="output" id="serve_name"><br>
                represent as:
                <select id="serve_type">
                    <option value="text">Text</option>
                    <option value="json">JSON</option>
                    <option value="image">Image</option>
                </select><br>
                <button onclick="serve_form_action()">SERVE</button>
            `;
}


/// ACTIONS ///

function perform_dump_api_request(url, arg, request_type) {
    perform_ajax(url, arg, request_type).always(function(responseText) {
        result_form.innerHTML = responseText;
    });

}

function create_form_action() {
    perform_dump_api_request("http://127.0.0.1:5000/session/create", undefined, "get")
}

function request_form_action() {
    let session_name = $("#session_name").value;
    console.log(">>>", session_name);
    let genie = $("#genie_name").value;

    let parameters = {};
    for (let i in request_fields) {
        let parameter_pair = request_fields[i];
        let param_name = parameter_pair[0].value;
        let param_value = parameter_pair[1].value;

        if (param_name !== "") {
            parameters[param_name] = param_value;
        }
    }

    console.log("Parameters:", parameters);

    perform_dump_api_request("http://127.0.0.1:5000/genie/" + genie + "/request/" + session_name, parameters, "get")
}

function add_request_parameter_field() {
    let param_row = document.createElement("div");

    let name_input = document.createElement("input");
    let value_input = document.createElement("input");
    let remove_button = document.createElement("button");
    remove_button.innerHTML = "-";
    remove_button.onclick = function () {
        //Not implemented ...
    };

    param_row.appendChild(name_input);
    param_row.appendChild(value_input);
    param_row.appendChild(remove_button);

    let add_param_form = $("#add_param_form");
    let add_button = $("#add_param_button");

    add_param_form.insertBefore(param_row, add_button);
    request_fields.push([name_input, value_input, param_row])
}

function serve_form_action() {
    let session_name = get_session_name();
    let name = $("#serve_name").value;
    let element = $("#serve_type");
    let data_id = element.options[element.selectedIndex].value;

    let path = "http://127.0.0.1:5000/session/" + session_name + "/serve/" + name;
    switch (data_id) {
        case "text":
            perform_dump_api_request(path, undefined, "get");
            break;
        case "json":
            throw "Not implemented";
            //break;
        case "image":
            result_form.innerHTML = "<img src='" + path + "' class='result_image'>";
            break;
        default:
            throw "Unknown data_id";
    }
}


function initFileUpload(filedropSelector, onsuccess) {
    let filedrop = $(filedropSelector);
    if (!filedrop) {
        console.error('Selector did not match any element:', filedropSelector);
        return;
    }

    let progressbar = filedrop.querySelector('.progressbar');
    if (!progressbar) console.info('No `.progressbar` found inside', filedrop);

    let filechooser = filedrop.querySelector('.filechooser');
    if (!filechooser) console.info('No `.filechooser` found inside', filedrop);

    let capturebutton = filedrop.querySelector('button');
    if (!capturebutton) console.log('No capturebutton found inside', filedrop);

    let browserSupport = {
        draggable: 'draggable' in document.createElement('span'),
        formdata: !!window.FormData,
        progress: "upload" in new XMLHttpRequest()
    };

    // upload the files
    function uploadFiles(session_name, name, files) {
        let formData = browserSupport.formdata ? new FormData() : null;
        for (let i = 0; i < files.length; i++) {
            if (browserSupport.formdata) formData.append('file', files[i]);
        }

        if (browserSupport.formdata) {
            let xhr = new XMLHttpRequest();
            xhr.open('POST', '/session/' + session_name + '/upload/' + name);
            xhr.onload = function () {
                if (progressbar) progressbar.value = progressbar.innerHTML = "" + 100;
                let response = JSON.parse(this.response);
                if (response.success) {
                    onsuccess(response.filename);
                } else {
                    alert(response.error);
                }
            };

            if (browserSupport.progress) {
                xhr.upload.onprogress = function (event) {
                    if (event.lengthComputable) {
                        let progress = (event.loaded / event.total * 100 | 0);
                        if (progressbar) progressbar.value = progressbar.innerHTML = "" + progress;
                    }
                };
            }

            xhr.onreadystatechange = function () {
                if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                    result_form.innerHTML = this.responseText;
                }
            };

            xhr.send(formData);
        }
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
            let session_name = get_session_name();
            uploadFiles(session_name, "source", e.dataTransfer.files);
        };
    }

    // add change event for filechooser
    filechooser.onchange = function () {
        let session_name = get_session_name();
        uploadFiles(session_name, "source", this.files);
    };

    // open file chooser on click
    filedrop.onclick = function (e) {
        if (e.target !== capturebutton) {
            filechooser.click();
        }
    };
}