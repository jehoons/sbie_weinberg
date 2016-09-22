<?php
/* --------------------------------

config/page.php
모든 페이징기법 설정.

-------------------------------- */

//  __CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();

//페이징 세팅
function setPage($select, $content_volume, $page_volume){
	
	global $conn;					// 데이터베이스 객체를 function 안에서도 사용하기 위해.
	global $cnt;					// 한 페이지당 보여지는 쿼리한 실제 row수.
	global $recordsu;				// 쿼리한 총 row 수.
	global $rpp;					// 한 페이지당 보여주는 최대치 row 수.
	global $startpoint;			// 쿼리 시작점 LIMIT 시작점.
	global $pagegroup;			// 보여줄 페이징 수.
	global $pagesu;				// 총 페이지 수. 
	global $pagenum;			// 현재 페이지 위치. 0부터 시작이다. 0이 1페이지다.
	
	global $pagegroupnum;	// 현재 페이징이 소속된 그룹 넘버. 2가 되면 현재 페이지에서 다음 버튼을 누른 것이다.
	global $startpage;			// 시작 페이지 위치.
	global $endpage;			// 마지막 페이지 위치.
	
	global $sql;
	global $result;
	
	global $folder_rowid;
	
	$pagenum = $_GET[pagenum];

	$sql = $select;

	//총 row 수.
	$recordsu = $result->num_rows;
	$rpp = $content_volume;
	$pagegroup = $page_volume;
	$pagesu = ceil($recordsu/$rpp);
	$startpoint = $pagenum*$rpp;

	//LIMIT 는 0부터 시작점 예) LIMIT 0,10 : 0부터 10개까지 들고 오너라.
	$sql = $sql." limit $startpoint,$rpp";
	$result = $conn->query($sql);
	$cnt = $result->num_rows;

}

function getPage(){

	global $conn;
	global $cnt;
	global $recordsu;
	global $rpp;
	global $startpoint;
	global $pagegroup;
	global $pagesu;
	global $pagenum;
	
	global $pagegroupnum;
	global $startpage;
	global $endpage;
	
	global $sql;
	global $result;
	
	global $folder_rowid;
	
?>
<nav role="navigation">
	<div class="cd-pagination no-space">
	<?php 
	//자료가 없을 때
	if(!$cnt){
	?>
	<div style="margin-bottom: 1em;">자료가 없습니다.</div>
	<?php 
	}else{
	
		$pagegroupnum=ceil(($pagenum+1)/$pagegroup);
		$startpage=($pagegroupnum-1)*$pagegroup+1;
		$endpage=$startpage+$pagegroup-1;
	
		// 현재 화면에 있는 페이지 넘버들 보다 더 많은 양이 있을 때 처음으로 갈 수 있도록.
		if($pagegroupnum>1){
		?>
			<!-- <a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=<?php echo $_GET["module"];?>&act=<?php echo $_GET["act"];?>&pagenum=0&searchColumn=<?php echo $_GET["searchColumn"];?>&searchStr=<?php echo $_GET["searchStr"];?>&folder_rowid=<?php echo $folder_rowid;?>&orderby=<?php echo $_GET["orderby"];?>&orderopt=<?php echo $_GET["orderopt"];?>">처음활성</a> -->
			<div class="page-li button"><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=<?php echo $_GET["module"];?>&act=<?php echo $_GET["act"];?>&pagenum=<?php echo $startpage-2;?>&searchColumn=<?php echo $_GET["searchColumn"];?>&searchStr=<?php echo $_GET["searchStr"];?>&folder_rowid=<?php echo $folder_rowid;?>&orderby=<?php echo $_GET["orderby"];?>&orderopt=<?php echo $_GET["orderopt"];?>"><i>이전</i></a></div>
		<?php 
		}else{
		?>
			<!-- <div>처음비활성</div> -->
			<div class="page-li button"><a href="#0"><i>이전</i></a></div>
		<?php
		}
	
		// 시작 페이지 넘버부터 마지막 페이지 넘버까지 클릭숫자 보이게.
		for($i=$startpage; $i<=$endpage; $i++){
	
			// 총 페이지 수 보다 커지면 멈춘다.
			if($i>$pagesu){
				break;
			}
	
			$j=$i-1;
			// 해당 숫자클릭이 현재페이지라면 비활성화.
			if($j==$pagenum){
			?>
				<div class="page-li"><a class="current" href="#0"><?php echo $i?></a></div>
			<?php 
			// 해당 숫자클릭이 아니라면 모두 클릭 활성화.
			}else{
			?>
				<div class="page-li"><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=<?php echo $_GET["module"];?>&act=<?php echo $_GET["act"];?>&pagenum=<?php echo $j;?>&searchColumn=<?php echo $_GET["searchColumn"];?>&searchStr=<?php echo $_GET["searchStr"];?>&folder_rowid=<?php echo $folder_rowid;?>&orderby=<?php echo $_GET["orderby"];?>&orderopt=<?php echo $_GET["orderopt"];?>"><?php echo $i;?></a></div>
			<?php 
			}
	
		}
	
		// 끝 페이지가 아니라면 끝 버튼 활성화.
		if($endpage<$pagesu){
		?>
			<div class="page-li button"><a href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=<?php echo $_GET["module"];?>&act=<?php echo $_GET["act"];?>&pagenum=<?php echo $endpage;?>&searchColumn=<?php echo $_GET["searchColumn"];?>&searchStr=<?php echo $_GET["searchStr"];?>&folder_rowid=<?php echo $folder_rowid;?>&orderby=<?php echo $_GET["orderby"];?>&orderopt=<?php echo $_GET["orderopt"];?>"><i>다음</i></a></div>
			<!--  <a class="pagingEndButton"  href="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>?module=<?php echo $_GET["module"];?>&act=<?php echo $_GET["act"];?>&pagenum=<?php echo $pagesu-1;?>&searchColumn=<?php echo $_GET["searchColumn"];?>&searchStr=<?php echo $_GET["searchStr"];?>&folder_rowid=<?php echo $folder_rowid;?>&orderby=<?php echo $_GET["orderby"];?>&orderopt=<?php echo $_GET["orderopt"];?>">끝</a> -->
		<?php 
		// 끝 페이지라면 끝 버튼 비 활성화.
		}else{
		?>
			<div class="page-li button"><a href="#0"><i>다음</i></a></div>
			<!-- <div>끝</div> -->
		</div>
	</nav>		
		<?php
		}
	}	
}
?>