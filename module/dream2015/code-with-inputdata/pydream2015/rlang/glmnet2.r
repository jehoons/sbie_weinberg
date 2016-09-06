#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
library(glmnet)
library(doMC)
library(jsonlite)

lassoregres <- function(input_json, output_json) { 
    input_data = fromJSON(paste(readLines(input_json), collapse="\n"))
    registerDoMC(cores=input_data$config$ncores)

    xdata <- read.table(input_data$data$xdatafile,
                   sep=',',
                   header=TRUE,
                   check.names=FALSE)
    ydata <- read.table(input_data$data$ydatafile,
                   sep=',',
                   header=TRUE,
                   check.names=FALSE)
    
    xdata <- as.matrix(xdata) 

    idx_selected <- abs(ydata) < input_data$config$threshold

    x <- xdata[idx_selected, ]
    y <- ydata[idx_selected]
    ybin <- (y>=0)
    train_ratio = input_data$config$train_ratio
    alpha = input_data$config$alpha
    nfolds = input_data$config$nfolds
    nrepeats = input_data$config$nrepeats 
    normalize = input_data$config$normalize
    outputdata <- list(config=input_data$config,
                       data=list(`coef(min)`=list(),
                                 `coef(1se)`=list(),
                                 score=list(),
                                 `crossvals`=list(),
                                 parity=list()))

    for (i in 1 : nrepeats) { 
        num_samples <- length(y)
        idx_train <- sample( 1:num_samples, train_ratio*num_samples)
        x.train <- x[ idx_train, ]
        x.test <- x[ -idx_train, ]
        
        y.train <- y[ idx_train ]
        y.test <- y[ -idx_train ]

        ybin.train<-ybin[idx_train]
        ybin.test<-ybin[-idx_train]

        cvfit <- cv.glmnet(x.train, 
                           y.train, 
                           alpha=alpha, 
                           parallel=TRUE,
                           nfolds=nfolds, 
                           standardize=normalize)

        yhat_min <- predict(cvfit, newx=x.test, s="lambda.min")
        yhat_1se <- predict(cvfit, newx=x.test, s="lambda.1se")
        yhat_min <- as.vector(yhat_min)
        yhat_1se <- as.vector(yhat_1se)

#        pearsonr_min = cor(yhat_min, y.test)[1] 
#        pearsonr_1se = cor(yhat_1se, y.test)[1] 
#        rmse_min = sqrt(mean(((yhat_min - y.test)^2)))
#        rmse_1se = sqrt(mean(((yhat_1se - y.test)^2)))
        crossvaldata <- list()
#        crossvaldata[['r(min)']] = pearsonr_min 
#        crossvaldata[['r(1se)']] = pearsonr_1se
#        crossvaldata[['rmse(min)']] = rmse_min
#        crossvaldata[['rmse(1se)']] = rmse_1se

        coef_min = coef(cvfit, s="lambda.min")
        coef_min_names = slot(coef_min, "Dimnames")[[1]]
        coef_min_names = coef_min_names[slot(coef_min, "i")+1]
        coef_min_values = slot(coef_min, "x")
        coefdic_min = list() 
        coef_size = length(coef_min_values)

        for (i2 in 1 : coef_size) { 
            coefdic_min[[ coef_min_names[i2] ]] = coef_min_values[i2]
        }

        crossvaldata[['coef(min)']] = coefdic_min

        coef_1se = coef(cvfit, s="lambda.1se")
        coef_1se_names = slot(coef_1se, "Dimnames")[[1]]
        coef_1se_names = coef_1se_names[slot(coef_1se, "i")+1]
        coef_1se_values = slot(coef_1se, "x")
        coefdic_1se = list() 
        coef_size = length(coef_1se_values)

        for (i3 in 1 : coef_size) { 
            coefdic_1se[[ coef_1se_names[i3] ]] = coef_1se_values[i3]
        }

        crossvaldata[['coef(1se)']] = coefdic_1se

        # outputdata$data$`score(cv)`[[sprintf('%d',i)]] <- crossvaldata
        outputdata$data$`crossvals`[[sprintf('%d',i)]] <- crossvaldata

    } # for-loop

    # fit with full data: 
    cvfit <- cv.glmnet(x, y, alpha=alpha, parallel=TRUE, nfolds=nfolds, standardize=normalize) 

    yhat_min <- predict(cvfit, newx=x, s="lambda.min")
    yhat_1se <- predict(cvfit, newx=x, s="lambda.1se")
    yhat_min <- as.vector(yhat_min)
    yhat_1se <- as.vector(yhat_1se)

    #pearsonr_min <- cor(yhat_min, y)[1] 
    #pearsonr_1se <- cor(yhat_1se, y)[1] 
    #rmse_min <- sqrt(mean(((yhat_min - y)^2)))
    #rmse_1se <- sqrt(mean(((yhat_1se - y)^2)))

    #outputdata$data$score$`r(min)` = pearsonr_min
    #outputdata$data$score$`r(1se)` = pearsonr_1se
    #outputdata$data$score$`rmse(min)` = rmse_min
    #outputdata$data$score$`rmse(1se)` = rmse_1se

    outputdata$data$parity = list(obs=as.vector(y), 
                                  pred_min=yhat_min, 
                                  pred_1se=yhat_1se)

    coef_min = coef(cvfit, s="lambda.min")
    coef_min_names = slot(coef_min, "Dimnames")[[1]]
    coef_min_names = coef_min_names[slot(coef_min, "i")+1]
    coef_min_values = slot(coef_min, "x")
    coefdic_min = list()
    coef_size = length(coef_min_values)
    for (i in 1 : coef_size) { 
        coefdic_min[[ coef_min_names[i] ]] = coef_min_values[i]
    }
    outputdata$data$`coef(min)` = coefdic_min

    coef_1se = coef(cvfit, s="lambda.1se")
    coef_1se_names = slot(coef_1se, "Dimnames")[[1]]
    coef_1se_names = coef_1se_names[slot(coef_1se, "i")+1]
    coef_1se_values = slot(coef_1se, "x")
    coefdic_1se = list() 
    coef_size = length(coef_1se_values)
    for (i in 1 : coef_size) { 
        coefdic_1se[[ coef_1se_names[i] ]] = coef_1se_values[i]
    }
    outputdata$data$`coef(1se)` = coefdic_1se

    #Xsel = x[,coef_min_names[2:length(coef_min_names)]]
    #beta = coef_min_values[2:length(coef_min_names)]
    #intercept = coef_min_values[1]

    #yhat_min_manual = Xsel %*% beta + intercept
    #pearsonr_min_manual <- cor(yhat_min_manual, y)[1] 
    #outputdata$data$score$`r(min_manual)` = pearsonr_min_manual

    if(input_data$config$figure==TRUE) { 
        postscript(file=input_data$config$figure_file)

        plot(cvfit)

        plot(as.vector(y), yhat_min, xlab='obs', ylab='y_min')
        abline(lm(as.vector(y)~as.vector(y+1e-50)), col="blue") 

        plot(as.vector(y), yhat_min, xlab='obs', ylab='y_min', xlim=c(-200,200),ylim=c(-200,200))
        abline(lm(as.vector(y)~as.vector(y+1e-50)), col="blue") 

        plot(as.vector(y), yhat_1se, xlab='obs', ylab='y_1se')
        abline(lm(as.vector(y)~as.vector(y+1e-50)), col="blue") 

        plot(as.vector(y), yhat_1se, xlab='obs', ylab='y_1se', xlim=c(-200,200),ylim=c(-200,200))
        abline(lm(as.vector(y)~as.vector(y+1e-50)), col="blue") 

        dev.off()
    }
    return(outputdata)
}

args<-commandArgs(trailingOnly=TRUE)

nargs = length(args) 

if(nargs == 2) {
    input_json <- args[1]
    output_json <- args[2]

} else if(nargs == 0){ 
    input_json <- 'testinput.json'
    output_json <-'testoutput.json'
}

regres <- lassoregres(input_json, output_json) 

write(toJSON(regres, pretty=TRUE, auto_unbox=TRUE), file=output_json, 
      append=FALSE)


