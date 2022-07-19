# Suckless Auto Installer
- [What is sai?](#what-is-sai)
- [Requirments](#requirments)
- [Installation](#installation)
- [How to use](#how-to-use)

## What is sai?
Sai stands for Suckless Auto Installer.  

Based on the name it's script written on python that automatically download and install any suckless software( also can apply patches! )  
Script can also automatically install software from remote links or from your computer.  

Sai uses file `links.json` which contains links to software and patches to download  

## Requirments
### To run script you have to get installed these programmes
* `python3`
* `git`
* `patch`
* `diff`
* `make`
> Don't forget to install all depedencies of programmes you are going to install


## Installation
```
git clone https://github.com/FlareXF/sai      #clone repo to your local machine
chmod +x sai.py                               #make script executable
```



## How to use
> repository already contains links.json, all you have to do is to edit it
* First of all you have to fill `links.json` file with links to software (or patches) you are going to install :  
Example json below
```json
{
	"dwm" :
   	{
		"programme":"https://dl.suckless.org/dwm/dwm-6.2.tar.gz",
		"patches":
		[
			"https://dwm.suckless.org/patches/fullgaps/dwm-fullgaps-6.2.diff",
			"https://dwm.suckless.org/patches/systray/dwm-systray-6.2.diff",
			"/home/USER/patches/dwm.patch"
		]
	},

	"stterm" : 
	{
		"programme" : "https://dl.suckless.org/st/st-0.8.5.tar.gz",
		"patches":[]
	}
}
```

* Script have many working modes, to get information about them run 
```
python3 sai.py -h
```

* To download and install everything on your system run
```
python3 sai.py -S
```



