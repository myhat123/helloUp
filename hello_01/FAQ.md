常见问题
=======

出现过如下问题，可参考网上资料处理

错误信息  
java.util.concurrent.RejectedExecutionException: Task scala.concurrent.impl.CallbackRunnable
ERROR TransportResponseHandler: Still have 2 requests outstanding when connection from

https://www.jianshu.com/p/7c74b8690322

原因分析  
以上日志出现的比较明显， 就是线程池满了。还有就是仍有外部的请求，但是连接已经关闭。

解决  
修改了 partitionnum 500，核数100，然后修改如下一个参数 
spark.shuffle.io.numConnectionsPerPeer = 5

spark.shuffle.io.numConnectionsPerPeer 默认值是1

机器之间的可以重用的网络连接，主要用于在大型集群中减小网络连接的建立开销，如果一个集群的机器并不多，可以考虑增加这个值

(Netty only) Connections between hosts are reused in order to reduce connection buildup for large clusters. For clusters with many hard disks and few hosts, this may result in insufficient concurrency to saturate all disks, and so users may consider increasing this value.