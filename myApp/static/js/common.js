function encodeJSON(data) {
	var data = data.replace(/&#34;/gi, '"');
	var obj = jQuery.parseJSON(data);
	return obj;
}

function objSize(Object) {
	// 오브젝트의 사이즈를 구한다. (배열)

	var key, count = 0;
	for(key in Object) {
		if(Object.hasOwnProperty(key)) {
			count++;
		}
	}
	return count;
}