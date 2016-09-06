# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of {pydream2015}.
#*************************************************************************
__all__ = ['util', 'feature', 'preproc', 'initdatapath', 'rlang', 'diary', 
    'model']

import os 
from os.path import join,exists


def initdatapath(input_dir, output_dir, user_data=None):

    global DATA_COMBITHERAPY
    global DATA_COMBITHERAPY_TEST
    global DATA_COMBITHERAPY_LEADER
    global DATA_COMBITHERAPY_USER
    global DATA_GENEEXPR
    global DATA_MUTATION
    global DATA_CELLINFO
    global DATA_ENSEMBLID
    global DATA_PPI_NCI 
    global DATA_PPI_STRING
    global DATA_DRUG_DESC_2D 
    global DATA_DRUG_DESC_3D
    global DATA_DRUG_INFO

    DATA_COMBITHERAPY = join(input_dir,
            'dream2015/synergy/ch1_train_combination_and_monoTherapy_updated.csv')
    assert exists(DATA_COMBITHERAPY)

    DATA_COMBITHERAPY_TEST = join(input_dir,
            'dream2015/synergy/ch1_test_monoTherapy.csv')
    assert exists(DATA_COMBITHERAPY_TEST)

    DATA_COMBITHERAPY_LEADER = join(input_dir,
            'dream2015/synergy/ch1_leaderBoard_monoTherapy.csv')
    assert exists(DATA_COMBITHERAPY_LEADER)

    DATA_COMBITHERAPY_USER = user_data 

    DATA_GENEEXPR = join(input_dir, 'dream2015/molecular/gex.csv')
    assert exists(DATA_GENEEXPR)

    DATA_MUTATION = join(input_dir, 'dream2015/molecular/mutations.csv') 
    assert exists(DATA_MUTATION)

    DATA_CELLINFO = join(input_dir, 'dream2015/molecular/cell_info.csv')
    assert exists(DATA_CELLINFO)

    DATA_ENSEMBLID = join(input_dir, 'db/biomart/ensemblid.csv') 
    assert exists(DATA_ENSEMBLID)

    DATA_PPI_NCI = join(input_dir, 'db/NCI/nci_pid_modification_link.txt') 
    assert exists(DATA_PPI_NCI)

    DATA_PPI_STRING = join(input_dir, 'db/STRING/protein.links.9606.v10.txt') 
    assert exists(DATA_PPI_STRING)

    DATA_DRUG_DESC_2D = join(input_dir, 'team/jhsong/desc_2d_final_updated.csv') 
    assert exists(DATA_DRUG_DESC_2D) 

    DATA_DRUG_DESC_3D = join(input_dir, 'team/jhsong/desc_3d_final.csv') 
    assert exists(DATA_DRUG_DESC_3D) 

    DATA_DRUG_INFO = join(input_dir,
            'dream2015/synergy/Drug_info_release_jhs.csv') 
    assert exists(DATA_DRUG_INFO)

    # result files : 
    global MYDATA_GENEEXPR_FILLED 
    global MYDATA_DICT
    global MYDATA_PPI_STRING_PROCESSED
    global MYDATA_PPI_STRING_TRANSLATED 
    global MYDATA_PPI_STRING_HIST
    global MYDATA_DRUG_DESC_3D_CONV 

    global MYDATA_MUTSMOOTH_MAT_NCI 
    global MYDATA_MUTSMOOTH_VEC_NCI 
    global MYDATA_SMOOTHED_MUTATION_NCI
    global MYDATA_MUTSMOOTH_MAT_STRING 
    global MYDATA_MUTSMOOTH_VEC_STRING
    global MYDATA_SMOOTHED_CNV_STRING
    global MYDATA_SMOOTHED_METHYL_STRING
    global MYDATA_SMOOTHED_MUTATION_STRING

    MYDATA_GENEEXPR_FILLED = join(output_dir, 'gex_filled.csv')
    MYDATA_DICT = join(output_dir, 'biomart_dict.pkl') 
    MYDATA_PPI_STRING_PROCESSED = join(output_dir, 'stringppi_processed.csv') 
    MYDATA_PPI_STRING_TRANSLATED = join(output_dir, 'stringppi_translated.csv') 
    MYDATA_PPI_STRING_HIST = join(output_dir, 'stringppi_hist.csv') 
    MYDATA_DRUG_DESC_3D_CONV = join(output_dir, 'desc_3d_conv.csv') 
    
    # smoothing mutation profile with nci network 
    MYDATA_MUTSMOOTH_MAT_NCI = join(output_dir, 'mutsmooth_mat_NCI.csv') 
    MYDATA_MUTSMOOTH_VEC_NCI = join(output_dir, 'mutsmooth_vec_NCI.csv') 
    MYDATA_SMOOTHED_MUTATION_NCI = join(output_dir, 'smoothed_mut_NCI.csv') 

    # smoothing mutation profile with string network 
    MYDATA_MUTSMOOTH_MAT_STRING = join(output_dir, 'mutsmooth_mat_STRING.csv') 
    MYDATA_MUTSMOOTH_VEC_STRING = join(output_dir, 'mutsmooth_vec_STRING.csv') 
    MYDATA_SMOOTHED_MUTATION_STRING = join(output_dir, 'smoothed_mut_STRING.csv') 
    MYDATA_SMOOTHED_CNV_STRING = join(output_dir, 'smoothed_CNV_STRING.csv')
    MYDATA_SMOOTHED_METHYL_STRING = join(output_dir, 'smoothed_methyl_STRING.csv')

    global MYDATA_DRUG_INFO_EXT
    global MYDATA_DRUG_TARGET_ABLE 
    global MYDATA_DRUG_TARGET_UNABLE 
    global MYDATA_SMOOTHED_DRUGEFFECT_NCI 
    global MYDATA_SMOOTHED_DRUGEFFECT_STRING 

    # smoothing drug targets 
    MYDATA_DRUG_INFO_EXT = join(output_dir, 'druginfo_extended.csv')
    MYDATA_DRUG_TARGET_ABLE = join(output_dir, 'drugtarget_able.csv')
    MYDATA_DRUG_TARGET_UNABLE = join(output_dir, 'drugtarget_unable.csv')
    MYDATA_SMOOTHED_DRUGEFFECT_NCI = join(output_dir, 'smoothed_drugeffect_NCI.csv')
    MYDATA_SMOOTHED_DRUGEFFECT_STRING = join(output_dir, 'smoothed_drugeffect_STRING.csv')

    # matched
    global MYDATA_MATCHED_GEX
    global MYDATA_MATCHED_MUT
    global MYDATA_MATCHED_SMOOTHED_CNV 
    global MYDATA_MATCHED_SMOOTHED_METHYL
    global MYDATA_MATCHED_SMOOTHED_MUT
    global MYDATA_MATCHED_DD3DC
    global MYDATA_MATCHED_DRUGEFFECT
    global MYDATA_MATCHED_DRCC

    MYDATA_MATCHED_GEX = join(output_dir, 'matched_gex.pkl')
    MYDATA_MATCHED_MUT = join(output_dir, 'matched_mut.pkl')
    MYDATA_MATCHED_SMOOTHED_CNV = join(output_dir, 'matched_smoothed_CNV.pkl')
    MYDATA_MATCHED_SMOOTHED_METHYL = join(output_dir, 'matched_smoothed_methyl.pkl')
    MYDATA_MATCHED_SMOOTHED_MUT = join(output_dir, 'matched_smoothed_mut.pkl')
    MYDATA_MATCHED_DD3DC = join(output_dir, 'matched_dd3dc.pkl')
    MYDATA_MATCHED_DRUGEFFECT = join(output_dir, 'matched_drugeffect.pkl')
    MYDATA_MATCHED_DRCC = join(output_dir, 'matched_drcc.pkl')

    # matched - test 
    global MYDATA_MATCHEDTEST_GEX
    global MYDATA_MATCHEDTEST_MUT
    global MYDATA_MATCHEDTEST_SMOOTHED_CNV 
    global MYDATA_MATCHEDTEST_SMOOTHED_METHYL
    global MYDATA_MATCHEDTEST_SMOOTHED_MUT
    global MYDATA_MATCHEDTEST_DD3DC
    global MYDATA_MATCHEDTEST_DRUGEFFECT
    global MYDATA_MATCHEDTEST_DRCC

    MYDATA_MATCHEDTEST_GEX = join(output_dir, 'matchedtest_gex.pkl')
    MYDATA_MATCHEDTEST_MUT = join(output_dir, 'matchedtest_mut.pkl')
    MYDATA_MATCHEDTEST_SMOOTHED_CNV = join(output_dir, 'matchedtest_smoothed_CNV.pkl')
    MYDATA_MATCHEDTEST_SMOOTHED_METHYL = join(output_dir, 'matchedtest_smoothed_methyl.pkl')
    MYDATA_MATCHEDTEST_SMOOTHED_MUT = join(output_dir, 'matchedtest_smoothed_mut.pkl')
    MYDATA_MATCHEDTEST_DD3DC = join(output_dir, 'matchedtest_dd3dc.pkl')
    MYDATA_MATCHEDTEST_DRUGEFFECT = join(output_dir, 'matchedtest_drugeffect.pkl')
    MYDATA_MATCHEDTEST_DRCC = join(output_dir, 'matchedtest_drcc.pkl')

    # matched - leader
    global MYDATA_MATCHEDLEADER_GEX
    global MYDATA_MATCHEDLEADER_MUT
    global MYDATA_MATCHEDLEADER_SMOOTHED_CNV 
    global MYDATA_MATCHEDLEADER_SMOOTHED_METHYL
    global MYDATA_MATCHEDLEADER_SMOOTHED_MUT
    global MYDATA_MATCHEDLEADER_DD3DC
    global MYDATA_MATCHEDLEADER_DRUGEFFECT
    global MYDATA_MATCHEDLEADER_DRCC

    MYDATA_MATCHEDLEADER_GEX = join(output_dir, 
            'matchedleader_gex.pkl')
    MYDATA_MATCHEDLEADER_MUT = join(output_dir, 
            'matchedleader_mut.pkl')
    MYDATA_MATCHEDLEADER_SMOOTHED_CNV = join(output_dir, 
            'matchedleader_smoothed_CNV.pkl')
    MYDATA_MATCHEDLEADER_SMOOTHED_METHYL = join(output_dir, 
            'matchedleader_smoothed_methyl.pkl')
    MYDATA_MATCHEDLEADER_SMOOTHED_MUT = join(output_dir, 
            'matchedleader_smoothed_mut.pkl')
    MYDATA_MATCHEDLEADER_DD3DC = join(output_dir, 
            'matchedleader_dd3dc.pkl')
    MYDATA_MATCHEDLEADER_DRUGEFFECT = join(output_dir, 
            'matchedleader_drugeffect.pkl')
    MYDATA_MATCHEDLEADER_DRCC = join(output_dir, 
            'matchedleader_drcc.pkl')

    # matched - user
    global MYDATA_MATCHEDUSER_GEX
    global MYDATA_MATCHEDUSER_MUT
    global MYDATA_MATCHEDUSER_SMOOTHED_CNV 
    global MYDATA_MATCHEDUSER_SMOOTHED_METHYL
    global MYDATA_MATCHEDUSER_SMOOTHED_MUT
    global MYDATA_MATCHEDUSER_DD3DC
    global MYDATA_MATCHEDUSER_DRUGEFFECT
    global MYDATA_MATCHEDUSER_DRCC

    MYDATA_MATCHEDUSER_GEX = join(output_dir, 
            'matcheduser_gex.pkl')
    MYDATA_MATCHEDUSER_MUT = join(output_dir, 
            'matcheduser_mut.pkl')
    MYDATA_MATCHEDUSER_SMOOTHED_CNV = join(output_dir, 
            'matcheduser_smoothed_CNV.pkl')
    MYDATA_MATCHEDUSER_SMOOTHED_METHYL = join(output_dir, 
            'matcheduser_smoothed_methyl.pkl')
    MYDATA_MATCHEDUSER_SMOOTHED_MUT = join(output_dir, 
            'matcheduser_smoothed_mut.pkl')
    MYDATA_MATCHEDUSER_DD3DC = join(output_dir, 
            'matcheduser_dd3dc.pkl')
    MYDATA_MATCHEDUSER_DRUGEFFECT = join(output_dir, 
            'matcheduser_drugeffect.pkl')
    MYDATA_MATCHEDUSER_DRCC = join(output_dir, 
            'matcheduser_drcc.pkl')

    # rawdatafiles
    global DIR_TRAINING_COMBI_THERAPY
    global DIR_TRAINING_MONO_THERAPY

    DIR_TRAINING_COMBI_THERAPY = join(input_dir, 'dream2015/synergy/Raw_Data_csv/ch1_training_combinations') 
    DIR_TRAINING_MONO_THERAPY = join(input_dir, 'dream2015/synergy/Raw_Data_csv/ch1_ch2_monoTherapy')


from os.path import dirname, exists, join, abspath
thisdir = abspath(dirname( __file__ ))

if not exists(join(thisdir, 'test_input')) or not exists(join(thisdir, 'test_output')):   
    prevdir = os.getcwd() 
    os.chdir(thisdir)
    os.system('scp sbieshare@ras.kaist.ac.kr:dataset/dream2015/dataset.tar %s' % '.')
    os.system('tar xvf dataset.tar')
    os.system('rm -f dataset.tar')
    os.chdir(prevdir)

