jQuery(document).ready(function($){
	//if you change this breakpoint in the style.css file (or _layout.scss if you use SASS), don't forget to update this value as well
	var $L = 1200,
		$menu_navigation = $('#main-nav'),
		$cart_trigger = $('#cl-cart-trigger'),
		$hamburger_icon = $('#cl-hamburger-menu'),
		$lateral_cart = $('#cl-cart'),
		$shadow_layer = $('#cl-shadow-layer');

	//open lateral menu on mobile
	$hamburger_icon.on('click', function(event){
		event.preventDefault();
		//close cart panel (if it's open)
		$lateral_cart.removeClass('speed-in');
		toggle_panel_visibility($menu_navigation, $shadow_layer, $('body'));
	});

	//open cart
	$cart_trigger.on('click', function(event){
		event.preventDefault();
		//close lateral menu (if it's open)
		$menu_navigation.removeClass('speed-in');
		toggle_panel_visibility($lateral_cart, $shadow_layer, $('body'));
	});

	//close lateral cart or lateral menu
	$shadow_layer.on('click', function(){
		$shadow_layer.removeClass('is-visible');
		// firefox transitions break when parent overflow is changed, so we need to wait for the end of the trasition to give the body an overflow hidden
		if( $lateral_cart.hasClass('speed-in') ) {
			$lateral_cart.removeClass('speed-in').on('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(){
				$('body').removeClass('overflow-hidden');
			});
			$menu_navigation.removeClass('speed-in');
		} else {
			$menu_navigation.removeClass('speed-in').on('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(){
				$('body').removeClass('overflow-hidden');
			});
			$lateral_cart.removeClass('speed-in');
		}
	});

	//move #main-navigation inside header on laptop
	//insert #main-navigation after header on mobile
	move_navigation( $menu_navigation, $L);
	$(window).on('resize', function(){
		move_navigation( $menu_navigation, $L);
		
		if( $(window).width() >= $L && $menu_navigation.hasClass('speed-in')) {
			$menu_navigation.removeClass('speed-in');
			$shadow_layer.removeClass('is-visible');
			$('body').removeClass('overflow-hidden');
		}

	});
	
	//Ajax를 이용하는 일반적인 form 데이터 전송.
	$('#cl-form').submit(function(){
		
		//데이터 일괄 검사
		callValidation('#cl-form',true);
		return false;
		
	});
	
    //Ajax를 이용하는 simulation sfa form 데이터 전송.
    $('#cl-simul-sfa-form').submit(function(){

        callSimulAjaxSfa($('#cl-simul-sfa-form'));
        return false;

    });

	//Ajax를 이용하는 simulation attractor form 데이터 전송.
	$('#cl-simul-attractor-form').submit(function(){
		
		callSimulAjax($('#cl-simul-attractor-form'));
		return false;
		
	});
	
	//삭제 모드 delete
	$('.delete-open').click(function(){
		 
		 sendCheckMessage("삭제된 자료는 복구가 불가능합니다.<br /><br />삭제하시겠습니까?",$(this).data("urldata"),"삭제");
		
	})
	
	//로그인 클릭하면.
	$('.login-open').click(function(){

		$("body").append("<div id='cl-message-veil'></div> <div id='cl-message'> <div class='message-title'>Notification</div> <div class='message-content'>로그인이 필요한 서비스입니다.</div> <div class='message-button'><a href='#0' id='messagebutton'>로그인</a></div> </div>");
		$('#messagebutton').focus();
		
		$('#cl-message-veil').click(function(){
			$('#cl-message-veil').remove();
			$('#cl-message').remove();
		});
		
		$('#messagebutton').click(function(){
			window.location.assign($("#clpathhost").val() + "index.php?module=member&act=login.php");
		});
			
	});	
	
	//Simulation 에서 module change
	$('#cl-simul-module').change(function(){
		 
		if($("#cl-simul-module").val() == "dream2015"){
			
			//Get 방식으로 전송하기 위해 주소를 파라미터로.
			callGetSimulAjax($("#clpathhost").val() + "index.php?module=simulation&act=dream2015_cellline_work.php","dream2015_cellline");
			
			$("#cl-simul-sfa").hide();
			$("#cl-simul-sfa-graph").hide();
			$("#cl-simul-attractor").hide();
			$("#cl-simul-attractor-graph").hide();
			
			
		}else if($("#cl-simul-module").val() == "sfa"){
			
			//Get 방식으로 전송하기 위해 주소를 파라미터로.
			callGetSimulAjax($("#clpathhost").val() + "index.php?module=simulation&act=sfa_target1_work.php","sfa_target1");
			
			$("#cl-simul-dream2015").hide();
			$("#cl-simul-dream2015-graph").hide();
			$("#cl-simul-attractor").hide();
			$("#cl-simul-attractor-graph").hide();
			
		}else if($("#cl-simul-module").val() == "attractor"){
			
			//Get 방식으로 전송하기 위해 주소를 파라미터로.
			callGetSimulAjax($("#clpathhost").val() + "index.php?module=simulation&act=attractor_target1_work.php","attractor_target1");
			
			$("#cl-simul-dream2015").hide();
			$("#cl-simul-dream2015-graph").hide();
			$("#cl-simul-sfa").hide();
			$("#cl-simul-sfa-graph").hide();
			
			//체크박스 초기화
			$("#cl-simul-attractor-node1").attr('checked', false); 
			$("#cl-simul-attractor-node2").attr('checked', false); 
			$("#cl-simul-attractor-node3").attr('checked', false); 
			$("#cl-simul-attractor-node4").attr('checked', false); 
			$("#cl-simul-attractor-node5").attr('checked', false); 
		}
	})
	
	//Simulation 에서 dream2015 cellline change
	$('#cl-simul-dream2015-cellline').change(function(){
		
		
		var cellline = $('#cl-simul-dream2015-cellline').val();
		
		//Get 방식으로 전송하기 위해 주소를 파라미터로.
		callGetSimulAjax($("#clpathhost").val() + "index.php?module=simulation&act=dream2015_drug1_work.php&cellline=" + cellline,"dream2015_drug1");
	})
	
	//Simulation 에서 dream2015 drug1 change
	$('#cl-simul-dream2015-drug1').change(function(){
		
		var cellline = $('#cl-simul-dream2015-cellline').val();
		var drug1 = $('#cl-simul-dream2015-drug1').val();
		
		//Get 방식으로 전송하기 위해 주소를 파라미터로.
		callGetSimulAjax($("#clpathhost").val() + "index.php?module=simulation&act=dream2015_drug2_work.php&cellline=" + cellline + "&drug1=" + drug1,"dream2015_drug2");
	})
	
	//Simulation 에서 dream2015 drug2 change
	$('#cl-simul-dream2015-drug2').change(function(){
		
		var cellline = $('#cl-simul-dream2015-cellline').val();
		var drug1 = $('#cl-simul-dream2015-drug1').val();
		var drug2 = $('#cl-simul-dream2015-drug2').val();
		
		//Get 방식으로 전송하기 위해 주소를 파라미터로.
		callGetSimulAjax($("#clpathhost").val() + "index.php?module=simulation&act=dream2015_graph_work.php&cellline=" + cellline + "&drug1=" + drug1 + "&drug2=" + drug2,"dream2015_graph");
	})
	
	//Simulation 에서 attractor target1 change
	$('#cl-simul-attractor-target1').change(function(){
		
		
		var target1 = $('#cl-simul-attractor-target1').val();
		
		//Get 방식으로 전송하기 위해 주소를 파라미터로.
		callGetSimulAjax($("#clpathhost").val() + "index.php?module=simulation&act=attractor_target2_work.php&target1=" + target1,"attractor_target2");
	})
	
	//Simulation 에서 sfa target1 change
	$('#cl-simul-sfa-target1').change(function(){
		
		
		var target1 = $('#cl-simul-sfa-target1').val();
		
		//Get 방식으로 전송하기 위해 주소를 파라미터로.
		callGetSimulAjax($("#clpathhost").val() + "index.php?module=simulation&act=sfa_target2_work.php&target1=" + target1,"sfa_target2");
	})
	
	
});

