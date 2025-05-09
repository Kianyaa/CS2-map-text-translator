# CS2 map text translator
**Python script that translates [Chinese --> English] map text from [StripperCS2](https://github.com/Source2ZE/StripperCS2) 'JSON' format by using Google Translate API**

![สกรีนช็อต 2025-03-27 022044](https://github.com/user-attachments/assets/8838af97-5fdc-4d14-8b85-b4992c5a0715)

## Features

- Support multiple map lump text data files from StripperCS2 format
- Export Workshop_ID and Workshop Name in json
- Using Google Translate API for translate

> [!IMPORTANT] 
> This script support only translate Chinese to English only! 
>
> If you provide others langauge, Output will be the same!

## Requirements

- [Python](https://www.python.org/downloads/) (version 3.9.11 atleast)
- All dependencies in `requirements.txt`

## Installation

Install [python](https://www.python.org/downloads/) and then download this [repository](https://github.com/Kianyaa/CS2-map-text-translator/archive/refs/heads/main.zip), Extract the zip file in any folder and run `install.bat` file to install
all Python dependencies in this script are required

> [!NOTE]  
> `install.bat` file will automatically create virtual environment and activate it for you

> [!WARNING]
> If you have a problem with installing dependencies while running install batch file
>
> Try to run `pip install pandas requests beautifulsoup4 googletrans` in any bash shell

or you can see all libraries using in `requirements.txt`

## How to use
1. Open PowerShell or CMD on the working directory that has `translate_script.py` file stored
2. Type `python translate_script.py` to run the script (The script will automatically create `data` and `data/export` directories)
3. Put all map lump text data files you want to translate in `data` and follow the script
4. Output file will be create at `data/export` with the same name and same JSON StripperCS2 structure

<hr>



<br>

### Example Input of Lump text file `3347418203_text.json`
```json
{
  "modify": [
    {
      "match": {
        "io": [
          {
            "overrideparam": "say 左乐：此次前赴大荒城，有博士协助，想必路途会轻松不少"
          }
        ]
      },
      "replace": {
        "io": {
          "overrideparam": ""
        }
      }
    },
    {
      "match": {
        "io": [
          {
            "overrideparam": "say 左乐:博士，前方道路开放还有20s"
          }
        ]
      },
      "replace": {
        "io": {
          "overrideparam": ""
        }
      }
    }
  ]
}
```

### Output of `3347418203_text.json` located in `\data\export\3347418203_text.json` after runing the script
```json
{
  "modify": [
    {
      "match": {
        "io": [
          {
            "overrideparam": "say 左乐：此次前赴大荒城，有博士协助，想必路途会轻松不少"
          }
        ]
      },
      "replace": {
        "io": {
          "overrideparam": "Say Zuo Le: This time I went to Dahuang City, with the help of a doctor, I guess the journey will be much easier"
        }
      }
    },
    {
      "match": {
        "io": [
          {
            "overrideparam": "say 左乐:博士，前方道路开放还有20s"
          }
        ]
      },
      "replace": {
        "io": {
          "overrideparam": "Say Zuo Le: Doctor, the road ahead is open for 20 seconds"
        }
      }
    }
  ]
}
```

## Know-Issue

Sometimes script out with `Operation Time Out` or `Exit code 200` or `RunTimeWarning` just re-run the script again or put the file want to translate more less
