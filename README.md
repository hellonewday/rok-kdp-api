## Rise of Kingdoms KVK Preparation Player Extracting API

This project is made by LK Maximusss, Y719 Officer, Kingdom 2719. 

Players will send their images including profile, info, pre-kvk result to identify initial data before starting KVK.

### 1. Live demo

Web Version: Working in progress

API Version, uploaded on Google Cloud Run: https://rok-kdp-api-m3gpgoqcgq-as.a.run.app

### 2. Quickstart 

```bash
git clone https://github.com/hellonewday/rok-kdp-api
cd rok-kdp-api
pip install -r requirements.txt
flask run
```

Capturing these screen on your device: 

1. Profile screen image

![profile_image](profile.jpg)

2. Info screen with kill point pop-up image

![info_image](info.jpg)

3. Pre-kvk screen image

![pre_image](pre.jpg)


Send POST request to /uploads endpoint

Example Request: 

```bash
Content-Type: multipart/form-data
Body: 
    "profile": File,
    "info": File,
    "pre": File

```

Example Response: 

```javascript
{
    "Id": "121607730)",
    "Kill points": [
        "832,946",
        "1,580,832",
        "1,360,587",
        "'4,745,472",
        "138,094"
    ],
    "Name": "LK Maximusss",
    "Power": "20,539,430",
    "Pre-kvk points": "35,000"
}
```

### 3. Deployment

```bash

docker build -t rok-kdp-api:1.0 .
docker run -p 5000:5000 -d rok-kdp-api:1.0

```

Test if your API is working on http://localhost:5000


### 4. Future Plan & Contact

This is just the beginning, I am planning to make more features, including daily kill point tracking for top 100/300/500/..., leaderboard daily tracking (top power changes, resouces farming changes, flags per day,...). Any questions, p.m me:

- LK Maximusss, 2719

- Lx Cafe, 1296

- BA 5, 1930

