library(plyr)
library(jsonlite)
# ------------------------------------------------------------------------------------
# Description: AZ-Sanger Challenge scoring functions
# Authors: Michael P Menden, Julio Saez-Rodriguez, Mike Mason, Thomas Yu
# ------------------------------------------------------------------------------------
# Get observation format for Subchallenge 1
getObs_ch1 <- function(ls) {
    return(data.frame(CELL_LINE=as.character(ls$CELL_LINE),
                      COMBINATION_ID=as.character(ls$COMBINATION_ID),
                      OBSERVATION=ls$SYNERGY_SCORE))
}

# Get the drug combinations score of Subchallenge 1
getDrugCombiScore_ch1 <- function(obsfile, predfile, confidence=NA, topX=10) {

    R <- c()

    obs <- read.csv(obsfile,stringsAsFactors = F)
    obs <- getObs_ch1(obs)

    pred <- read.csv(predfile,stringsAsFactors=F)
    pred <- pred[match(paste(obs$CELL_LINE,obs$COMBINATION_ID),paste(pred$CELL_LINE,pred$COMBINATION_ID)),]

    pred$COMBINATION_ID <- gsub(" ", "", pred$COMBINATION_ID)
    for (i in as.character(unique(obs$COMBINATION_ID))) {
        R <- c(R, cor(obs[obs$COMBINATION_ID == i, 'OBSERVATION'], 
                      pred[pred$COMBINATION_ID == i, 'PREDICTION']))
    }
    #Make NA's in R = 0
    R[is.na(R)] = 0
    names(R) <- as.character(unique(obs$COMBINATION_ID))

    if (!file.exists(confidence))
        return(round(c(mean=mean(R),
                       ste=sd(R),
                       n=sum(!is.na(R))),2))

    confidence <- read.csv(confidence,stringsAsFactors=F)
    confidence <- confidence[match(unique(obs$COMBINATION_ID),confidence$COMBINATION_ID),]

    nStep <- 1000
    nVal <- round(topX * (length(R) / 100))
    boot_R <- rep(0, nVal)
    for (i in 1:nStep) {
        idx <- order(confidence$CONFIDENCE, sample(length(R)), decreasing = T)[1:nVal]
        boot_R <- boot_R + R[idx]
    }

    return(round(c(mean=mean(boot_R/nStep),
                   ste=sd(boot_R/nStep),
                   n=sum(!is.na(boot_R/nStep))),2))
}

# ------------------------------------------------------------------------------------
# Get the global score of Subchallenge 1
# ------------------------------------------------------------------------------------
getGlobalScore_ch1 <- function(obsfile, predfile) {
    obs <- read.csv(obsfile, stringsAsFactors=F)
    obs <- getObs_ch1(obs)

    pred <- read.csv(predfile,stringsAsFactors=F)


    pred <- pred[match(paste(obs$CELL_LINE,obs$COMBINATION_ID),paste(pred$CELL_LINE,pred$COMBINATION_ID)),]

    x = obs$OBSERVATION
    y = pred$PREDICTION

    agg <- aggregate(OBSERVATION ~ CELL_LINE, obs, median)
    z0 <- agg$OBSERVATION[match(obs$CELL_LINE, agg$CELL_LINE)]

    agg <- aggregate(OBSERVATION ~ COMBINATION_ID, obs, median)
    z1 <- agg$OBSERVATION[match(obs$COMBINATION_ID, agg$COMBINATION_ID)]

    parCor <- function(u,v,w) {
        numerator = cor(u,v) - cor(u,w) * cor(w,v)
        denumerator = sqrt(1-cor(u,w)^2) * sqrt(1-cor(w,v)^2)
        return(numerator/denumerator)
    }

    numerator=parCor(x,y,z1) - parCor(x,z0,z1) * parCor(z0,y,z1)
    denumerator= sqrt(1-parCor(x,z0,z1)^2) * sqrt(1-parCor(z0,y,z1)^2)
    # ----------------------------------------
    # sub challenge 1 FINAL SCORING metrics
    # ----------------------------------------
    temp   <- data.frame(OBSERVATION = x, PREDICTION = y, COMBINATION_ID = obs$COMBINATION_ID)
    R      <- ddply(temp, "COMBINATION_ID", function(x){if(length(x$OBSERVATION) > 1){return(cor(x$OBSERVATION,x$PREDICTION))}else{return(0)}})
    R[is.na(R[,2]),2] <- 0;
    R$N    <- table(obs$COMBINATION_ID)
    obsMax <- ddply(obs, "COMBINATION_ID", function(x){max(x$OBSERVATION)})

    primaryScoreCH1     <- sum(R$V1*sqrt(R$N-1))/sum(sqrt(R$N-1))                       # primary metric
    gt20Inds             <- obsMax[,2] >= 20
    tieBreakingScoreCH1  <- sum((R$V1*sqrt(R$N-1))[gt20Inds])/sum(sqrt(R$N-1)[gt20Inds]) # tie-breaking metric
    # ----------------------------------------

    # partial out the mean of synergy across cell lines and combinationations
    return(c(score=numerator/denumerator,
             final= primaryScoreCH1,
             tiebreak= tieBreakingScoreCH1))
}

args<-commandArgs(trailingOnly=TRUE)
nargs = length(args)

if (nargs==0){
    obs<-"ch1_obs.csv"
    pred<-"ch1_pred.csv"
    confid<-"ch1_priority.csv"
    outjson <- 'evaluated.json'
} else {
    obs <- args[1]
    pred <- args[2]
    confid <- args[3]
    outjson <- args[4]
}

g_score = getGlobalScore_ch1(obs, pred)
#print (g_score) 
dc_score10 = getDrugCombiScore_ch1(obs, pred, confidence=confid, topX=10)
#print (dc_score10)
dc_score20 = getDrugCombiScore_ch1(obs, pred, confidence=confid, topX=20)
#print (dc_score20)
dc_score30 = getDrugCombiScore_ch1(obs, pred, confidence=confid, topX=30)
#print (dc_score30)

output = list() 
output$global_score <- list(score=g_score['score'], final=g_score['final'],
                            tiebreak=g_score['tiebreak'])

output$drugcombi_score = list() 
output$drugcombi_score$topX_10 <- dc_score10
output$drugcombi_score$topX_20 <- dc_score20
output$drugcombi_score$topX_30 <- dc_score30
output$drugcombi_score$dimnames <- names(dc_score10)

write(toJSON(output, pretty=TRUE, auto_unbox=TRUE, digits=20),
      file=outjson, append=FALSE)



