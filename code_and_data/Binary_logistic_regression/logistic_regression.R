install.packages("glmnet")
install.packages("rsample")
install.packages("caret")
install.packages("pROC")
install.packages("ROSE")
# 安装并加载字体包
install.packages("extrafont")

library(extrafont)
library(ROSE)
library(rsample)
library(glmnet)
library(caret)
library(pROC)


font_import()
loadfonts(device = "win") 

#-----------------------logistic回归--强弱----------------------------

data <- read.csv("E:/insectOR/PAPER/result6/3-ee_combination/ee_comb_BBI_high_low.csv")


data$BBI <- ifelse(data$BBI == "high", 1, 0)


y <- data$BBI

# one-hot
X <- model.matrix(BBI ~ . - 1, data = data) 

X_df <- as.data.frame(X)

data_encoded_BBI <- cbind(X_df, BBI = data$BBI)

#set.seed(321)
set.seed(321)
data_balanced <- ovun.sample(BBI ~ ., data = data_encoded_BBI, method = "over", N = 24)$data


table(data_balanced$BBI)
table(data_encoded_BBI$BBI)


#set.seed(1234)
set.seed(1234)
trainIndex <- createDataPartition(data_balanced$BBI, p = 0.8, list = FALSE)
trainData <- data_balanced[trainIndex, ]
testData <- data_balanced[-trainIndex, ]


x_train <- model.matrix(BBI ~ ., trainData)[,-1]
y_train <- trainData$BBI
x_test <- model.matrix(BBI ~ ., testData)[,-1]
y_test <- testData$BBI


cvfit <- cv.glmnet(x_train, y_train, family = "binomial", alpha = 0.5,nfolds = 10)  # alpha = 1表示Lasso回归，alpha = 0.5随便选的



best_lambda <- cvfit$lambda.min
best_lambda


par(family = "serif",lwd = 3)  # Windows 通常将 Times New Roman 映射到 serif


plot(cvfit,xlim = c(-8,-1), ylim = c(0,4))
plot(cvfit$glmnet.fit,xvar = "lambda",label = T,lwd = 3)


coef(cvfit, s = "lambda.min") 


pred <- predict(cvfit, s = best_lambda, newx = x_test, type = "response")

#pred <- predict(cvfit, s = best_lambda, newx = x_train, type = "response")


roc_obj <- roc(y_test, as.numeric(pred))

#roc_obj <- roc(y_train, as.numeric(pred))

auc_value <- auc(roc_obj)


y_test
y_train
as.numeric(pred)
cat("Best lambda:", best_lambda, "\n")
cat("AUC:", auc_value, "\n")


x <- model.matrix(BBI ~ . - 1, data = data_balanced)
y <- data_balanced$BBI

grid <- 10^seq(0, -5, length=100)
out <- cv.glmnet(x, y, family = "binomial", alpha = 0.8,lambda=grid)  # alpha = 1表示赋予L1正则项，而不是单纯的Lasso回归
out$lambda.min


plot(out,xlim = c(-4.1,-1.5), ylim = c(0.5,2.3))
plot(out$glmnet.fit,xvar = "lambda",label = T)

logistic.coef <- predict(out, type="response",newx = x, s=best_lambda)[1:24,]


roc_obj_all <- roc(y, as.numeric(logistic.coef))
auc_value_all <- auc(roc_obj_all)

cat("Best lambda:", best_lambda, "\n")
cat("AUC:", auc_value_all, "\n")


plot(roc_obj_all, col = "blue", main = paste("ROC Curve (AUC =", round(auc_value_all, 2), ")"))

coef(out, s = best_lambda) 
