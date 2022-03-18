window.FastClick = require('fastclick');
require('lazyload');
require('fancybox')(window.$);
window.notie = require('corner-notie');

require('./utils');
require('./motion');
require('./affix'); // 侧边栏随滚动条滑动
require('./pisces')(); // 侧边栏随滚动条滑动
require('./scrollspy');
require('./post-details')(); // 目录相关的事件
require('./bootstrap');
require('./share')(); //文章分享
require('./since');  //运行时间统计
require('./title'); //标题变化
require('./scroll'); //回到顶部，向上滑动显示菜单
require('./code_block');
require('./other_detail');
