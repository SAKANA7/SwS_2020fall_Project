#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
unsigned short s_box[] = { 0xe,0x4,0xd,0x1,0x2,0xf,0xb,0x8,0x3,0xa,0x6,0xc,0x5,0x9,0x0,0x7};
unsigned short decipher_s_box[] = {0xe, 0x3, 0x4, 0x8, 0x1, 0xc, 0xa, 0xf, 0x7, 0xd, 0x9, 0x6, 0xb, 0x2, 0x0, 0x5};
unsigned short p_box[] = {1,5,9,13,2,6,10,14,3,7,11,15,4,8,12,16};
void key_arrange(int i, unsigned int key, unsigned short* Kr);
void substitution(unsigned short Ur, unsigned short* Vr);//加密过程中的substitution
void decipher_substitution(unsigned short Vr, unsigned short* Ur);
void permutation(unsigned short Vr, unsigned short* Wr);
int encrypt(unsigned int key,unsigned short Wr);
void decipher(unsigned short Y,unsigned int key);//将密文最后1比特取反，解密后得到的明文。
int main() {
	int n,i;
	unsigned int key;
	unsigned short Wr, Y;//Y是密文,在decipher里解密
	scanf("%d",&n);
	for (i = 1; i <= n; i++) {
		scanf("%x", &key);
		scanf("%hx", &Wr);
		Y = encrypt(key, Wr);
		decipher(Y, key);
	}
	return 0;
}
/*加密部分*/
int encrypt(unsigned int key, unsigned short Wr) {
	unsigned short Ur = 0x0000, Vr = 0x0000,  Kr = 0x0000, Y = 0x0000;
	//Wr是步骤中的明文,r为0~4，当r=0，Wr为输入的明文，Y是输出的密文
	int i;
	for (i = 0; i < 3; i++) {
		key_arrange(i, key, &Kr);
		Ur = Kr ^ Wr;
		substitution(Ur, &Vr);
		permutation(Vr, &Wr);
	}
	key_arrange(3, key, &Kr);
	Ur = Kr ^ Wr;
	substitution(Ur, &Vr);
	key_arrange(4, key, &Kr);
	Y = Kr ^ Vr;
	printf("%04x ", Y);
	return Y;
}
/*取反&解密部分*/
//需要注意的是因为是逆过程，Vr,Wr,Ur在S盒和P盒的位置与加密过程恰好相反
void decipher(unsigned short Y, unsigned int key) {
	unsigned short Ur = 0x0000, Vr = 0x0000, Wr, X;//X是新解密的明文
	int i;
	unsigned short Kr[5];
	Y = Y ^ 0x0001;
	for (i = 0; i < 5; i++) {
		key_arrange(i, key, &Kr[i]);
	}//先存好五次的Kr
	Vr = Y ^ Kr[4];
	decipher_substitution(Vr, &Ur);
	Wr = Ur ^ Kr[3];
	for (i = 2; i >= 0; i--) {
		permutation(Wr, &Vr);
		decipher_substitution(Vr, &Ur);
		Wr = Ur ^ Kr[i];
	}
	X = Wr;
	printf("%04x\n", Wr);
}
/*密钥编排,其中i起始为0*/
void key_arrange(int i, unsigned int key, unsigned short* Kr) {
	unsigned int mask = 0xffff0000;
	mask = mask >> (4 * i);
	*Kr = (key & mask) >> (4 * (4 - i));
}
/*加密过程中的s_box代换*/
void substitution(unsigned short Ur, unsigned short* Vr) {
	unsigned short mask[] = { 0xf000,0x0f00,0x00f0,0x000f };
	unsigned short temp = 0x0000;//移位所需
	unsigned short v_temp = 0x0000;
	int flag;//角标
	int i = 0;
	for (i = 0; i < 4; i++) {
		temp = Ur & mask[i];
		flag = (int)(temp >> 4 * (3 - i));
		temp = s_box[flag] << 4 * (3 - i);
		v_temp = v_temp | temp;
	}
	*Vr = v_temp;
}
/*解密过程中的s_box代换*/
void decipher_substitution(unsigned short Vr, unsigned short* Ur) {
	unsigned short mask[] = { 0xf000,0x0f00,0x00f0,0x000f };
	unsigned short temp = 0x0000;//移位所需
	unsigned short u_temp = 0x0000;
	int flag;//角标
	int i = 0;
	for (i = 0; i < 4; i++) {
		temp = Vr & mask[i];
		flag = (int)(temp >> 4 * (3 - i));
		temp = decipher_s_box[flag] << 4 * (3 - i);
		u_temp = u_temp | temp;
	}
	*Ur = u_temp;

}
/*p_box置换*/
void permutation(unsigned short Vr, unsigned short* Wr) {
	int i = 0;
	unsigned int mask = 0x10000;
	unsigned short temp = 0x0000;//移位所需
	unsigned short w_temp = 0x0000;
	unsigned short flag_temp;//替换所需
	int flag;
	for (i = 0; i < 16; i++) {
		flag = p_box[i];
		mask = 0x10000 >> flag;
		flag_temp = (Vr & mask) >> (16 - flag);//把替换的移到最低位
		temp = flag_temp << (15 - i);//回到i
		w_temp = w_temp | temp;
	}
	*Wr = w_temp;
}