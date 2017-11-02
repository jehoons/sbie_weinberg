jQuery(document).ready(function($){
	//open-close submenu on mobile
	$('.main-nav').on('click', function(event){
		if($(event.target).is('.main-nav')) $(this).children('ul').toggleClass('is-visible');
	});
	
	//환자추가
	$('#paitent-add').click(function(){
		$("body").append("<div id='patient-add-veil'></div> <form action='" + $("#phpself").val() + "?module=analysis&act=write_work.php' method='POST' target='_self' accept-charset='UTF-8' enctype='application/x-www-form-urlencoded' autocomplete='on' id='patient-add-form'> <div id='patient-add-box'> <div class='patient-add-title'>환자추가</div> <div class='patient-add-content'> <table style='width: 100%;'> <colgroup> <col width='140px'> <col> </colgroup> <tr style='height:70px;'> <td>환자명</td> <td><input type='text' name='patient' class='text' placeholder=''   data-formdata='text'></td> </tr> <tr style='height:50px;'> <td>암종</td> <td><input type='radio' name='cancertype' value='colon' checked>대장암 <input type='radio' name='cancertype' value='breast' checked>유방암 <input type='radio' name='cancertype' value='lung' checked>폐암</td> </tr> <tr style='height:70px;'> <td>유전자발현량</td> <td><input type='text' name='expression' class='text' placeholder='' data-formdata='text'></td> </tr> <tr style='height:70px;'> <td>돌연변이</td> <td><input type='text' name='mutation' class='text' placeholder='' data-formdata='text'></td> </tr> <tr style='height:45px;'> <td>CNV</td> <td><input type='text' name='cnv' class='text' placeholder='' data-formdata='text'></td> </tr> </table> </div> <div class='patient-add-button'><input type='submit' id='patient-add-submit' value='확인'> <a href='#0' id='patient-add-cancel'>닫기</a></div> </div> </form>");
		$('#patient-add-veil').click(function(){
			$('#patient-add-veil').remove();
			$('#patient-add-box').remove();
			$('#patient-add-form').remove();
		});
		$('#patient-add-cancel').click(function(){
			$('#patient-add-veil').remove();
			$('#patient-add-box').remove();
			$('#patient-add-form').remove();
		});
		$('#patient-add-form').submit(function(){
			//데이터 일괄 검사
			if(callValidation('#patient-add-form',false) == false){
				return false;
			}
		});
	});
	
	//삭제
	$('.delete-open').click(function(){
		 sendCheckMessage("삭제된 자료는 복구가 불가능합니다.<br /><br />삭제하시겠습니까?",$(this).data("urldata"),"삭제");
	})
});

//안내
function sendMessage(msg,val){
	
	//환자추가 창에서 뜬다면
	if($('#patient-add-veil').length){
		var PatientAddTrue = true;
		$('#patient-add-veil').remove();
	}
	
	$("body").append("<div id='message-veil'></div> <div id='message-box'> <div class='message-title'>안내</div> <div class='message-content'> "+msg+" </div> <div class='message-button'><a href='#0' id='message-close'>닫기</a></div> </div>");
	$('#message-close').focus();
	
	$('#message-veil').click(function(){
		$('#message-veil').remove();
		$('#message-box').remove();
		if(PatientAddTrue){
			$("body").append("<div id='patient-add-veil'></div>");
			
			$('#patient-add-veil').click(function(){
				$('#patient-add-veil').remove();
				$('#patient-add-box').remove();
				$('#patient-add-form').remove();
			});
			
		}
		val.focus();
	});
	
	$('#message-close').click(function(){
		$('#message-veil').remove();
		$('#message-box').remove();
		if(PatientAddTrue){
			$("body").append("<div id='patient-add-veil'></div>");
			
			$('#patient-add-veil').click(function(){
				$('#patient-add-veil').remove();
				$('#patient-add-box').remove();
				$('#patient-add-form').remove();
			});
		}
		val.focus();
	});	
}

//체크 안내
function sendCheckMessage(msg,move,option){
	
	$("body").append("<div id='message-veil'></div> <div id='message-box'> <div class='message-title'>안내</div> <div class='message-content'> "+msg+" </div> <div class='message-button'><a href='#0' id='message-close'>닫기</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href='#0' id='message-delete'> "+option+" </a></div> </div>");
	$('#message-close').focus();
	
	$('#message-veil').click(function(){
		$('#message-veil').remove();
		$('#message-box').remove();
	});
	
	$('#message-close').click(function(){
		$('#message-veil').remove();
		$('#message-box').remove();
	});
	
	$('#message-delete').click(function(){
		$('#message-veil').remove();
		$('#message-box').remove();
		getCallAjax(move);
	});
	
}

//AJax 호출 이후 안내
function sendAjaxMessage(msg,work,content,how){
	$("body").append("<div id='message-veil'></div> <div id='message-box'> <div class='message-title'>안내</div> <div class='message-content'> "+msg+" </div> <div class='message-button'><a href='#0' id='message-close'>확인</a></div> </div>");
	$('#message-close').focus();
	
	$('#message-veil').click(function(){
		//move는 이동
		if(work == "move"){
			window.location.assign(content);
		//close는 닫기
		}else if(work == "close"){
			$('#message-veil').remove();
			$('#message-box').remove();
		//나머지는 add
		}else{
			$('#message-veil').remove();
			$('#message-box').remove();
			if(how == "append"){
				$(work).append(content.replace(/\\r\\n/g,'<br />'));
			}else if(how == "html"){
				$(work).html(content.replace(/\\r\\n/g,'<br />'));
			}
		}
	});
	
	$('#message-close').click(function(){
		//move는 이동
		if(work == "move"){
			window.location.assign(content);
		//close는 닫기
		}else if(work == "close"){
			$('#message-veil').remove();
			$('#message').remove();
		//나머지는 add
		}else{
			$('#message-veil').remove();
			$('#message').remove();
			if(how == "append"){
				$(work).append(content.replace(/\\r\\n/g,'<br />'));
			}else if(how == "html"){
				$(work).html(content.replace(/\\r\\n/g,'<br />'));
			}
			
		}
		
	});
}

//정규식
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
		postCallAjax(obj);
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
function postCallAjax(val){
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
		$("body").append("<img src='" + $("#clpathhost").val() + "common/img/wait.gif' id='wait' />");
	});
	$(document).ajaxComplete(function(){
	    $('#wait').remove();
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

//GET 방식의 Ajax 호출
function getCallAjax(val){
	//ajax 시작.
	$.ajaxSetup({
		cache : false
	  });
	$(document).ajaxError(function(){
	    alert("An error occured!");
	});
	$(document).ajaxStart(function(){
		$("body").append("<img src='" + $("#clpathhost").val() + "common/img/wait.gif' id='wait' />");
	});
	$(document).ajaxComplete(function(){
	    $('#wait').remove();
	});
	$.ajax({
	    url:encodeURI(val),
	    dataType:'json',
	    type:'GET',
	    success:function(result){
		    sendAjaxMessage(result.afterMessage, result.afterWork, result.afterContent, result.afterHow);
	    },
	    error:function (xhr, ajaxOptions, thrownError){
	        alert(xhr.status);
	        alert(xhr.statusText);
	        alert(xhr.responseText);
	    }
	});
}