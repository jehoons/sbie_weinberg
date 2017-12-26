<?php
if(!defined('__CL__')) exit();

$rowid = $_GET["pt_rowid"];

//데이터가 넘어왔는지 확인.
if($rowid){

	//DELETE 실행.
	$sql = "DELETE FROM patient WHERE pt_rowid = '$rowid'";

	//책 업데이트 성공.
	if ($conn->query($sql) === TRUE) {
			
		$afterMessage = "삭제를 완료하였습니다.";
		$afterWork = "move";
		$afterContent = htmlspecialchars($_SERVER["PHP_SELF"])."?module=analysis&act=list.php&pagenum=".$_GET["pagenum"]."&searchColumn=".$_GET["searchColumn"]."&searchStr=".$_GET["searchStr"]."&orderby=".$_GET["orderby"]."&orderopt=".$_GET["orderopt"];
		$afterHow = "empty";
			
		//책 업데이트 실패.
	} else {
		$afterMessage = "데이터베이스에 문제가 발생하여<br />데이터가 정상적으로 등록되지 않았습니다.<br />다시 시도해 주십시오.<br /><br />불편을 끼쳐 드려 죄송합니다.";
		$afterWork = "close";
		$afterContent = "empty";
		$afterHow = "empty";
	}
	
	//{"a":1,"b":2,"c":3,"d":4,"e":5} 식으로 만들기.
	$arr = array ('afterMessage'=>$afterMessage,'afterWork'=>$afterWork,'afterContent'=>$afterContent,'afterHow'=>$afterHow);
	
	//json으로 변환.
	echo json_encode($arr);

}
?>