var $ = function(q) { return document.querySelector(q); };

// hasClass, addClass and removeClass polyfills
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


// initFileUpload adds drag'n'drop and click handlers to the element selected
// by the given css selector `filedropSelector`
function initFileUpload(filedropSelector, onsuccess) {
  var filedrop = $(filedropSelector);
  if (!filedrop) {
    console.error('Selector did not match any element:', filedropSelector);
    return;
  }

  var progressbar = filedrop.querySelector('.progressbar');
  if (!progressbar) console.info('No `.progressbar` found inside', filedrop);

  var filechooser = filedrop.querySelector('.filechooser');
  if (!filechooser) console.info('No `.filechooser` found inside', filedrop);

  var capturebutton = filedrop.querySelector('button');
  if (!capturebutton) console.log('No capturebutton found inside', filedrop);

  var video = filedrop.querySelector('video');
  if (!video) console.log('No video element found inside', filedrop);

  var acceptedTypes = {
    'image/png': true,
    'image/jpeg': true,
    'image/gif': true
  };

  var browserSupport = {
    draggable: 'draggable' in document.createElement('span'),
    formdata: !!window.FormData,
    progress: "upload" in new XMLHttpRequest()
  };

  // upload the files
  function uploadFiles(files) {
    var formData = browserSupport.formdata ? new FormData() : null;
    for (var i = 0; i < files.length; i++) {
      if (browserSupport.formdata) formData.append('file', files[i]);
    }

    if (browserSupport.formdata) {
      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/upload');
      xhr.onload = function(e) {
        if (progressbar) progressbar.value = progressbar.innerHTML = 100;
        var response = JSON.parse(this.response);
        if (response.success) {
          onsuccess(response.filename);
        } else {
          alert(response.error);
        }
      };

      if (browserSupport.progress) {
        xhr.upload.onprogress = function (event) {
          if (event.lengthComputable) {
            var progress = (event.loaded / event.total * 100 | 0);
            if (progressbar) progressbar.value = progressbar.innerHTML = progress;
          }
        };
      }

      xhr.send(formData);
    }
  }

  // start webcam video stream
  if ('mediaDevices' in navigator && 'getUserMedia' in navigator.mediaDevices) {
    navigator.mediaDevices.getUserMedia({video: true, audio: false}).then(function(mediaStream) {
      video.srcObject = mediaStream;
      video.onloadedmetadata = function(e) {
        video.play();
        video.removeClass('hidden');
        capturebutton.removeClass('hidden');
      };
    }).catch(function(e) {
      console.log(e);
    });
  } else {
    console.log("Webcam capturing is not supported by this browser.");
  }


  // add drag and drop events
  if (browserSupport.draggable) {
    filedrop.ondragover = function () { this.addClass('hover'); return false; };
    filedrop.ondragend = function () { this.removeClass('hover'); return false; };
    filedrop.ondrop = function (e) {
      this.removeClass('hover');
      e.preventDefault();
      uploadFiles(e.dataTransfer.files);
    };
  }

  // add change event for filechooser
  filechooser.onchange = function () {
    uploadFiles(this.files);
  };

  // open file chooser on click
  filedrop.onclick = function(e) {
    if (e.target !== capturebutton) {
      filechooser.click();
    }
  };

  // capture image from webcam
  capturebutton.onclick = function(e) {
    var canvas = document.createElement('canvas');
    canvas.width  = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
    var dataURL = canvas.toDataURL('image/png');
    var blobBin = atob(dataURL.split(',')[1]);
    var array = [];
    for(var i = 0; i < blobBin.length; i++) {
        array.push(blobBin.charCodeAt(i));
    }
    var file = new File([new Uint8Array(array)], 'webcam.png', {type: 'image/png'});
    uploadFiles([file]);
  };
}

initFileUpload('.placeholder.left', function(filename) {
  console.log(filename);
  $('.imgwrapper.left img').src = '/uploads/' + filename;
  $('.imgwrapper.left .toolbar span').innerText = filename;
  $('.imgwrapper.left').removeClass('hidden');
  $('.placeholder.left').addClass('hidden');
});

initFileUpload('.placeholder.right', function(filename) {
  console.log(filename);
  $('.imgwrapper.right img').src = '/uploads/' + filename;
  $('.imgwrapper.right .toolbar span').innerText = filename;
  $('.imgwrapper.right').removeClass('hidden');
  $('.placeholder.right').addClass('hidden');
});

$('.imgwrapper.left .toolbar i').addEventListener('click', function() {
  $('.imgwrapper.left').addClass('hidden');
  $('.placeholder.left').removeClass('hidden');
});

$('.imgwrapper.right .toolbar i').addEventListener('click', function() {
  $('.imgwrapper.right').addClass('hidden');
  $('.placeholder.right').removeClass('hidden');
});

// retrieve images for the immage gallery
var xhr = new XMLHttpRequest();
xhr.open('GET', '/api/get/uploads.json');
xhr.onload = function(e) {
  var response = JSON.parse(this.response);
  console.log(response.files);
  var gallery = $('.gallery .content');
  gallery.innerText = '';
  for (var i = 0; i < response.files.length; i++) {
    var filename = response.files[i];
    var imgwrapper = document.createElement('div');
    imgwrapper.className = 'imgwrapper';
    var img = document.createElement('img');
    img.src = '/uploads/' + filename;
    var span = document.createElement('span');
    span.innerText = filename;
    imgwrapper.appendChild(img);
    imgwrapper.appendChild(span);
    gallery.appendChild(imgwrapper);
  }
};
xhr.send();
