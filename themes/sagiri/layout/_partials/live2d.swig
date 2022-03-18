<div class="live2d-container">
	<div class="live2d-tips"></div>
	<canvas id="live2d-canvas" height="{{ theme.live2d.height }}" style="width:{{ theme.live2d.width }}px;" ></canvas>
	<div class="live2d-tools">
		<i class="fa fa-commenting"></i>
		<i class="fa fa-chevron-down"></i>
		<i class="fa fa-chevron-up"></i>
	</div>
</div>

<script type="text/javascript" src="{{ url_for(theme.js) }}/live2d.js"></script>
<script type="text/javascript" src="{{ url_for(theme.js) }}/live2d_tools.js"></script>
<script>
	loadlive2d('live2d-canvas', "{{ theme.live2d.model }}");
</script>
