E = read.csv("E.csv", header = T)
E_clean = read.csv("E_clean.csv", header = T)
X = read.csv("X.csv", header = T)
output = kmeans(X, centers=5, iter.max = 100, nstart = 1, algorithm = c("Hartigan-Wong", "Lloyd", "Forgy",
                     "MacQueen"), trace=FALSE)
library(cluster)
output_p = pam(X, 5, metric = "euclidean", stand = F)

X$cluster_kmeans = output$cluster
X$cluster_pam = output_p$clustering
# write.csv(X, file="X_cluster.csv")
