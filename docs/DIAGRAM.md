```mermaid
flowchart LR

    ALB[Application Load Balancer] --request---> UserService[User Service] <---> UsersDB[(Users DB)]
    UserService --response---> ALB
```