function toggle_panel_visibility ($lateral_panel, $background_layer, $body) {
	if( $lateral_panel.hasClass('speed-in') ) {
		// firefox transitions break when parent overflow is changed, so we need to wait for the end of the trasition to give the body an overflow hidden
		$lateral_panel.removeClass('speed-in').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(){
			$body.removeClass('overflow-hidden');
		});
		$background_layer.removeClass('is-visible');

	} else {
		$lateral_panel.addClass('speed-in').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(){
			$body.addClass('overflow-hidden');
		});
		$background_layer.addClass('is-visible');
	}
}

function move_navigation( $navigation, $MQ) {
	if ( $(window).width() >= $MQ ) {
		$navigation.detach();
		$navigation.appendTo('header');
	} else {
		$navigation.detach();
		$navigation.insertAfter('header');
	}
}


/* --------------------------------

자체 함수

-------------------------------- */
//안내방송
function sendMessage(msg,val){
	
	$("body").append("<div id='cl-message-veil'></div> <div id='cl-message'> <div class='message-title'>Notification</div> <div class='message-content'> "+msg+" </div> <div class='message-button'><a href='#0' id='messagebutton'>닫기</a></div> </div>");
	$('#messagebutton').focus();
	
	$('#cl-message-veil').click(function(){
		$('#cl-message-veil').remove();
		$('#cl-message').remove();
		if(val){
			val.focus();
		}
		
	});
	
	$('#messagebutton').click(function(){
		$('#cl-message-veil').remove();
		$('#cl-message').remove();
		if(val){
			val.focus();
		}
	});
	
}

//체크 안내방송  - 삭제와 같이 확인여부를 물을 때 사용
function sendCheckMessage(msg,move,option){
	
	$("body").append("<div id='cl-message-veil'></div> <div id='cl-message'> <div class='message-title'>안내방송</div> <div class='message-content'> "+msg+" </div> <div class='message-button'><a href='#0' id='messagebutton'>닫기</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href='#0' id='deletebutton'> "+option+" </a></div> </div>");
	$('#messagebutton').focus();
	
	$('#cl-message-veil').click(function(){
		$('#cl-message-veil').remove();
		$('#cl-message').remove();

	});
	
	$('#messagebutton').click(function(){
		$('#cl-message-veil').remove();
		$('#cl-message').remove();
	});
	
	$('#deletebutton').click(function(){
		$('#cl-message-veil').remove();
		$('#cl-message').remove();
		callGetAjax(move);
	});
	
}

