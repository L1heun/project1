function preview(fileIdx) {
	$("#preview-modal").modal("show");
	$(".modal-body").empty();
	$(".modal-footer").empty();
	fileType = $("#file_" + fileIdx + " .file_type").text();

	if (fileType == 'image') {
		imgView = $("#file_" + fileIdx + " div img").attr("src");
		div = "<div class = 'imgLiquidFill imgLiquid imgLiquid_bgSize imgLiquid_ready preview_img'>";
		div += "<img src = '" + imgView + "'>";
		div += "</div>";
		$(".modal-body").append(div);
		var img = new Image();
		img.src = imgView;
		height = img.height;
		$(".preview_img").height(height);
		$(".imgLiquidFill").imgLiquid({
			fill: false,
			horizontalAlign: "center",
			verticalAlign: "50%"
		});
		div = "<a class = 'btn btn-primary' href = '/download/" + fileIdx + "'>다운로드</a>";
		$(".modal-footer").append(div);
	} else {
		div = "<div class = 'non'>";
		div += "<p class = 'text-center'>";
		div += "지원하지 않는 포맷입니다.";
		div += "</p>";
		div += "<a class = 'btn btn-primary' href = '/download/" + fileIdx + "'>다운로드</a>";
		div += "</div>";
		$(".modal-body").append(div);
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
