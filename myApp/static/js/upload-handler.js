$(document).ready(function() {
	f = 0;
	var obj = $("#dragandrophandler");
	obj.on('dragenter', function (e) {
		e.stopPropagation();
		e.preventDefault();
		$(this).css('border', '2px solid #0B85A1');
	});

	obj.on('dragover', function (e) {
		e.stopPropagation();
		e.preventDefault();
	});

	obj.on('drop', function (e) {
		e.stopPropagation();
		e.preventDefault();
		$(this).css('border', '2px dotted #0B85A1');
		if (f == 1) {
			var files = e.originalEvent.dataTransfer.files;
			handleFileUpload(files,obj);
			f = 0;
		} else {
			f +=1;
		}
	});
	$(document).on('dragenter', function (e) 
	{
		e.stopPropagation();
		e.preventDefault();
	});
	$(document).on('dragover', function (e) 
	{
		e.stopPropagation();
		e.preventDefault();
		obj.css('border', '2px dotted #0B85A1');
	});
	$(document).on('drop', function (e) 
	{
		e.stopPropagation();
		e.preventDefault();
	});
});

function addFile(id, file) {
	var template = '' +
		'<div class="file box" id="uploadFile' + id + '">' +
			'<div class="info">' +
				'#' + id + ' - <span class="filename" title="Size: ' + file.size + 'bytes - Mimetype: ' + file.type + '">' + file.name + '</span><br /><small>Status: <span class="status">Waiting</span></small>' +
				'</div>' +
				'<div caivlass="bar">' +
					'<div class="progressColor" style="width:0%">' + 
				'</div>' +
			'</div>' +
			'<div class="progress">' +
				'<div class="progress-bar progress-bar-info progress-bar-striped active" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="min-width: 2em;">' + 
					'0%' + 
				'</div>' +
			'</div>' + 
		'</div>';
	$(".modal-body").append(template)
};

fileIdx = 0;

function fileUploadStatus(id, status, message) {
	$('#uploadFile' + id).find('span.status').html(message).addClass(status);
};

function handleFileUpload(files,obj) {
	for (var i = 0; i < files.length; i++)  {
			fileIdx += 1;
			// fd.append('file', files[i]);
			addFile(fileIdx, files[i]);
			sendFileToServer(fileIdx, files[i]);
	}
}

function sendFileToServer(fileIdx, file) {
	var formData = new FormData();
	formData.append("files", file);
	console.log(file);
	console.log(formData);

	$.ajax({
		url : "/api/ver-1/file/upload",
		data : formData,
		mimetype : "multipart/form-data",
		contentType : false,
		cache : false,
		processData : false,
		type : "POST",
		xhr : function () {
			var xhr = new window.XMLHttpRequest();
			console.log("XHR");
			console.log(xhr);
			//Download progress
			if (xhr.upload) {
				console.log("asdF");
			}
			xhr.addEventListener("progress", function (evt) {
				if (evt.lengthComputable) {
					var percentComplete = evt.loaded / evt.total;
					var percent = Math.round(percentComplete * 100) + "%"
					// $("#uploadFile" + fileIdx).find(".progress .progress-bar").css("width", percent);
					// $("#uploadFile" + fileIdx).find(".progress .progress-bar").text(percent);
					$("#uploadFile" + fileIdx + " .progress .progress-bar").css("width", percent);
					$("#uploadFile" + fileIdx + " .progress .progress-bar").text(percent);
				}
			}, false);
			return xhr;
		},
		beforeSend : function () {
			// $("#uploadFile" + fileIdx).find(".status").text("Waiting");
			$("#uploadFile" + fileIdx + " .status").text("Waiting");
			console.log("beforeSend");
		},
		complete : function () {
			$("#uploadFile" + fileIdx + " .status").text("Success");
			console.log("complete");
		},
		success : function (json) {
			$("#uploadFile" + fileIdx + " .status").text("Sending");
			console.log("success");
		},
		error : function (xhr, ajaxOptions, thrownError) {
			console.log("반환 : " + xhr.responseText);
			console.log("에러로그 : " + thrownError);
			$("#uploadFile" + fileIdx + " .status").text("Error");
			$("#uploadFile" + fileIdx).find(".progress .progress-bar").removeClass("progress-bar-info").addClass("progress-bar-danger");
		}
	});
}

