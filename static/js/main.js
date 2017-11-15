Element.prototype.hasClass = Element.prototype.hasClass || function ( className ) {
  return (' ' + this.className + ' ').indexOf(' ' + className + '') !== -1;
};
Element.prototype.addClass = Element.prototype.addClass || function ( className ) {
  if (!this.hasClass(className)) this.className += ' ' + className;
  return this;
};
Element.prototype.removeClass = Element.prototype.removeClass || function ( className ) {
  this.className = this.className.toLowerCase().replace(className.toLowerCase(), '');
  return this;
};

function initFileUpload(filedropSelector) {
  console.log(filedropSelector);
  var filedrop = document.querySelector(filedropSelector);
  var progressbar = filedrop.querySelector('.uploadprogress');
  var filechooser = filedrop.querySelector('.filechooser');
  console.log(filedrop, progressbar, filechooser);

  var acceptedTypes = {
    'image/png': true,
    'image/jpeg': true,
    'image/gif': true
  };

  var browserSupport = {
    filereader: typeof FileReader != 'undefined',
    draggable: 'draggable' in document.createElement('span'),
    formdata: !!window.FormData,
    progress: "upload" in new XMLHttpRequest()
  };

  function previewfile(file) {
    if (browserSupport.filereader === true && acceptedTypes[file.type] === true) {
      var reader = new FileReader();
      reader.onload = function (event) {
        var image = new Image();
        image.src = event.target.result;
        image.width = 250; // a fake resize
        filedrop.appendChild(image);
      };

      reader.readAsDataURL(file);
    }
  }

  function readfiles(files) {
      var formData = browserSupport.formdata ? new FormData() : null;
      for (var i = 0; i < files.length; i++) {
        if (browserSupport.formdata) formData.append('file', files[i]);
        //previewfile(files[i]);
      }

      // upload the files
      if (browserSupport.formdata) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/upload');
        xhr.onload = function(e) {
          progressbar.value = progressbar.innerHTML = 100;
          showImage(JSON.parse(e.target.response).filename);
        };

        if (browserSupport.progress) {
          xhr.upload.onprogress = function (event) {
            if (event.lengthComputable) {
              var progress = (event.loaded / event.total * 100 | 0);
              progressbar.value = progressbar.innerHTML = progress;
            }
          };
        }

        xhr.send(formData);
      }
  }

  function showImage(filename) {
    console.log(filename);
    document.querySelector('.imgwrapper.left img').src = '/images/' + filename;
    document.querySelector('.imgwrapper.left .toolbar span').innerText = filename;
    document.querySelector('.imgwrapper.left').removeClass('hidden');
    document.querySelector('.placeholder.left').addClass('hidden');
  }

  // add drag and drop events
  if (browserSupport.draggable) {
    filedrop.ondragover = function () { this.addClass('hover'); return false; };
    filedrop.ondragend = function () { this.removeClass('hover'); return false; };
    filedrop.ondrop = function (e) {
      this.removeClass('hover');
      e.preventDefault();
      readfiles(e.dataTransfer.files);
    };
  }

  // add change event for filechooser
  filechooser.onchange = function () {
    readfiles(this.files);
  };

  // open file chooser on click
  filedrop.onclick = function(e) {
    filechooser.click();
  };
}

initFileUpload('.placeholder.left');
