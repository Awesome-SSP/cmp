// Connect to sender (primary node)
shell.connect('root@192.168.1.28:3306')

// Configure instance
dba.configureInstance('root@192.168.1.28:3306', {
  recoveryAccount: 'repl',
  recoveryPassword: 'ReplPass123'
})

// Create the cluster
var cluster = dba.createCluster('mycluster')

// Add the receiver node
cluster.addInstance('root@192.168.1.22:3306', {
  recoveryAccount: 'repl',
  recoveryPassword: 'ReplPass123'
})

// Show status
print(JSON.stringify(cluster.status(), null, 2))
