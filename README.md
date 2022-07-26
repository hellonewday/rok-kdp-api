## Rise of Kingdoms KVK Preparation Player Extracting API



### 1. Quickstart 

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
