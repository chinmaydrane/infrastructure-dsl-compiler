# Database Cluster Setup
# Primary database with multiple read replicas

database "primary_db" {
    engine = "mysql"
    version = "8.0"
    storage = "1000GB"
    instance_class = "db.r5.large"
    backup_retention = 30
}

database "read_replica_1" {
    engine = "mysql"
    version = "8.0"
    storage = "1000GB"
    instance_class = "db.r5.large"
    backup_retention = 7
}

database "read_replica_2" {
    engine = "mysql"
    version = "8.0"
    storage = "1000GB"
    instance_class = "db.r5.large"
    backup_retention = 7
}

database "read_replica_3" {
    engine = "mysql"
    version = "8.0"
    storage = "1000GB"
    instance_class = "db.r5.large"
    backup_retention = 7
}

database "redis_primary" {
    engine = "redis"
    version = "6.0"
    storage = "100GB"
    instance_class = "cache.r5.large"
    backup_retention = 14
}

database "redis_replica" {
    engine = "redis"
    version = "6.0"
    storage = "100GB"
    instance_class = "cache.r5.large"
    backup_retention = 7
}

network "vpc_database_cluster" {
    cidr_block = "10.0.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support = true
}