//AJax 호출 이후 안내방송
function sendAjaxMessage(msg,work,address){

	$("body").append("<div id='cl-message-veil'></div> <div id='cl-message'> <div class='message-title'>Notification</div> <div class='message-content'> "+msg+" </div> <div class='message-button'><a href='#0' id='messagebutton'>확인</a></div> </div>");
	$('#messagebutton').focus();
	
	$('#cl-message-veil').click(function(){
		
		//move는 이동
		if(work == "move"){
			
			window.location.assign(address);
		
		//close는 닫기
		}else if(work == "close"){
			
			$('#cl-message-veil').remove();
			$('#cl-message').remove();
			
		//나머지
		}else{
			
		}
		
	});
	
	$('#messagebutton').click(function(){
		
		//move는 이동
		if(work == "move"){
			
			window.location.assign(address);
		
		//close는 닫기
		}else if(work == "close"){
			
			$('#cl-message-veil').remove();
			$('#cl-message').remove();
			
		//나머지
		}else{
			
		}
		
	});
}

//데이터 전송 전 유효 검사(모든 데이터에 적용 가능하는 일괄처리 장치) : text, email, id, pwd, password1, select, radio, isbn 순으로 검사.
function callValidation(str,val){
	
	var formdata = $(str+" [data-formdata]");
	var obj = $(str);

	//for 문으로 돌리면서 formdata 에 맞게 검사
	for(var i=0;i<formdata.length;i++){

		// 텍스트 형식 검사
		if(formdata.eq(i).data("formdata") == "text"){
			if(!formdata.eq(i).val().trim()){
				sendMessage('내용을 입력해 주십시오.',formdata.eq(i));
				return false;
			}
		}
		
		// 이메일 형식 검사
		if(formdata.eq(i).data("formdata") == "email"){
			if(!checkEmail(formdata.eq(i).val(),formdata.eq(i))){
				return false;
			}
		}
		
		// 로그인시 아이디(이메일) 검사
		if(formdata.eq(i).data("formdata") == "id"){
			if(!formdata.eq(i).val()){
				sendMessage('이메일을 입력해 주십시오.',formdata.eq(i));
				return false;
			}
		}
		
		// 로그인, 암호수정시 암호 검사
		if(formdata.eq(i).data("formdata") == "pwd"){
			if(!formdata.eq(i).val()){
				sendMessage('암호를 입력해 주십시오.',formdata.eq(i));
				return false;
			}
		}
		
		// 회원가입시 2개의 비밀번호 있을 때 검사	
		if(formdata.eq(i).data("formdata") == "password1"){
			if(formdata.eq(i).val() == formdata.eq(i+1).val()){
				if(!checkPassword(formdata.eq(i).val(),formdata.eq(i))){
					return false;
				}
			}else{
				sendMessage('암호가 일치하지 않습니다.',formdata.eq(i+1));
				return false;
			}
		}
		
		// 셀렉트 형식 검사
		if(formdata.eq(i).data("formdata") == "select"){
			if(!formdata.eq(i).val()){
				sendMessage('내용을 선택해 주십시오.',formdata.eq(i));
				return false;
			}
		}

		// range 형식 검사
		if(formdata.eq(i).data("formdata") == "range"){
			if(formdata.eq(i).val() == 0){
				sendMessage('범위를 선택해 주십시오.',formdata.eq(i));
				return false;
			}
		}
		
		// isbn 형식 검사
		if(formdata.eq(i).data("formdata") == "isbn"){
			if(!formdata.eq(i).val()){
				sendMessage('책 정보가 입력되지 않았습니다.<br /><br />ISBN 또는 ISSN 을 입력하신 후 우측의 SEARCH 버튼을 눌러 주십시오.',formdata.eq(i));
				return false;
			}
		}
    }
	
	
	//나는 로봇이 아닙니다.
	if($('.g-recaptcha')[0]){
		var response = grecaptcha.getResponse();
		if(response.length == 0){
			sendMessage('Please prove you are not a robot.',formdata.eq(i));
			return false;
		}
	}
	
	
	/*
	// 라디오 형식 검사
	if(!$("#cl-form [data-formdata]:checked").length){
		sendMessage('성별을 구분하여 주십시오..');
		return false;
	}
	*/
	
	//True이면 ajax로 처리
	if(val){
		//Ajax로 처리
		callAjax(obj);
	}

}

