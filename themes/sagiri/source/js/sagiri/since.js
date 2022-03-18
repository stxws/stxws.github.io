function show_date_time()
{
	window.setTimeout(function () {
		show_date_time();
	}, 1000);

	var birth_time = window.CONFIG.since;
	var BirthDay = new Date(birth_time);
	var tmp_date = new Date(birth_time);
	var today = new Date();

	tmp_date.setFullYear(today.getFullYear());
	tmp_date.setMonth(today.getMonth());
	if(today.getTime() < tmp_date.getTime())
	{
		var tmp_month = tmp_date.getMonth();
		if(tmp_date.getMonth() == 0)
		{
			tmp_date.setMonth(11);
			tmp_date.setFullYear(today.getFullYear() - 1);
		}
		else
		{
			tmp_date.setMonth(today.getMonth() - 1);
		}
	}
	var dif_year = tmp_date.getFullYear() - BirthDay.getFullYear();
	var dif_month = tmp_date.getMonth() - BirthDay.getMonth();
	if(dif_month < 0)
	{
		dif_year = dif_year - 1;
		dif_month = dif_month + 12;
	}

	var dif_time = today.getTime() - tmp_date.getTime();
	dif_time = Math.floor(dif_time / 1000) * 1.0;
	var dif_day  = Math.floor(dif_time / 60 / 60 / 24);
	var dif_hour = Math.floor(dif_time / 60 / 60) % 24;
	var dif_min  = Math.floor(dif_time / 60) % 60;
	var dif_sec  = dif_time % 60;

	var dif_text = dif_day + "天" + dif_hour + "小时" + dif_min + "分" + dif_sec + "秒";
	if(dif_month > 0)
	{
		dif_text = dif_month + "个月" + dif_text;
	}
	if(dif_year > 0)
	{
		dif_text = dif_year + "年" + dif_text;
	}

	$('#since').html(dif_text);
}
show_date_time();