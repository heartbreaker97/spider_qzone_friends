<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="X-UA-Compatible" content="IE=8">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>好友关系网络</title>
<script type="text/javascript" charset="utf-8"></script>
<script type="text/javascript" src="jquery.min.js">
</script> 
<script type="text/javascript" src="echarts.js">
</script>  <!--导入的为ECharts3的js -->

<script type="text/javascript">
$(function(){
	postChart();
});
//学员职务统计图
function postChart(){
	//这个echarts对象应该是在echarts-all.js文件里面初始化好的，所以直接拿来用，
	var myChart = echarts.init(document.getElementById('main')); 
	var option={
 title: {
            text:"qq好友关系网"
            },
             series: [{
                itemStyle: {                
                    normal: {
                        label: {
                            position: 'top',
                            show: true,
                            textStyle: {
                                color: '#333'
                            }
                        },
                        nodeStyle: {
                            brushType: 'both',
                            borderColor: 'rgba(255,215,0,0.4)',
                            borderWidth: 1
                        },
                        linkStyle: {
                            normal: {
                                color: 'source',
                                curveness: 0,
                                type: "solid"
                            }
                        },
                        force: {
				            edgeLength: [100,200],//线的长度，这个距离也会受 repulsion，支持设置成数组表达边长的范围
				            repulsion: 100//节点之间的斥力因子。值越大则斥力越大
				        }
                    },

                },
                     force:{
                    initLayout: 'circular',//初始布局
                    repulsion:200,//斥力大小
                },

                hoverAnimation: true,//是否开启鼠标悬停节点的显示动画
                name:"",
                type: 'graph',//关系图类型
                layout: 'force',//引力布局
                roam: true,//可以拖动
                draggable: true,
                focusNodeAdjacency:true,//移到节点高亮显示临边
              //  legendHoverLink: true,//是否启用图例 hover(悬停) 时的联动高亮。
               // coordinateSystem: null,//坐标系可选
              //  xAxisIndex: 0, //x轴坐标 有多种坐标系轴坐标选项
              //  yAxisIndex: 0, //y轴坐标 
               // ribbonType: true,
                useWorker: false,
                minRadius: 15,
                maxRadius: 25,
                gravity: 1.1,

                scaling: 1.1,
                "nodes": [
                	<?php
				 		$file = fopen('这里修改为第三步得到的txt文件路径','r,ccs=UTF-8');
				 		$id = 0;
				 		$name_id = [];
				 		#生成name_id映射数组
				 		while (! feof($file)) {
				 			#每一行两个名字的标记
				 			$flag_0 = true;
				 			$flag_1 = true;
				 			$line = fgets($file);
				 			$data = explode('$|$', $line);
							if($data['0'] == '')
								continue;
							#便利遍历数组如果该节点id以生成那么不再生成结点
				 			foreach ($name_id as $key => $value) {
				 				#存在则不生成
				 				if($data[0] == $key )
				 					$flag_0 = false;
				 				if($data[1] == $key )
				 					$flag_1 = false;
				 			}
				 			if($data[0] == $data[1])
				 				$flag_1=false;
				 			if($flag_0){
				 				$name_id["$data[0]"] = $id;
				 				$id++;
				 			}
				 			if($flag_1){
				 				$name_id["$data[1]"] = $id;
				 				$id++;
				 			}
				 		}
			 	        #根据name_id生成全部节点
			 	        foreach ($name_id as $key => $value) {
			 	        	
			 	        ?>
                		{ "id": "<?php echo $value;?>", "category": 0, "name": "<?php echo $key?>"},
						<?php }?>
                ],//数据内容
                //接收格式均为json对象数组
                "links": [
                	<?php
                		#再读一遍数据
                		$file2 = fopen('这里修改为第三步得到的txt文件路径','r,ccs=UTF-8');
				 		while (! feof($file2)) {
				 			$line = fgets($file2);
				 			$data = explode('$|$', $line);
				 			if($data['0'] == '')
								continue;
				 			#根据name_id，生成对应边
				 	?>	
				 	 {
			            "source": <?php echo $name_id[$data[0]];?>,//起始节点，0表示第一个节点
			            "target": <?php echo $name_id[$data[1]];?>, //目标节点，1表示与索引为1的节点进行连接
			            "lineStyle": {"width":<?php echo (int)$data[2]/100 < 1? 1 : (int)$data[2]/100;?>}
			         },

				 	<?php	
				 		}
                	?>
                    
                ]//关系对应
            } ]            
}
   myChart.setOption(option);//将option添加到mychart中
}
</script>

</script>
</head>
<body>

    <!-- 为 ECharts 准备一个具备大小（宽高）的 DOM -->
   <div id="main" style="width: 90%;height:900px;">
     
   </div>
           


</body>
</html>