//이메일 검사
function checkEmail(str,val){
     /* check whether input value is included space or not  */
     if(str == ""){
    	 sendMessage("이메일을 입력해 주십시오.",val);
     	return false;
     }
     var retVal = checkSpace(str);
     if(retVal){
          sendMessage("이메일에 공백이 있습니다.",val);
         return false;
     }
     if(-1 == str.indexOf('.')){
     	 sendMessage("이메일을 정확하게 입력해 주십시오.",val);
        return false;
     }
     var isEmail = /[-!#$%&'*+\/^_~{}|0-9a-zA-Z]+(\.[-!#$%&'*+\/^_~{}|0-9a-zA-Z]+)*@[-!#$%&'*+\/^_~{}|0-9a-zA-Z]+(\.[-!#$%&'*+\/^_~{}|0-9a-zA-Z]+)*/;
     if(!isEmail.test(str)){
          sendMessage("이메일을 정확하게 입력해 주십시오.",val);
         return false;
     }
     if( str.length > 60 ){
          sendMessage("이메일을 정확하게 입력해 주십시오.",val);
         return false;
     }
     return true;
}

//공백이 있으면 true, 없으면 false
function checkSpace(str){
     if(str.search(/\s/) != -1){
    	 return true;
     } else {
    	 return false;
     }
}

//암호 검사
function checkPassword(str,val){
	var sep;
	var isPW = /^[A-Za-z0-9`\-=\\\[\];',\./~!@#\$%\^&\*\(\)_\+|\{\}:"<>\?]{8,16}$/;
	if(!isPW.test(str)){
		sendMessage("암호는 8~16자의 영문 대소문자와 숫자, 특수문자를 이용할 수 있습니다.",val);
		return false;
	}

	var checkNumber = str.search(/[0-9]/g);
	var checkEnglish = str.search(/[a-z]/ig);
	var checkSpecial = str.search(/[`\-=\\\[\];',\./~!@#\$%\^&\*\(\)_\+|\{\}:"<>\?]/ig);

	if(checkNumber <0 || checkEnglish <0 || checkSpecial <0){
		sendMessage("숫자, 영문자 그리고 특수문자를 혼용하여야 합니다.",val);
		return false;
	}
	if(/(\w)\1\1\1/.test(str)){
		sendMessage('111같은 문자를 4번 이상 사용하실 수 없습니다.',val);
		return false;
	}
	if($('#mbid').val()){
		if(str.search($('#mbid').val()) > -1){
			sendMessage("암호에 아이디가 포함되었습니다.",val);
			return false;
		}
	}
	return true;
}

//POST 방식의 Ajax 호출
function callAjax(val){
	
	// seriallize() : ie8이상. form 안에 있는 value를 정리해서 반환.
	var formData = val.serialize();
	var formAction = val.attr("action");
	
	//ajax 시작.
	$.ajaxSetup({
		cache : false
	  });
	
	$(document).ajaxError(function(){
	    alert("An error occured!");
	});
	
	$(document).ajaxStart(function(){
		$("body").append("<img src='" + $("#clpathhost").val() + "common/img/cl_wait.gif' id='cl-wait' />");
	});
	$(document).ajaxComplete(function(){
	    $('#cl-wait').remove();
	});
	
	$.ajax({
	    url:encodeURI(formAction),
	    dataType:'json',
	    type:'POST',
	    data:formData,
	    success:function(result){
	    	
	    	sendAjaxMessage(result.afterMessage.replace(/\\/gi, ""), result.afterWork, result.afterAddress);
	
	    },
	    error:function (xhr, ajaxOptions, thrownError){
	        alert(xhr.status);
	        alert(xhr.statusText);
	        alert(xhr.responseText);
	    }
	    
	});
}

function callSimulAjaxSfa(val){

    // seriallize() : ie8이상. form 안에 있는 value를 정리해서 반환.
    var formData = val.serialize();
    var formAction = val.attr("action");

    //ajax 시작.
    $.ajaxSetup({
        cache : false
      });

    $(document).ajaxError(function(){
        alert("An error occured!");
    });

    $(document).ajaxStart(function(){
        $("#cl-slmul-loading-veil").remove();
        $("body").append("<div id='cl-slmul-loading-veil'></div>");
        $("body").append("<img src='" + $("#clpathhost").val() + "common/img/cl_loading.gif' id='cl-loading' />");

    });
    $(document).ajaxComplete(function(){
        $("#cl-slmul-loading-veil").remove();
        $('#cl-loading').remove();
    });

    $.ajax({
        url:encodeURI(formAction),
        dataType:'json',
        type:'POST',
        data:formData,
        success:function(result){


            $('#cl-simul-sfa-graph').fadeIn();
            drawNetworkSfa(result);

        },
        error:function (xhr, ajaxOptions, thrownError){
            alert(xhr.status);
            alert(xhr.statusText);
            alert(xhr.responseText);
        }

    });
}


//POST 방식의 Simulation Ajax 호출
function callSimulAjax(val){
	
	// seriallize() : ie8이상. form 안에 있는 value를 정리해서 반환.
	var formData = val.serialize();
	var formAction = val.attr("action");
	
	//ajax 시작.
	$.ajaxSetup({
		cache : false
	  });
	
	$(document).ajaxError(function(){
	    alert("An error occured!");
	});
	
	$(document).ajaxStart(function(){
		$("#cl-slmul-loading-veil").remove();
		$("body").append("<div id='cl-slmul-loading-veil'></div>");
		$("body").append("<img src='" + $("#clpathhost").val() + "common/img/cl_loading.gif' id='cl-loading' />");
		
	});
	$(document).ajaxComplete(function(){
		$("#cl-slmul-loading-veil").remove();
	    $('#cl-loading').remove();
	});
	
	$.ajax({
	    url:encodeURI(formAction),
	    dataType:'json',
	    type:'POST',
	    data:formData,
	    success:function(result){
	    	
	    	//$('#cl-simul-attractor-graph').html("node1" + result['node1'] + "<br />node2" + result['node2'] + "<br />node3" + result['node3'] + "<br />node4" + result['node4'] + "<br />node5" + result['node5'] + "<br />target1" + result['target1'] + "<br />target1_on" + result['target1_on'] + "<br />target2" + result['target2'] + "<br />target2_on" + result['target2_on'] + "<br />input_nodes" + result['input_nodes'] + "<br />attractors" + result['attractors'] + "<br />state_key" + result['state_key']);
	    	
	    	$('#cl-simul-attractor-graph').fadeIn();
            drawNetwork(result);

            google.charts.load('upcoming', {packages:['corechart']});

            // Set a callback to run when the Google Visualization API is loaded. result를 파라미터로 보내주기 위
            google.charts.setOnLoadCallback(function() { attControlDrawChart(result); });
            google.charts.setOnLoadCallback(function() { attExpDrawChart(result); });

	
	    },
	    error:function (xhr, ajaxOptions, thrownError){
	        alert(xhr.status);
	        alert(xhr.statusText);
	        alert(xhr.responseText);
	    }
	    
	});
}

//GET 방식의 Ajax 호출
function callGetAjax(val){

	//ajax 시작.
	$.ajaxSetup({
		cache : false
	  });
	
	$(document).ajaxError(function(){
	    alert("An error occured!");
	});
	
	$(document).ajaxStart(function(){
		$("body").append("<img src='" + $("#clpathhost").val() + "common/img/cl_wait.gif' id='cl-wait' />");
	});
	$(document).ajaxComplete(function(){
	    $('#cl-wait').remove();
	});
	
	$.ajax({
	    url:encodeURI(val),
	    dataType:'json',
	    type:'GET',
	    success:function(result){
	    	
	  
	    	sendAjaxMessage(result.afterMessage.replace(/\\/gi, ""), result.afterWork, result.afterAddress);
	    	
	
	    },
	    error:function (xhr, ajaxOptions, thrownError){
	        alert(xhr.status);
	        alert(xhr.statusText);
	        alert(xhr.responseText);
	    }
	    
	});
}

//GET 방식의 Simulation Ajax 호출
function callGetSimulAjax(val,mode){
	
	//ajax 시작.
	$.ajaxSetup({
		cache : false
	  });
	
	$(document).ajaxError(function(){
	    alert("An error occured!");
	});
	
	$(document).ajaxStart(function(){
		$("#cl-slmul-loading-veil").remove();
		$("body").append("<div id='cl-slmul-loading-veil'></div>");
		$("body").append("<img src='" + $("#clpathhost").val() + "common/img/cl_loading.gif' id='cl-loading' />");
		
	});
	$(document).ajaxComplete(function(){
		$("#cl-slmul-loading-veil").remove();
	    $('#cl-loading').remove();
	});
	
	$.ajax({
	    url:encodeURI(val),
	    dataType:'json',
	    type:'GET',
	    success:function(result){
	    	
	    	//Dream2015
	    	if(mode == "dream2015_cellline"){
	    		
	    		//해당 Select 박스의 option이 1이상이면 그 이하의 종속 selects를 reset 한다.
	    		if($('#cl-simul-dream2015-cellline option').size() > 1){
	    			$('#cl-simul-dream2015-cellline option').remove();
	    			$('#cl-simul-dream2015-cellline').append("<option value=''>--- Module ---</option>");
	    			
	    			$('#cl-simul-dream2015-drug1 option').remove();
	    			$('#cl-simul-dream2015-drug1').append("<option value=''>--- Drug 1 ---</option>");
	    			
	    			$('#cl-simul-dream2015-drug2 option').remove();
	    			$('#cl-simul-dream2015-drug2').append("<option value=''>--- Drug 2 ---</option>");
	    		}
	    		
	    		//Ajax로 받아온 JSON data format 파일을 for문으로 돌려 option으로 넣는다. 
	    		for(i = 0; i < result.length; i++){
			    	$('#cl-simul-dream2015-cellline').append("<option value='" + result[i].CELL_LINE + "'>" + result[i].CELL_LINE + "</option>");
		    	}
	    		
	    		//dream2015 div가 보이도록.
				$("#cl-simul-dream2015").fadeIn();
				
				//cellline으로 포커스 이동.
				$("#cl-simul-dream2015-cellline").focus();
				
	    	}else if(mode == "dream2015_drug1"){
	    		
	    		//해당 Select 박스의 option이 1이상이면 그 이하의 종속 selects를 reset 한다.
	    		if($('#cl-simul-dream2015-drug1 option').size() > 1){
	    			$('#cl-simul-dream2015-drug1 option').remove();
	    			$('#cl-simul-dream2015-drug1').append("<option value=''>--- Drug 1 ---</option>");
	    			
	    			$('#cl-simul-dream2015-drug2 option').remove();
	    			$('#cl-simul-dream2015-drug2').append("<option value=''>--- Drug 2 ---</option>");
	    			
	    		}
	    		
	    		//Ajax로 받아온 JSON data format 파일을 for문으로 돌려 option으로 넣는다.
	    		for(i = 0; i < result.length; i++){
			    	$('#cl-simul-dream2015-drug1').append("<option value='" + result[i].COMPOUND_A + "'>" + result[i].COMPOUND_A + " (" + result[i].TARGET + ")</option>");
		    	}
	    		
	    		//cellline으로 포커스 이동.
	    		$("#cl-simul-dream2015-drug1").focus();
	    		
	    	}else if(mode == "dream2015_drug2"){
	    		
	    		//해당 Select 박스의 option이 1이상이면 그 이하의 종속 selects를 reset 한다.
	    		if($('#cl-simul-dream2015-drug2 option').size() > 1){
	    			$('#cl-simul-dream2015-drug2 option').remove();
	    			$('#cl-simul-dream2015-drug2').append("<option value=''>--- Drug 2 ---</option>");
	    		}
	    		
	    		//Ajax로 받아온 JSON data format 파일을 for문으로 돌려 option으로 넣는다.
	    		for(i = 0; i < result.length; i++){
			    	$('#cl-simul-dream2015-drug2').append("<option value='" + result[i].COMPOUND_B + "'>" + result[i].COMPOUND_B + " (" + result[i].TARGET + ")</option>");
		    	}
	    		
	    		//cellline으로 포커스 이동.
	    		$("#cl-simul-dream2015-drug2").focus();
	    		
	    	}else if(mode == "dream2015_graph"){
	    		// Fadein으로 showing
	    		$("#cl-simul-dream2015-graph").fadeIn();
	    		
	    		// Load the Visualization API and the piechart package.
				google.charts.load('upcoming', {packages:['corechart']});
				
				// Set a callback to run when the Google Visualization API is loaded. result를 파라미터로 보내주기 위해 아래와 같이 사용.
				google.charts.setOnLoadCallback(function() { drawChart(result); });
	    		
	    		var rowlength = result["rows"].length; //row수
	    		var total = 0; //모두 더한 값 
	    		var totalSubtractMean = 0; 
	    		var mean; //평균 
	    		var variance; //분산
	    		var deviation; //표준편차
	    		
	    		//값 다 더하기
	    		for(i = 0; i < rowlength; i++){
	    			total += Number(result["rows"][i]["c"][1]["v"]);
		    	}
	    		
	    		//평균 구하기
	    		mean = Number(total/rowlength);
	    		//소수점 두 자리
	    		meanRound = Math.round(mean*100)/100;
	    		
	    		for(j = 0; j < rowlength; j++){
	    			totalSubtractMean += Math.pow(Number(result["rows"][j]["c"][1]["v"]) - mean, 2);
		    	}
	    		
	    		variance = totalSubtractMean/rowlength;
	    		deviation = Math.sqrt(variance);
	    		deviationRound = Math.round(deviation*100)/100;
	    		
	    		$("#meandeviation").html("Mean : "+meanRound+"<br />Standard Deviation : "+deviationRound);
	    		
	    	//Attractor
	    	}else if(mode == "attractor_target1"){
	    		
	    		//해당 Select 박스의 option이 1이상이면 그 이하의 종속 selects를 reset 한다.
	    		if($('#cl-simul-attractor-target1 option').size() > 1){
	    			$('#cl-simul-attractor-target1 option').remove();
	    			$('#cl-simul-attractor-target1').append("<option value=''>--- target 1 ---</option>");
	    			
	    			$('#cl-simul-attractor-target2 option').remove();
	    			$('#cl-simul-attractor-target2').append("<option value=''>--- target 2 ---</option>");
	    		}
	    		
	    		$('#cl-simul-attractor-target1').append("<option value='free'>선택안함</option>");
	    		
	    		//Ajax로 받아온 JSON data format 파일을 for문으로 돌려 option으로 넣는다. 
	    		for(i = 0; i < result.length; i++){
			    	$('#cl-simul-attractor-target1').append("<option value='" + result[i].target1 + "'>" + result[i].target1 + "</option>");
		    	}
	    		
	    		//dream2015 div가 보이도록.
				$("#cl-simul-attractor").fadeIn();
				
				//cellline으로 포커스 이동.
				$("#cl-simul-attractor-target1").focus();
	    		
	    	}else if(mode == "attractor_target2"){
	    		
	    		//해당 Select 박스의 option이 1이상이면 그 이하의 종속 selects를 reset 한다.
	    		if($('#cl-simul-attractor-target2 option').size() > 1){
	    			$('#cl-simul-attractor-target2 option').remove();
	    			$('#cl-simul-attractor-target2').append("<option value=''>--- target 2 ---</option>");
	    		}
	    		
	    		$('#cl-simul-attractor-target2').append("<option value='free'>선택안함</option>");
	    		
	    		//Ajax로 받아온 JSON data format 파일을 for문으로 돌려 option으로 넣는다. 
	    		for(i = 0; i < result.length; i++){
			    	$('#cl-simul-attractor-target2').append("<option value='" + result[i].target2 + "'>" + result[i].target2 + "</option>");
		    	}
	    		
				//target2로 포커스 이동.
				$("#cl-simul-attractor-target2").focus();
	    		
			//SFA
	    	}else if(mode == "sfa_target1"){
	    		
	    		//해당 Select 박스의 option이 1이상이면 그 이하의 종속 selects를 reset 한다.
	    		if($('#cl-simul-sfa-target1 option').size() > 1){
	    			$('#cl-simul-sfa-target1 option').remove();
	    			$('#cl-simul-sfa-target1').append("<option value=''>--- target 1 ---</option>");
	    			
	    			$('#cl-simul-sfa-target2 option').remove();
	    			$('#cl-simul-sfa-target2').append("<option value=''>--- target 2 ---</option>");
	    		}
	    		
	    		$('#cl-simul-sfa-target1').append("<option value='free'>선택안함</option>");
	    		
	    		//Ajax로 받아온 JSON data format 파일을 for문으로 돌려 option으로 넣는다. 
	    		for(i = 0; i < result.length; i++){
			    	$('#cl-simul-sfa-target1').append("<option value='" + result[i].target1 + "'>" + result[i].target1 + "</option>");
		    	}
	    		
	    		//dream2015 div가 보이도록.
				$("#cl-simul-sfa").fadeIn();
				
				//cellline으로 포커스 이동.
				$("#cl-simul-sfa-target1").focus();
	    		
	    	}else if(mode == "sfa_target2"){
	    		
	    		//해당 Select 박스의 option이 1이상이면 그 이하의 종속 selects를 reset 한다.
	    		if($('#cl-simul-sfa-target2 option').size() > 1){
	    			$('#cl-simul-sfa-target2 option').remove();
	    			$('#cl-simul-sfa-target2').append("<option value=''>--- target 2 ---</option>");
	    		}
	    		
	    		$('#cl-simul-sfa-target2').append("<option value='free'>선택안함</option>");
	    		
	    		//Ajax로 받아온 JSON data format 파일을 for문으로 돌려 option으로 넣는다. 
	    		for(i = 0; i < result.length; i++){
			    	$('#cl-simul-sfa-target2').append("<option value='" + result[i].target2 + "'>" + result[i].target2 + "</option>");
		    	}
	    		
				//target2로 포커스 이동.
				$("#cl-simul-sfa-target2").focus();
	    		
	    	}
	    	
	    },
	    
	    error:function (xhr, ajaxOptions, thrownError){
	        alert(xhr.status);
	        alert(xhr.statusText);
	        alert(xhr.responseText);
	    }
	    
	});
}

//google chart 그리기.
function drawChart(result) {
	var data = new google.visualization.DataTable(result);

	  var options = {
	    title: 'Prediction',
	    legend: { position: 'none' },
	    colors: ['#1A70DB'],
	  };

	  var chart = new google.visualization.Histogram(document.getElementById('example1'));

	  chart.draw(data, options);
	}

function attControlDrawChart(result) {
    var data = new google.visualization.DataTable(result['att_control']);

      var options = {
        title: 'Attractors - control',
        legend: { position: 'none' },
        colors: ['#1A70DB'],
        vAxis: {
            minValue: 0,
            maxValue: 1
        }
      };

      var chart = new google.visualization.ColumnChart(document.getElementById('atthist_control'));

      chart.draw(data, options);
    }

function attExpDrawChart(result) {
    var data = new google.visualization.DataTable(result['att_exp']);

      var options = {
        title: 'Attractors - simulation',
        legend: { position: 'none' },
        colors: ['#1A70DB'],
        vAxis: {
            minValue: 0,
            maxValue: 1
        }
      };

      var chart = new google.visualization.ColumnChart(document.getElementById('atthist_exp'));

      chart.draw(data, options);
    }

//vis
var att;
var att_con;
var network;
function drawNetwork(result) {
    // load the JSON file containing the Gephi network.
    //var gephiJSON = loadJSON("./fumia.json"); // code in importing_from_gephi.
    var gephiJSON = netfile; // code in importing_from_gephi.

    // you can customize the result like with these options. These are explained below.
    // These are the default options.
    var parserOptions = {
        edges: {
            inheritColors: false
        },
        nodes: {
            fixed: true,
            parseColor: false
        }
    }

    // parse the gephi file to receive an object
    // containing nodes and edges in vis format.
    var parsed = vis.network.convertGephi(gephiJSON, parserOptions);

    // provide data in the normal fashion
    var data = {
        nodes: new vis.DataSet(parsed.nodes),
        edges: new vis.DataSet(parsed.edges)
    };

    // Node color
    nodeIds = data.nodes.getIds()
    for (var i = 0; i < nodeIds.length; i++) {
        var temp = data.nodes.get(nodeIds[i]);
        temp.color = {
            background: '#3333FF',
            border: '#3333FF'
        }
        data.nodes.update(temp);
    }

    if (result['target1']!='') {
        S = result['target1'].slice(2);
        var selNode = data.nodes.get(String(S));
        selNode.color = { 
            background: '#CC3333',
            border: '#CC3333'
        }   
        data.nodes.update(selNode);
    }
    if (result['target2']!='') {
        S = result['target2'].slice(2);
        var selNode = data.nodes.get(String(S));
        selNode.color = {
            background: '#CC3333',
            border: '#CC3333'
        }
        data.nodes.update(selNode);
    }
    //data.nodes[0]['color']['background'] = '#00ff00';
    //data.nodes[0]['color']['border'] = '#00ff00';


    // Edge color
    //var selEdge = data.edges.get('134');
    //selEdge.color = '#ff0000';
    //data.edges.update(selEdge);
    //data.edges[0]['color'] = '#ff0000';
    edgeIds = data.edges.getIds()
    for (var i = 0; i < edgeIds.length; i++) {
        var temp = data.edges.get(edgeIds[i]);
        temp.arrows = 'to';
        data.edges.update(temp);
    }
    // Edge scaling
    temp = data.edges.get(0);
    //temp.from == 'node1' & temp.to == 'node2';
    temp.value = 0.3;
    //data.edges.update(temp);

    // create a network
    var options = {
        nodes: {
            font: {
                color: '#ffffff'
            },
            borderWidthSelected: 4
        },
        edges: {
            color: '#000000'
        },
        interaction: {
            // longheld click or control-click
            multiselect: true,
            hover: true
        }
    };
    var container = document.getElementById('mynetwork');
    var network = new vis.Network(container, data, options);

    // network load progress bar
    network.on("stabilizationProgress", function(params) {
        var maxWidth = 496;
        var minWidth = 20;
        var widthFactor = params.iterations/params.total;
        var width = Math.max(minWidth,maxWidth * widthFactor);
        document.getElementById('bar').style.width = width + 'px';
        document.getElementById('text').innerHTML = Math.round(widthFactor*100) + '%';
    });
    network.once("stabilizationIterationsDone", function() {
        document.getElementById('text').innerHTML = '100%';
        document.getElementById('bar').style.width = '496px';
        document.getElementById('loadingBar').style.opacity = 0;
        // really clean the dom element
        setTimeout(function () {document.getElementById('loadingBar').style.display = 'none';}, 500);
    });

    var selnodes = [];
    // event catch
    network.on("click", function (params) {
        //console.log(JSON.stringify(params));
        console.log(params['nodes']);
        selnodes = params['nodes'];
        //console.log(params['edges']);
    });
    this.att = result['att_exp'];
    this.att_con = result['att_control'];
    this.network = data;
}



var signal;
var network;
function drawNetworkSfa(result) {
    // load the JSON file containing the Gephi network.
    //var gephiJSON = loadJSON("./fumia.json"); // code in importing_from_gephi.
    var gephiJSON = netfile_sfa; // code in importing_from_gephi.

    // you can customize the result like with these options. These are explained below.
    // These are the default options.
    var parserOptions = {
        edges: {
            inheritColors: false
        },
        nodes: {
            fixed: true,
            parseColor: false
        }
    }

    // parse the gephi file to receive an object
    // containing nodes and edges in vis format.
    var parsed = vis.network.convertGephi(gephiJSON, parserOptions);

    // provide data in the normal fashion
    var data = {
        nodes: new vis.DataSet(parsed.nodes),
        edges: new vis.DataSet(parsed.edges)
    };

    // Node color
    nodeIds = data.nodes.getIds()
    for (var i = 0; i < nodeIds.length; i++) {
        var temp = data.nodes.get(nodeIds[i]);
        temp.color = {
            background: '#3333FF',
            border: '#3333FF'
        }
        data.nodes.update(temp);
    }

    if (result['drug1_target']!='') {
        S = result['drug1_target'];
        var selNode = data.nodes.get(String(S));
        selNode.color = { 
            background: '#CC3333',
            border: '#CC3333'
        }   
        data.nodes.update(selNode);
    }
    if (result['drug2_target']!='') {
        S = result['drug2_target'];
        var selNode = data.nodes.get(String(S));
        selNode.color = {
            background: '#CC3333',
            border: '#CC3333'
        }
        data.nodes.update(selNode);
    }
    //data.nodes[0]['color']['background'] = '#00ff00';
    //data.nodes[0]['color']['border'] = '#00ff00';


    // Edge color
    //var selEdge = data.edges.get('134');
    //selEdge.color = '#ff0000';
    //data.edges.update(selEdge);
    //data.edges[0]['color'] = '#ff0000';
    edgeIds = data.edges.getIds()
    for (var i = 0; i < edgeIds.length; i++) {
        var temp = data.edges.get(edgeIds[i]);
        temp.arrows = 'to';
        temp.width = 3;
        //temp.value = 2;
        data.edges.update(temp);
    }
    // Edge scaling
    signal_flow = result['signal'];
    signal_len = signal_flow.length;
    for (var i = 0; i < signal_len; i++) {
        for (var j = 0; j < edgeIds.length; j++) {
            var temp = data.edges.get(edgeIds[j]);
            if (temp.from == signal_flow[i][0] & temp.to == signal_flow[i][1]) {
                //temp.value = 2 * ((10**signal_flow[i][2])**5);
                temp.width = 3 * ((10**signal_flow[i][2])**4);
                data.edges.update(temp);
                break;
            }
        }
    }

    // create a network
    var options = {
        nodes: {
            font: {
                color: '#ffffff'
            },
            borderWidthSelected: 4
        },
        edges: {
            color: '#000000'
        },
        interaction: {
            // longheld click or control-click
            multiselect: true,
            hover: true
        }
    };
    var container = document.getElementById('mynetwork_sfa');
    var network = new vis.Network(container, data, options);

    // network load progress bar
    network.on("stabilizationProgress", function(params) {
        var maxWidth = 496;
        var minWidth = 20;
        var widthFactor = params.iterations/params.total;
        var width = Math.max(minWidth,maxWidth * widthFactor);
        document.getElementById('bar').style.width = width + 'px';
        document.getElementById('text').innerHTML = Math.round(widthFactor*100) + '%';
    });
    network.once("stabilizationIterationsDone", function() {
        document.getElementById('text').innerHTML = '100%';
        document.getElementById('bar').style.width = '496px';
        document.getElementById('loadingBar').style.opacity = 0;
        // really clean the dom element
        setTimeout(function () {document.getElementById('loadingBar').style.display = 'none';}, 500);
    });

    var selnodes = [];
    // event catch
    network.on("click", function (params) {
        //console.log(JSON.stringify(params));
        console.log(params['nodes']);
        selnodes = params['nodes'];
        //console.log(params['edges']);
    });
    this.signal = result['signal'];
    this.network = data;
}

