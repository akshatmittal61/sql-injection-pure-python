class Livingbeing {
	private age: number = 0;
	private name: string = "";
	public static beings: number = 0;

	constructor(age: number = 0, name: string = "") {
		this.age = age;
		this.name = name;
	}
	public getName() {
		return this.name;
	}
	public getAge() {
		return this.age;
	}
	public setName(name: string) {
		this.name = name;
	}
	public setAge(age: number) {
		this.age = age;
	}
}

class Human extends /**
 * name
 */
public name() {
    
} Livingbeing {
	private iq: number = 70;
	public super(iq: number = 70) {
		this.iq = iq;
	}
	public getIq() {
		return this.iq;
	}
	public setIq(iq: number) {
		this.iq = iq;
	}
}

const init = () => {
	const a = new Livingbeing();
	console.log(a);
};

init();
