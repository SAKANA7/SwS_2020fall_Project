#include<stdio.h>
int s_box[16] = {0xe,0x4,0xd,0x1,0x2,0xf,0xb,0x8,0x3,0xa,0x6,0xc,0x5,0x9,0x0,0x7};
int decipher_s_box[16] ={0xe, 0x3, 0x4, 0x8, 0x1, 0xc, 0xa, 0xf, 0x7, 0xd, 0x9, 0x6, 0xb, 0x2, 0x0, 0x5};

/*因为超时原因，参考同学的代码结构进行了重写*/
/*思路都是一致的，之前代码的不好之处在于指针过于混乱，函数调用过多，
倘若检查代码应该可以看到我的先前提交并对比*/
/*时间复杂度是一样的，
具体为什么在：构造测试样例相同输出结果相同的情况下无法通过测试点，怀疑是引用的问题
为什么之前最后一个测试点超时，怀疑是调用函数过多的问题*/

int encrypt(int x, unsigned int t) {
	unsigned int k[5];
	k[0] = t >> 16;
	k[1] = (t & 0x0ffff000) >> 12;
	k[2] = (t & 0xffff00) >> 8;
	k[3] = (t & 0xffff0) >> 4;
	k[4] = t & 0xffff;
	int a[4];


	for (int i = 0; i <= 2; i++) {
		x = x ^ k[i];
		//明文分段
		a[0] = (x & 0xf000) >> 12;
		a[1] = (x & 0xf00) >> 8;
		a[2] = (x & 0xf0) >> 4;
		a[3] = x & 0xf;

		//s_box
		for (int j = 0; j < 4; j++)
			a[j] = s_box[a[j]];

		//p_box
		x = ((a[0] & 0b1000) << 12) + ((a[1] & 0b1000) << 11) + ((a[2] & 0b1000) << 10) + ((a[3] & 0b1000) << 9) + ((a[0] & 0b100) << 9) + ((a[1] & 0b0100) << 8) + ((a[2] & 0b0100) << 7) + ((a[3] & 0b0100) << 6) + ((a[0] & 0b0010) << 6) + ((a[1] & 0b0010) << 5) + ((a[2] & 0b0010) << 4) + ((a[3] & 0b0010) << 3) + ((a[0] & 0b0001) << 3) + ((a[1] & 0b0001) << 2) + ((a[2] & 0b0001) << 1) + (a[3] & 0b0001);
	}

	x = x ^ k[3];
	a[0] = (x & 0xf000) >> 12;
	a[1] = (x & 0xf00) >> 8;
	a[2] = (x & 0xf0) >> 4;
	a[3] = x & 0xf;
	for (int j = 0; j < 4; j++)
		a[j] = s_box[a[j]];
	x = (a[0] << 12) + (a[1] << 8) + (a[2] << 4) + a[3];
	return (x ^ k[4]);
}

int decipher(int y, unsigned int t) {
	unsigned int k[5];
	k[4] = t >> 16;
	k[3] = (t & 0x0ffff000) >> 12;
	k[2] = (t & 0xffff00) >> 8;
	k[1] = (t & 0xffff0) >> 4;
	k[0] = t & 0xffff;

	y = y ^ k[0];
	int a[4];
	a[0] = (y & 0xf000) >> 12;
	a[1] = (y & 0xf00) >> 8;
	a[2] = (y & 0xf0) >> 4;
	a[3] = y & 0xf;
	for (int j = 0; j < 4; j++)
		a[j] = decipher_s_box[a[j]];
	y = (a[0] << 12) + (a[1] << 8) + (a[2] << 4) + a[3];
	y = y ^ k[1];

	//轮换
	for (int i = 2; i <= 4; i++) {
		//p置换的逆置换
		a[0] = ((y & 0x8000) >> 12) + ((y & 0x800) >> 9) + ((y & 0x80) >> 6) + ((y & 0x8) >> 3);
		a[1] = ((y & 0x4000) >> 11) + ((y & 0x400) >> 8) + ((y & 0x40) >> 5) + ((y & 0x4) >> 2);
		a[2] = ((y & 0x2000) >> 10) + ((y & 0x200) >> 7) + ((y & 0x20) >> 4) + ((y & 0x2) >> 1);
		a[3] = ((y & 0x1000) >> 9) + ((y & 0x100) >> 6) + ((y & 0x10) >> 3) + (y & 0x1);
		//s置换的逆置换
		for (int j = 0; j < 4; j++)
			a[j] = decipher_s_box[a[j]];
		y = (a[0] << 12) + (a[1] << 8) + (a[2] << 4) + a[3];
		y = y ^ k[i];
	}
	return y;
}
int main() {
	unsigned key;
	int x, y, n;
	scanf("%d", &n);
	for (int i = 0; i < n; i++) {
		scanf("%x%x", &key, &x);
		y = encrypt(x, key);
		printf("%04x ", y);
		y = y ^ 0x1;
		printf("%04x\n", decipher(y, key));
	}
	return 0;
}
