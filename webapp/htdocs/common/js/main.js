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
	
	//Ajax를 이용하는 login-form 데이터 전송.
	$('#cl-form-login').submit(function(){

		//데이터 일괄 검사
		callValidation('#cl-form-login',true);
		return false;
		
	});
	
	//로그인 클릭하면.
	$('.cl-btn-inner').click(function(){

		sendMessage("입력이 완료 되었습니다.");
			
	});
	
	//로그인 클릭하면.
	$('.login-open').click(function(){

		sendMessage("로그인");
			
	});
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
	
	//로그인 창에서 뜬다면.
	if($('#cl-login-veil').length){
		var loginTrue = true;
		$('#cl-login-veil').remove();
	}
	
	$("body").append("<div id='cl-message-veil'></div> <div id='cl-message'> <div class='message-title'>안내방송</div> <div class='message-content'> "+msg+" </div> <div class='message-button'><a href='#0' id='messagebutton'>닫기</a></div> </div>");
	$('#messagebutton').focus();
	
	$('#cl-message-veil').click(function(){
		$('#cl-message-veil').remove();
		$('#cl-message').remove();
		if(loginTrue){
			$("body").append("<div id='cl-login-veil'></div>");
			
			$('#cl-login-veil').click(function(){
				$('#cl-login-veil').remove();
				$('#cl-login').remove();
				$('#cl-form-login').remove();
			});
			
		}
		val.focus();
	});
	
	$('#messagebutton').click(function(){
		$('#cl-message-veil').remove();
		$('#cl-message').remove();
		if(loginTrue){
			$("body").append("<div id='cl-login-veil'></div>");
			
			$('#cl-login-veil').click(function(){
				$('#cl-login-veil').remove();
				$('#cl-login').remove();
				$('#cl-form-login').remove();
			});
		}
		val.focus();
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

//AJax 호출 이후 안내방송
function sendAjaxMessage(msg,work,address){

	$("body").append("<div id='cl-message-veil'></div> <div id='cl-message'> <div class='message-title'>안내방송</div> <div class='message-content'> "+msg+" </div> <div class='message-button'><a href='#0' id='messagebutton'>확인</a></div> </div>");
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