<?php
/* --------------------------------

config/function.php
간단한 php 함수 설정.

-------------------------------- */

// __CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

//이동하기.
function gotoUrl($url){
	echo "
<!doctype html>
<html lang='en' class='no-js'>
<head>
<meta charset='UTF-8'>
<meta http-equiv='refresh' content='0;url=$url'>
</head>
<html>
";
	exit;
}

//alert 띄우기.
function alertScript($msg){
	if(!$msg) return;
	echo '<script type="text/javascript">alert("'.$msg.'");</script>';
}

//file_get_contents 을 보안상 안 쓰기 위하여 curl 로 외부 사이트 파싱
function curlGetcontents($url){
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
	$g = curl_exec($ch);
	curl_close($ch);
	
	return $g;
}

//네이버에서 isbn, issn이 띄어쓰기로 구분되어 오기때문에 이것을 나누어 2개의 변수에 넣는다.
function isbnisbnsort($ib_isbn){
	
	global $ib_isbnissn1;
	global $ib_isbnissn2;
	
	$ib_isbn = explode(" ", $ib_isbn);
	
	if(count($ib_isbn) == 1){
		
		$ib_isbnissn1 = $ib_isbn[0];
		$ib_isbnissn2 = $ib_isbn[0];
		
	}else{
		
		$ib_isbnissn1 = $ib_isbn[0];
		$ib_isbnissn2 = $ib_isbn[1];
		
	}
}

//$_POST, $_GET 데이터 가공.
function dataCheck($str){
	//슬래쉬 붙이기. 5.4부터는 디폴트 아니라서 그렇다.
	//$str = addslashes($str);
	//인젝션 공격 대비 특수문자 이스케이프 시키기.
	$str = mysql_escape_string($str);
	//html tag 제거
	$str = filter_var($str, FILTER_SANITIZE_STRING);
	
	return $str;
}

//데이터 보여주기.
function dataShow($str){
	//슬래쉬 없애서 데이터 보여주기.
	$str = stripslashes("$str");

	return $str;
}

//단일 또는 다중 검색어 가공.
function getSearch($search_column, $search_str, $search_operator="and"){

	//예) (INSTR(ib_title, '한국인') and INSTR(ib_title, '밑반찬')) OR (INSTR(bk_review, '한국인') and INSTR(bk_review, '밑반찬'))
	//띄어쓰기로 구분한다.
	$search_column = trim($search_column);
	$search_column = explode(" ", $search_column);
	
	//띄어쓰기로 구분한다.
	$search_str = trim($search_str);
	$search_str = explode(" ", $search_str);

	$str2 = "";
	$opt2 = "";
	for($a=0;$a<count($search_column);$a++){
		
		$str = "";
		$opt = "";
		for($i=0;$i<count($search_str);$i++){
	
			$str .= $opt;
			$str .= "";
	
			if(preg_match("/[a-zA-Z]/", $search_str[$i])){ 
				$str .= "INSTR(LOWER($search_column[$a]), LOWER('$search_str[$i]'))";
			}else{
				$str .= "INSTR($search_column[$a], '$search_str[$i]')";
			}
	
			$str .= "";
			$opt = " $search_operator ";
	
		}
		
		$str2 .= $opt2;
		$str2 .= "(";
		$str2 .= $str;
		$str2 .= ")";
		$opt2 = " OR ";
		
	}	

	return "(".$str2.")";

}

// 문자열 자르기
function stringCut($str,$limit) {

	mb_internal_encoding('UTF-8');

	if (mb_strlen($str)>$limit) {

		$str = mb_substr($str,0,$limit).'...';
	  
	}else{

		$str = $str;
	}

	return $str;
}

// 천단위 콤마(,) 표시
function thousandNum($num){

	return number_format($num);

}

// 천단위 콤마(,) 표시
function levelShow($num,$score){

	//$num은 활동점수
	
	for ($x = 1; $x <= 100; $x++) {
	   
		$total = $x * ($x * 5 + 30);
		
		if($total > $num){
			break;
		}
		
		
	}
	
	if($score){
		return $x."<span style='font-size:1.0rem;'> (".thousandNum($num).")</span>";
	}else{
		return $x;
	}
	

}

// 검색어 표시
function searchStrExp($searchStr, $content){
	
	return str_ireplace($searchStr,"<span style='background-color : #FFF600; color: #000000; font-weight: 900;'>$searchStr</span>",$content);
	
}

// 
function dateDiff($startdate,$enddate){
	
	$nowtime=strtotime($startdate);
	$detailtime=strtotime($enddate);
	
	$cha=$detailtime - $nowtime;
	return $days= ceil($cha/60/60/24);
	
}
?>