# Step 1. Preprocessing  

$cd pydream2015/preproc 
$py.test -qs __init__.py 

# Step 2. Feature generation

$cd pydream2015/feature 
$py.test -qs test_smoother.py 
$py.test -qs test_smoother_arc2016_16_cnv_methyl.py
$py.test -qs test_calc_dd3d.py 
$py.test -qs test_match.py

# Step 3. Challenge 1A Model

# Feature selection 
$cd pydream2015/model/ch1a_mxdrg
$py.test -qs makeinput.py
$make

# Model training
$cd pydream2015/model/ch1a_mxdrg_post
$make
$python summary.py

# Step 4. Challenge 1B Model

# Feature selection and model training 
$cd pydream2015/model/ch1b_mxdrg
$make 
$python summary_tr.py

# Step 5. Post dream challenge - Identification of Biomarkers 

$cd pydream2015/postproc
$cp pydream2015/model/ch1a_mxdrg_post/scoreXXXX_data.tar.gz best  (or) 
$cp pydream2015/model/ch1b_mxdrg/scoreXXXX_data.tar.gz best 

cd best 
$tar xf scoreXXXX_data.tar.gz
cd ..
$py.test -qs test_biomarker.py

# Step 6. Calculate combination priority
$cd extra/test_data
$cp pydream2015/model/ch1a_mxdrg_post/scoreXXXX_data.tar.gz . 
$tar xf scoreXXXX_data.tar.gz
$cd .. 
$py.test -qs calc_priority.py

