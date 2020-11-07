import fabric

c = fabric.Connection(
    host='localhost', 
    user='hzg',
    port=22, 
    config=None, 
    gateway=None, 
    inline_ssh_env=True,
    connect_kwargs={"password": "1234"})

result = c.run('./apache-cassandra-3.11.8/bin/nodetool clearsnapshot')