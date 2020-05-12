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
            "supporter": "k8s",
            "consumer": "servicetree",
            "type": "vital"
        },
        {
            "supporter": "workstation",
            "consumer": "servicetree",
            "type": "none"
        },
        {
            "supporter": "docker",
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
            "supporter": "dbcluster",
            "consumer": "retail",
            "type": "vital"
        },
        {
            "supporter": "batchservice",
            "consumer": "dbcluster",
            "type": "vital"
        },
        {
            "supporter": "dbcluster",
            "consumer": "batchservice",
            "type": "vital"
        },
        {
            "supporter": "fileservice",
            "consumer": "retail",
            "type": "vital"
        },
        {
            "supporter": "batchservice",
            "consumer": "retail",
            "type": "important"
        }
    ]
}