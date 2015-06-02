$(document).ready(function() {
	var tmp = "<div class='col-lg-13'>";
	tmp += "<div class='input-group'>";
	tmp += "<input type='text' class='form-control' id='input-keyword' placeholder='Search for...'>";
	tmp += "<span class='input-group-btn'>";
	tmp += "<button class='btn btn-default' id='btn-search' type='button' onclick='search()'>";
	tmp += "<span class='glyphicon glyphicon-search' aria-hidden='true'></span>";
	tmp += "</button></span></div></div>";
	$("#file-search").attr("data-html", "true").attr("data-content", tmp);
	$('[data-toggle="popover"]').popover();
});

function search() {
	keyword = $("#input-keyword").val();
	var formData = new FormData();
	url = "/api/ver-1/file/search";
	formData.append("keyword", keyword);
	$.ajax({
		url : url,
		data : formData,
		mimeType:"multipart/form-data",
		contentType: false,
		cache: false,
		type : "POST",
		processData:false,
		success: function(data) {
			obj = encodeJSON(data);
			for (var i = 0; i < obj.length; i++) {
				console.log(obj[i]);
				tmp = "<tr onclick = 'preview(" + obj[i]['fileIdx'] + ")' id = 'file_" + obj[i]['fileIdx'] + ")'>"
				tmp += "<td>"
				tmp += "<div class = 'imgLiquidFill imgLiquid imgLiquid_bgSize imgLiquid_ready thumb_nail'>"
				
				if(obj[i]['fileType'] == 'file') {
					tmp += "<img src = '/static/res/file.png'>";
				} else if(obj[i]['fileType'] == 'music') {
					tmp += "<img src = '/static/res/music.png'>";
				} else if(obj[i]['fileType'] == 'movie') {
					tmp += "<img src = '/static/res/movie.png'>";
				} else if(obj[i]['fileType'] == 'image') {
					tmp += "<img src = '/static/" + obj[i]['filePath'] + "'>";
				}
				tmp += "</div>";
				tmp += "<p style = 'float : left; padding-top : 5px;'>" + obj[i]['fileOriginName'] + "</p>";
				tmp += "</td>";
				tmp += "<td style = 'padding-top : 15px;' class='file_type'>" + obj[i]['fileType'] + "</td>";
				tmp += "<td style = 'padding-top : 15px;''>" + obj[i]['fileInitDate'] + "</td>";
				tmp += "</tr>"
				$("#search-modal table tbody").append(tmp);
			}
			$("#search-modal table").css("width", "100%");
			$("#search-modal").modal("show");
			$('[data-toggle="popover"]').popover("hide");
			$(".imgLiquidFill").imgLiquid();
		},
		statusCode : {
			404 : function() {
				alert("검색결과가 없습니다.");
			}
		}
	});
}

function preview(fileIdx) {
	$("#preview-modal").modal("show");
	$("#preview-modal .modal-body").empty();
	$("#preview-modal .modal-footer").empty();
	fileType = $("#file_" + fileIdx + " .file_type").text();

	if (fileType == 'image') {
		imgView = $("#file_" + fileIdx + " div img").attr("src");
		div = "<div class = 'imgLiquidFill imgLiquid imgLiquid_bgSize imgLiquid_ready preview_img'>";
		div += "<img src = '" + imgView + "'>";
		div += "</div>";
		$("#preview-modal .modal-body").append(div);
		var img = new Image();
		img.src = imgView;
		height = img.height;
		$(".preview_img").height(height);
		$(".imgLiquidFill").imgLiquid({
			fill: true,
			horizontalAlign: "center",
			verticalAlign: "50%"
		});
		div = "<a class = 'btn btn-primary' href = '/download/" + fileIdx + "'>다운로드</a>";
		$("#preview-modal .modal-footer").append(div);
	} else {
		div = "<div class = 'non'>";
		div += "<p class = 'text-center'>";
		div += "지원하지 않는 포맷입니다.";
		div += "</p>";
		div += "<a class = 'btn btn-primary' href = '/download/" + fileIdx + "'>다운로드</a>";
		div += "</div>";
		$("#preview-modal .modal-body").append(div);
	}
}

function menuBar(fileType) {
	menuBarOff();
	files = $('.file_type');
	for(var i = 0; i < files.length; i++) {
		if($(files[i]).text() != fileType) {
			$(files[i]).parent().css("display", "none");
		}
	}
}

function menuBarOff() {
	$('.file_type').parent().css("display", "");
}
