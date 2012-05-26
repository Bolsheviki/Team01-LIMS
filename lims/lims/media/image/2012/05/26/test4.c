struct A {
	int z;
	int g[10];

	struct B {
		int v;
		int u;
	} b;

};

struct D {
	int z;
	int m;
};

struct C {
	int s;

	int q[10];

	struct {
		int z;
		int m;
	} c;

};	


struct B f(struct C c[2][2]) {
	struct B b = c[1][0].c;
//	write(c[0][0].c.z);
//	write(c[0][1].c.z);
	write(c[1][0].c.z);
//	write(c[1][1].c.z);

	if ( c[1][0].c.z > 0 ) {
		struct A a[3][2];
		b.v = b.v - 1;
		a[1][0].b = b;
//		write(a[1][0].c.z);
		return f(a);

	} else if ( c[1][0].c.z < 0 ) {
		struct C a[3][2];
		b.v = b.v + 1;
		a[1][0].c = b;
		return f(a);

	} else {
		return b;
	}
}


int main() {
	struct A a[3][2][2];
	struct D d;
	a[2][1][0].b.v = read();
	d = f(a[2]);
	write(d.z);
}


