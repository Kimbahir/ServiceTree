empty = {
    "name": "MyTree",
    "label": "My overview tree",
    "customerId": "1234567",
    "services": [],
    "relations": []
}

example1 = {
    "name": "bahirinfrastructure",
    "label": "Bahir Infrastructure",
    "customerId": "",
    "services": [
        {
            "name": "k8s",
            "label": "Kubernetes Cluster",
            "type": "farm",
            "servers": [
                {
                    "id": "master",
                    "name": "master"
                },
                {
                    "id": "worker01",
                    "name": "Worker A"
                },
                {
                    "id": "worker02",
                    "name": "Worker B"
                }
            ]
        },
        {
            "name": "workstation",
            "label": "Workstations",
            "type": "none",
            "servers": [
                {
                    "id": "morticia",
                    "name": "Morticia"
                },
                {
                    "id": "shirinak",
                    "name": "Shirinak (motion)"
                }
            ]
        },
        {
            "name": "docker",
            "label": "DockerHub",
            "type": "farm",
            "servers": []
        },
        {
            "name": "servicetree",
            "label": "Service Tree Microservice",
            "type": "none",
            "servers": [
                {
                    "id": "container",
                    "name": "kimbahir/servicetree:latest"
                }
            ]
        }
    ],
    "relations": [
        {
            "provider": "k8s",
            "consumer": "servicetree",
            "type": "vital"
        },
        {
            "provider": "workstation",
            "consumer": "servicetree",
            "type": "none"
        },
        {
            "provider": "docker",
            "consumer": "k8s",
            "type": "vital"
        }
    ]
}

example2 = {
    "name": "MyTree",
    "label": "My overview tree",
    "customerId": "1234567",
    "services": [
        {
            "name": "retail",
            "label": "Retail Application",
            "type": "farm",
            "servers": [
                {
                    "id": "1234",
                    "name": "app01"
                },
                {
                    "id": "2345",
                    "name": "app02"
                },
                {
                    "id": "foo",
                    "name": "app03"
                }
            ]
        },
        {
            "name": "fileservice",
            "label": "File cluster",
            "type": "apcluster",
            "servers": [
                {
                    "id": "a",
                    "name": "file01"
                },
                {
                    "id": "a",
                    "name": "file02"
                }
            ]
        },
        {
            "name": "batchservice",
            "label": "Batch server",
            "type": "n/a",
            "servers": [
                {
                    "id": "batch",
                    "name": "batch01"
                }
            ]
        },
        {
            "name": "dbcluster",
            "label": "SQL Server Cluster",
            "type": "aacluster",
            "servers": [
                {
                    "id": "3456",
                    "name": "db01"
                },
                {
                    "id": "4567",
                    "name": "db02"
                }
            ]
        }
    ],
    "relations": [
        {
            "provider": "dbcluster",
            "consumer": "retail",
            "type": "vital"
        },
        {
            "provider": "batchservice",
            "consumer": "dbcluster",
            "type": "vital"
        },
        {
            "provider": "dbcluster",
            "consumer": "batchservice",
            "type": "vital"
        },
        {
            "provider": "fileservice",
            "consumer": "retail",
            "type": "vital"
        },
        {
            "provider": "batchservice",
            "consumer": "retail",
            "type": "important"
        }
    ]
}

