<div id="cl-content">
	<div id="cl-content-title">Install</div>
<?php
// member 테이블 생성
$sql=" 
	CREATE TABLE IF NOT EXISTS member (
mb_rowid					int not null auto_increment
,mb_email					varchar(255) not null default ''
,mb_pwd						varchar(255)
,mb_name					varchar(255)
,mb_organization			varchar(255)
,mb_visitnum				int
,mb_writedatetime			datetime
,mb_recentdatetime			datetime
,mb_updatedatetime			datetime
,mb_pwdupdatedatetime		datetime
,mb_outdatetime				datetime
,mb_outreason				text
,mb_code					int

,mb_varchar1				varchar(255)
,mb_varchar2				varchar(255)
,mb_int1					int
,mb_int2					int
,mb_text					text
,mb_datetime				datetime
,PRIMARY KEY(mb_rowid)
,UNIQUE KEY(mb_email)
	)ENGINE=InnoDB DEFAULT CHARSET=utf8 
";
$result = $conn->query($sql);

if($result){
	echo "1. Table member created successfully<br />";
}else{
	echo "1. Error creating member table: " . mysqli_error($conn)."(".mysqli_errno($conn).")<br />";
}

// cellline 테이블 생성
$sql="
	CREATE TABLE IF NOT EXISTS cellline (
cl_rowid					int not null auto_increment
,cl_cellname_name			varchar(50)
,cl_cclename_name			varchar(255)
,cl_alternative_name		varchar(50)
,cl_disease_area			varchar(50)
,cl_tissue					varchar(50)

,cl_varchar1				varchar(255)
,cl_varchar2				varchar(255)
,cl_int1					int
,cl_int2					int
,cl_text					text
,cl_datetime				datetime
,PRIMARY KEY(cl_rowid)
	)ENGINE=InnoDB DEFAULT CHARSET=utf8
";
$result = $conn->query($sql);

if($result){
	echo "2. Table cellline created successfully<br />";
}else{
	echo "2. Error creating cellline table: " . mysqli_error($conn)."(".mysqli_errno($conn).")<br />";
}

// drugs 테이블 생성
$sql="
	CREATE TABLE IF NOT EXISTS drugs (
dr_rowid					int not null auto_increment
,dr_sbie_id					varchar(700)
,dr_drug_targetss			text
,dr_src_id					tinytext
,dr_src_targets				text
,dr_HBA						int
,dr_cLogP					float
,dr_HBD						int
,dr_Lipinski				int
,dr_SMILES					text
,dr_MW						float
,dr_source					varchar(20)

,dr_varchar1				varchar(255)
,dr_varchar2				varchar(255)
,dr_int1					int
,dr_int2					int
,dr_text					text
,dr_datetime				datetime
,PRIMARY KEY(dr_rowid)
	)ENGINE=InnoDB DEFAULT CHARSET=utf8
";
$result = $conn->query($sql);

if($result){
	echo "3. Table drugs created successfully<br />";
}else{
	echo "3. Error creating drugs table: " . mysqli_error($conn)."(".mysqli_errno($conn).")<br />";
}

// inputs 테이블 생성
$sql="
	CREATE TABLE IF NOT EXISTS inputs (
dr_rowid					int not null auto_increment
,dr_cancer_type				varchar(700)
,dr_gene_expression			mediumblob
,dr_cnv						mediumblob
,dr_mutation				mediumblob
,dr_simulation_mode			char(20)
,dr_drugs					varchar(8000)
,dr_optimal_therapy			char(30)
,dr_email					varchar(100)
,dr_combination_drug		char(20)
,dr_cell_lines				varchar(8000)

,dr_varchar1				varchar(255)
,dr_varchar2				varchar(255)
,dr_int1					int
,dr_int2					int
,dr_text					text
,dr_datetime				datetime
,PRIMARY KEY(dr_rowid)
	)ENGINE=InnoDB DEFAULT CHARSET=utf8
";
$result = $conn->query($sql);

if($result){
	echo "4. Table inputs created successfully<br />";
}else{
	echo "4. Error creating inputs table: " . mysqli_error($conn)."(".mysqli_errno($conn).")<br />";
}
?>
</div>