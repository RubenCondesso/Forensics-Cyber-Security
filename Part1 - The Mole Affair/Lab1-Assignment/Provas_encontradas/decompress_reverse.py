# -*- coding: utf-8 -*-
import sys
import struct
import numpy


from PIL import Image

def gather(v): #Juntar um array de bits num ficheiro binário

	length=len(v)
	bytes = ""
	

	for idx in range (0, length/8):
		byte=0
		for i in range(0,8):
			if(idx*8+i < length):
				byte=(byte<<1)+v[idx*8+i]
		bytes=bytes+chr(byte)

	payload_size=struct.unpack("i", bytes[:4])[0]
	return bytes[4:payload_size+4]

def extract(in_file,out_file,password): #extrair os dados que estão escondidos nos bits LSB's, do ficheiro de entrada 
	
	#processar a imagem em causa
	img=Image.open(in_file)
	(width,height)=img.size
	conv=img.convert("RGBA").getdata()
	


	#extrair os LSB's
	v=[]
	displacement=0

	for h in range(height):
		for w in range(width):
			if displacement<password:
				displacement=displacement+1
				continue
			(r,g,b,a)=conv.getpixel((w,h))
			v.append(r & 1)
			v.append(r>>1 & 1 )
			v.append(g & 1)
			v.append(g>>1 & 1 )
			v.append(b & 1)
			v.append(b>>1 & 1 )
	data_out=gather(v)

	out_f=open(out_file,"wb")
	out_f.write(data_out)
	out_f.close()

	print (" Informação extraída para %s." % out_file)
	
def usage(progName):

	print (" Informação extraída de imagens que sofreram esteganografia\n")
	print (" Como usar:")
	print (" %s <Input file> <output file> [password] " % progName)
	print (" The password is optional and must be a number ")
	sys.exit()
	
if __name__ == "__main__":
	if len(sys.argv)<2:
		usage(sys.argv[0])

	password = int(sys.argv[3])%13 if len(sys.argv)>3 else 0

	extract(sys.argv[1],sys.argv[2],password)

	
	