example3 = {"customerId": "1234567", "label": "My overview tree", "name": "MyTree", "relations": [{"consumer": "Web", "provider": "File Content Cache", "type": "vital"}, {"consumer": "Web", "provider": "Web database", "type": "vital"}, {"consumer": "File Content Cache", "provider": "CMS", "type": "important"}, {"consumer": "Web database", "provider": "CMS", "type": "important"}, {"consumer": "Navision DB", "provider": "Database Hotel", "type": "vital"}, {"consumer": "Voice DB", "provider": "Database Hotel", "type": "vital"}, {"consumer": "Citrix DB", "provider": "Database Hotel", "type": "vital"}, {"consumer": "Dynamics Batch", "provider": "Navision DB", "type": "vital"}, {"consumer": "AOS", "provider": "Navision DB", "type": "vital"}, {"consumer": "Dynamics", "provider": "AOS", "type": "vital"}, {"consumer": "Dynamics", "provider": "Dynamics Batch", "type": "important"}, {"consumer": "Voice server", "provider": "Voice DB", "type": "vital"}, {"consumer": "Softphone", "provider": "Voice server", "type": "vital"}, {"consumer": "Citrix", "provider": "Citrix DB", "type": "vital"}, {"consumer": "Citrix", "provider": "File cluster", "type": "vital"}, {"consumer": "Dynamics", "provider": "Citrix", "type": "vital"}, {"consumer": "Retail-App", "provider": "Citrix", "type": "vital"}, {"consumer": "Office", "provider": "Citrix", "type": "vital"}, {"consumer": "Office", "provider": "File cluster", "type": "important"}, {"consumer": "Softphone", "provider": "Citrix", "type": "important"}], "services": [{"label": "Web", "name": "Web", "servers": [{"id": "web01", "name": "webserver01"}, {"id": "web02", "name": "webserver02"}, {"id": "web03", "name": "webserver03"}, {"id": "web04", "name": "webserver04"}], "type": "farm"}, {"label": "File Content Cache", "name": "File Content Cache", "servers": [{"id": "cache01", "name": "redis-cache01"}, {"id": "cache02", "name": "redis-cache02"}], "type": "farm"}, {
    "label": "Web database", "name": "Web database", "servers": [{"id": "wdb1", "name": "web-db-a"}, {"id": "wdb2", "name": "web-db-b"}], "type": "apcluster"}, {"label": "CMS", "name": "CMS", "servers": [{"id": "cms1", "name": "cms01"}], "type": "none"}, {"label": "Database Hotel", "name": "Database Hotel", "servers": [{"id": "db01", "name": "database-hotel-a"}, {"id": "db02", "name": "database-hotel-b"}], "type": "aacluster"}, {"label": "Navision DB", "name": "Navision DB", "servers": [], "type": "none"}, {"label": "Voice DB", "name": "Voice DB", "servers": [], "type": "none"}, {"label": "Citrix DB", "name": "Citrix DB", "servers": [], "type": "none"}, {"label": "Dynamics Batch", "name": "Dynamics Batch", "servers": [{"id": "aosbatch01", "name": "aos-batch-01"}], "type": "none"}, {"label": "AOS", "name": "AOS", "servers": [{"id": "aos01", "name": "aos01"}, {"id": "aos02", "name": "aos02"}, {"id": "aos03", "name": "aos03"}, {"id": "aos04", "name": "aos04"}, {"id": "aos05", "name": "aos05"}, {"id": "aos06", "name": "aos06"}], "type": "farm"}, {"label": "Dynamics", "name": "Dynamics", "servers": [], "type": "none"}, {"label": "Citrix", "name": "Citrix", "servers": [{"id": "ctx01", "name": "ctx-01"}, {"id": "ctx02", "name": "ctx-02"}, {"id": "ctx03", "name": "ctx-03"}, {"id": "ctx04", "name": "ctx-04"}, {"id": "ctx05", "name": "ctx-05"}], "type": "farm"}, {"label": "Retail-App", "name": "Retail-App", "servers": [], "type": "none"}, {"label": "Office", "name": "Office", "servers": [], "type": "none"}, {"label": "Softphone", "name": "Softphone", "servers": [], "type": "none"}, {"label": "File cluster", "name": "File cluster", "servers": [{"id": "file01", "name": "file01"}, {"id": "file02", "name": "file02"}], "type": "apcluster"}, {"label": "Voice server", "name": "Voice server", "servers": [{"id": "voip01", "name": "voip01"}], "type": "none"}]}
