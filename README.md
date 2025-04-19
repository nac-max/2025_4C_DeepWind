# 2025_4C_DeepWind
Project for the 18th Chinese Collegiate Computing Competition(4C)  of Chang'an University. This project , which is about the intelligent wind power prediction system, is on the web side.

## About us 
We are from Chang'an University. Our team members are as follows.

- Yifan Li,  College of Information Engineering.
- Puyu Liu,  College of Future of Transportation.
- Zhengkai Xie,  College of Information Engineering.
- Ke Xie,  College of Information Engineering.
- Ration Huang,  College of Information Engineering.

## How to deploy?

On the RedHat/CentOS Linux OS, you need to install docker in advance, and start docker serivce:
```bash
sudo systemctl enable --now docker.service
sudo systemctl is-active docker.service
```

Enter the backend directory, RUN this:

```bash
sudo docker compose build --no-cache
sudo docker compose up -d
```

Enter the frontend directory, RUN this:

```bash
sudo tar -xvf dist.tar
sudo docker compose build --no-cache
sudo docker compose up -d
```

If you deploy successfully, you will see 3 containers that are running:

```bash
docker ps
```

You could contanct me at li.yifan2004@hotmail.com, if you encounter any problems.
