class Live2dMessage {
	/**
	 * @param show_time 每条消息显示的时间
	 */
	constructor(show_time){
		this.show_time = show_time;
	}
	show_message(msg_text){
		var msg_container = document.getElementsByClassName("live2d-tips")[0];
		var new_msg = document.createElement('div');
		new_msg.className = "live2d-tip-item";
		new_msg.innerText = msg_text;
		msg_container.append(new_msg);
		setTimeout(() => {
			new_msg.remove();
		}, this.show_time);
	}
}

function init_live2d_tools(){
	var commenting    = document.getElementsByClassName("fa-commenting")[0];
	var chevron_down  = document.getElementsByClassName("fa-chevron-down")[0];
	var chevron_up    = document.getElementsByClassName("fa-chevron-up")[0];
	var live2d_tips   = document.getElementsByClassName("live2d-tips")[0];
	var live2d_canvas = document.getElementById("live2d-canvas");

	var live2d_message = new Live2dMessage(15000);

	function show_random_msg() {
		fetch("https://v1.hitokoto.cn/").then(response => {
			return response.json();
		}).then(res => {
			var msg_text = res.hitokoto;
			// console.log(msg_text);
			live2d_message.show_message(msg_text);
		});
	}

	commenting.onclick = show_random_msg;

	chevron_down.onclick = function() {
		live2d_canvas.style.display = "none";
		live2d_tips.style.display = "none";
		commenting.style.display = "none";
		chevron_down.style.display = "none";
		chevron_up.style.display = "block";
	}

	chevron_up.style.display = "none";
	chevron_up.onclick = function() {
		live2d_canvas.style.display = "block";
		live2d_tips.style.display = "block";
		commenting.style.display = "block";
		chevron_down.style.display = "block";
		chevron_up.style.display = "none";
	}

	show_random_msg();
	setInterval(show_random_msg, 60 * 1000);
}

init_live2d_tools();