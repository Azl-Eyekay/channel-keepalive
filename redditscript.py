# Installed python3-praw, geany and ffmpeg from debian
# and others from pip
# Made a Reddit account, set up an application and added its client id and secret
# made a white noise video named noise.mkv and downloaded 3 pieces of music as music{0-1}.mp3

import praw
from PIL import Image, ImageDraw, ImageFont
import urllib.request
import sys
import os
from io import BytesIO
import random
import subprocess
from gtts import gTTS

DEBUG_IMAGES_CREATE=False
DEBUG_AUDIOS_CREATE=False
DEBUG_VIDEO_CREATE_TRY2=False
DEBUG_VIDEO_COMPILATION_CREATE=False
DEBUG_VIDEO_MUSIC_ADD=False
DEBUG_VIDEO_COMPILATION_CREATE_2=True

if DEBUG_IMAGES_CREATE==True:
	file_path = 'reddits.txt'
	sys.stdout = open(file_path, "w")

	reddit = praw.Reddit(client_id='', client_secret='', user_agent='')

	acc=0 #FOR SAVED IMAGE NUMBERING
	best_posts_linuxmemes = reddit.subreddit('linuxmemes').hot(limit=60)
	for post in best_posts_linuxmemes:
		if post.selftext == '' and post.stickied==False and (post.url.endswith(".png") or post.url.endswith(".jpg") or post.url.endswith(".jpeg") or post.url.endswith(".gif")):
			urllib.request.urlretrieve(post.url, "tmpimage")
			try:
				img = Image.open("tmpimage")
			except:
				continue
			wid, hgt = img.size
			newimg = Image.new(img.mode, (wid, hgt + (hgt//20)),(0,0,0))
			newimg.paste(img, (0,0))
			d1=ImageDraw.Draw(newimg)
			font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf',hgt//40)
			post.title=post.title.replace('"','')
			post.title=post.title.replace("'",'')
			post.title=post.title.replace('--','')
			print(post.title + ' by '+post.author.name)
			if len(post.title)>20:
				post.title=post.title[0:20]+'...'
			d1.text((10,(hgt + hgt//50)),post.title+' - u/'+post.author.name+' - '+post.subreddit.display_name,fill="white",font=font)
			newimg.save('video'+str(acc)+'.png')
			acc+=1

if DEBUG_AUDIOS_CREATE==True:
	dirlist = os.listdir()
	f=open("reddits.txt","r")
	lines=f.readlines()
	vidcount=0
	for i in dirlist:
		if i.startswith("video"):
			vidcount+=1
	for i in range(vidcount):
			#os.system('espeak -s 120 -w audio'+str(i)+'.waw \''+lines[i]+'\'')
			mytext=lines[i]
			gts=gTTS(text=mytext,lang='en',slow=False)
			gts.save('audio'+str(i)+'.wav')
if DEBUG_VIDEO_CREATE_TRY2==True:
	dirlist = os.listdir()
	vidcount=0
	clips=[]
	for i in dirlist:
		if i.startswith("video"):
			vidcount+=1
	for i in range(vidcount):
		os.system('ffmpeg -stream_loop -1 -i video'+str(i)+'.png -i audio'+str(i)+'.wav -vf "tpad=stop_mode=clone:stop_duration=7,scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:-1:-1:color=black" -shortest out'+str(i)+'.mkv')
		#ffmpeg -i input -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:-1:-1:color=black" output
if DEBUG_VIDEO_COMPILATION_CREATE==True:
	sys.stdout = open("vids.txt", "w")
	dirlist = os.listdir()
	for i in dirlist:
		if i.startswith("out"):
			print('file '+i)
			print('file noise.mkv')
	print('file outro.mkv')
	subprocess.Popen('ffmpeg -f concat -i vids.txt -c copy nomusic.mkv',shell=True)

if DEBUG_VIDEO_COMPILATION_CREATE_2==True:
	dirlist = os.listdir()
	#inputs=''
	acc=0
	#filterstring=''
	for i in dirlist:
		if i.startswith("out"):
	#		inputs=inputs+' -i '+i+' -i noise.mkv'
			acc+=1
	#inputs=inputs+' -i outro.mkv'
	tmp=0
	remaining=0
	print(acc,'acc')
	sets=acc//5
	if acc//5<acc/5:
		remaining=acc%5
	print(sets,'sets')
	print(remaining,'remaining')
	for i in range(sets):
		inputs='-i out'+str(i*5)+'.mkv -i noise.mkv -i out'+str(i*5+1)+'.mkv -i noise.mkv -i out'+str(i*5+2)+'.mkv -i noise.mkv -i out'+str(i*5+3)+'.mkv -i noise.mkv -i out'+str(i*5+4)+'.mkv -i noise.mkv'
		print('ffmpeg '+inputs+' -filter_complex "[0:v] [0:a] [1:v] [1:a] [2:v] [2:a] [3:v] [3:a] [4:v] [4:a] [5:v] [5:a] [6:v] [6:a] [7:v] [7:a] [8:v] [8:a] [9:v] [9:a] concat=n=10:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" nomusic-set'+str(i)+'.mkv')
		os.system('ffmpeg '+inputs+' -filter_complex "[0:v] [0:a] [1:v] [1:a] [2:v] [2:a] [3:v] [3:a] [4:v] [4:a] [5:v] [5:a] [6:v] [6:a] [7:v] [7:a] [8:v] [8:a] [9:v] [9:a] concat=n=10:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" nomusic-set'+str(i)+'.mkv')
	inputs=''
	filterstring=''
	for i in range(remaining-1):
		inputs += '-i out'+str(sets*5+i)+'.mkv -i noise.mkv '
		filterstring+='['+str(i)+':v] ['+str(i)+':a] '
		filterstring+='['+str(remaining-1+i)+':v] ['+str(remaining-1+i)+':a] '
	#os.system('ffmpeg '+inputs+' -filter_complex "'+filterstring+'concat=n='+str(2*(remaining-1))+':v=1:a=1 [v] [a]" -map "[v]" -map "[a]" nomusic-remaining.mkv')
	print('ffmpeg '+inputs+' -filter_complex "'+filterstring+'concat=n='+str(2*(remaining-1))+':v=1:a=1 [v] [a]" -map "[v]" -map "[a]" nomusic-remaining.mkv')
	#for i in range(acc//5):
	#	filterstring+='['+str(i)+':v] ['+str(i)+':a] '
	#print('ffmpeg'+inputs+' -filter_complex "'+filterstring+'concat=n='+str(i)+':v=1:a=1 [v] [a]" -map "[v]" -map "[a]" nomusic.mkv')
	#os.system('ffmpeg'+inputs+' -filter_complex "'+filterstring+'concat=n='+str(i)+':v=1:a=1 [v] [a]" -map "[v]" -map "[a]" nomusic'+str(tmp)+'.mkv')

if DEBUG_VIDEO_MUSIC_ADD==True:
	musicno=random.randint(0,2)
	subprocess.Popen('ffmpeg -i nomusic.mp4 -stream_loop -1 -i music'+str(musicno)+'.mp3 -filter_complex "[1:a]volume=0.15,apad[A];[0:a][A]amerge[out]" -shortest -c:v copy -map 0:v -map [out] -y finale.mkv',shell=True)
