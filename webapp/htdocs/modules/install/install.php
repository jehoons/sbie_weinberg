<?php
/* --------------------------------

module/install/install.php
MySQL Database table 설치 페이지.

-------------------------------- */

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();
?>

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
sbie_id					varchar(700)
,drug_targetss			text
,src_id					tinytext
,src_targets				text
,HBA						int
,cLogP					float
,HBD						int
,Lipinski				int
,SMILES					text
,MW						float
,source					varchar(20)

,PRIMARY KEY(sbie_id)
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

// target 테이블 생성
$sql="
	CREATE TABLE IF NOT EXISTS targets (
ta_rowid					int not null auto_increment
,ta_target					varchar(50)
,PRIMARY KEY(ta_rowid)
	)ENGINE=InnoDB DEFAULT CHARSET=utf8
";
$result = $conn->query($sql);

if($result){
	echo "5. Table inputs created successfully<br />";
}else{
	echo "5. Error creating inputs table: " . mysqli_error($conn)."(".mysqli_errno($conn).")<br />";
}

// target insert
$sql = "INSERT INTO targets VALUES ('','S_AKT')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_AMPK')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_AMP_ATP')"; $result = $conn->query($sql);                                                                                         
$sql = "INSERT INTO targets VALUES ('','S_APC')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_ATM_ATR')"; $result = $conn->query($sql);                                                                                         
$sql = "INSERT INTO targets VALUES ('','S_AcidLactic')"; $result = $conn->query($sql);                                                                                      
$sql = "INSERT INTO targets VALUES ('','S_Apoptosis')"; $result = $conn->query($sql);                                                                                       
$sql = "INSERT INTO targets VALUES ('','S_BAD')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_BAX')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_Bak')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_Bcl_2')"; $result = $conn->query($sql);                                                                                           
$sql = "INSERT INTO targets VALUES ('','S_Bcl_XL')"; $result = $conn->query($sql);                                                                                          
$sql = "INSERT INTO targets VALUES ('','S_CHK1_2')"; $result = $conn->query($sql);                                                                                          
$sql = "INSERT INTO targets VALUES ('','S_COX412')"; $result = $conn->query($sql);                                                                                          
$sql = "INSERT INTO targets VALUES ('','S_Caspase8')"; $result = $conn->query($sql);                                                                                        
$sql = "INSERT INTO targets VALUES ('','S_Caspase9')"; $result = $conn->query($sql);                                                                                        
$sql = "INSERT INTO targets VALUES ('','S_CycA')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_CycB')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_CycD')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_CycE')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_Cytoc_APAF1')"; $result = $conn->query($sql);                                                                                     
$sql = "INSERT INTO targets VALUES ('','S_DNARepair')"; $result = $conn->query($sql);                                                                                       
$sql = "INSERT INTO targets VALUES ('','S_DnaDamage')"; $result = $conn->query($sql);                                                                                       
$sql = "INSERT INTO targets VALUES ('','S_Dsh')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_E2F')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_E2F_CyclinE')"; $result = $conn->query($sql);                                                                                     
$sql = "INSERT INTO targets VALUES ('','S_ERK')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_E_cadh')"; $result = $conn->query($sql);                                                                                          
$sql = "INSERT INTO targets VALUES ('','S_FADD')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_FOXO')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_FosJun')"; $result = $conn->query($sql);                                                                                                                                                                                     
$sql = "INSERT INTO targets VALUES ('','S_GSH')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_GSK_3')"; $result = $conn->query($sql);                                                                                           
$sql = "INSERT INTO targets VALUES ('','S_GSK_3_APC')"; $result = $conn->query($sql);                                                                                       
$sql = "INSERT INTO targets VALUES ('','S_Gli')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_Glut_1')"; $result = $conn->query($sql);                                                                                          
$sql = "INSERT INTO targets VALUES ('','S_HIF1')"; $result = $conn->query($sql);                                                                                                                                                                                    
$sql = "INSERT INTO targets VALUES ('','S_IKK')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_JNK')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_LDHA')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_MXI1')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_Max')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_Mdm2')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_Miz_1')"; $result = $conn->query($sql);                                                                                                                                                                                 
$sql = "INSERT INTO targets VALUES ('','S_Myc')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_Myc_Max')"; $result = $conn->query($sql);                                                                                         
$sql = "INSERT INTO targets VALUES ('','S_NF1')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_NF_kB')"; $result = $conn->query($sql);                                                                                                                                                                                 
$sql = "INSERT INTO targets VALUES ('','S_PDK1')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_PHDs')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_PI3K')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_PIP3')"; $result = $conn->query($sql);;
$sql = "INSERT INTO targets VALUES ('','S_PKC')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_PTEN')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_RAF')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_RAGS')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_RHEB')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_ROS')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_RTK')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_Ras')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_Rb')"; $result = $conn->query($sql);                                                                                              
$sql = "INSERT INTO targets VALUES ('','S_Slug')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_Smad')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_SmadE2F')"; $result = $conn->query($sql);                                                                                         
$sql = "INSERT INTO targets VALUES ('','S_SmadMiz_1')"; $result = $conn->query($sql);                                                                                       
$sql = "INSERT INTO targets VALUES ('','S_Snail')"; $result = $conn->query($sql);                                                                                           
$sql = "INSERT INTO targets VALUES ('','S_TAK1')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_TCF')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_TGFbeta')"; $result = $conn->query($sql);                                                                                                                                                                               
$sql = "INSERT INTO targets VALUES ('','S_TSC1_TSC2')"; $result = $conn->query($sql);                                                                                       
$sql = "INSERT INTO targets VALUES ('','S_UbcH10')"; $result = $conn->query($sql);                                                                                          
$sql = "INSERT INTO targets VALUES ('','S_VEGF')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_VHL')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_WNT')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_beta_cat')"; $result = $conn->query($sql);                                                                                        
$sql = "INSERT INTO targets VALUES ('','S_cdc20')"; $result = $conn->query($sql);                                                                                           
$sql = "INSERT INTO targets VALUES ('','S_cdh1')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_cdh1_UbcH10')"; $result = $conn->query($sql);                                                                                     
$sql = "INSERT INTO targets VALUES ('','S_eEF2')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_eEF2K')"; $result = $conn->query($sql);                                                                                           
$sql = "INSERT INTO targets VALUES ('','S_hTERT')"; $result = $conn->query($sql);                                                                                           
$sql = "INSERT INTO targets VALUES ('','S_mTOR')"; $result = $conn->query($sql);                                                                                            
$sql = "INSERT INTO targets VALUES ('','S_p14')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_p15')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_p21')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_p27')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_p53')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_p53_Mdm2')"; $result = $conn->query($sql);                                                                                        
$sql = "INSERT INTO targets VALUES ('','S_p53_PTEN')"; $result = $conn->query($sql);                                                                                        
$sql = "INSERT INTO targets VALUES ('','S_p70')"; $result = $conn->query($sql);                                                                                             
$sql = "INSERT INTO targets VALUES ('','S_p90')"; $result = $conn->query($sql);
?> 