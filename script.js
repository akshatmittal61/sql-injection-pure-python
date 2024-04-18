const loginForm = document.querySelector("form.form-login");
const registerForm = document.querySelector("form.form-register");
const resetPasswordForm = document.querySelector("form.form-reset-password");
const deleteAccountForm = document.querySelector("form.form-delete-account");
const adminTable = document.querySelector("table#admin-table");

class HTTPClient {
	baseUrl = "http://localhost:8080/api";

	constructor(baseUrl) {
		this.baseUrl = baseUrl;
	}

	async get(endpoint) {
		try {
			const res = await fetch(`${this.baseUrl}/${endpoint}`);
			const response = await res.json();
			return Promise.resolve(response);
		} catch (error) {
			console.error("HTTP Client " + error);
			return Promise.reject(error);
		}
	}

	async post(endpoint, body) {
		try {
			const res = await fetch(`${this.baseUrl}/${endpoint}`, {
				method: "POST",
				body: JSON.stringify(body),
				headers: {
					"Content-Type": "application/json",
				},
			});
			const response = await res.json();
			return Promise.resolve(response);
		} catch (error) {
			console.error("HTTP Client " + error);
			return Promise.reject(error);
		}
	}

	async patch(endpoint, body) {
		try {
			const res = await fetch(`${this.baseUrl}/${endpoint}`, {
				method: "PATCH",
				body: JSON.stringify(body),
				headers: {
					"Content-Type": "application/json",
				},
			});
			const response = await res.json();
			return Promise.resolve(response);
		} catch (error) {
			console.error("HTTP Client " + error);
			return Promise.reject(error);
		}
	}

	async delete(endpoint, body) {
		try {
			const res = await fetch(`${this.baseUrl}/${endpoint}`, {
				method: "DELETE",
				body: JSON.stringify(body),
				headers: {
					"Content-Type": "application/json",
				},
			});
			const response = await res.json();
			return Promise.resolve(response);
		} catch (error) {
			console.error("HTTP Client " + error);
			return Promise.reject(error);
		}
	}
}

const http = new HTTPClient("http://localhost:8080/api");

const register = async (name, username, password) => {
	try {
		const res = await http.post("auth/register", {
			name,
			username,
			password,
		});
		if (!res.data) {
			throw res;
		}
		return Promise.resolve(res.data);
	} catch (error) {
		console.error(error);
		return Promise.reject(error);
	}
};

const login = async (username, password) => {
	try {
		const res = await http.post("auth/login", {
			username,
			password,
		});
		if (!res.data) {
			throw res;
		}
		return Promise.resolve(res.data);
	} catch (error) {
		console.error(error);
		return Promise.reject(error);
	}
};

const resetPassword = async (username, oldPassword, newPassword) => {
	try {
		const res = await http.patch("auth/reset-password", {
			username,
			oldPassword,
			newPassword,
		});
		if (!res.data) {
			throw res;
		}
		return Promise.resolve(res.data);
	} catch (error) {
		console.error(error);
		return Promise.reject(error);
	}
};

const deleteAccount = async (username, password) => {
	try {
		const res = await http.delete("auth/delete-account", {
			username,
			password,
		});
		if (!res.data) {
			throw res;
		}
		return Promise.resolve(res.data);
	} catch (error) {
		console.error(error);
		return Promise.reject(error);
	}
};

const getAllUsers = async () => {
	try {
		const res = await http.get("admin");
		if (!res.data) {
			throw res;
		}
		return Promise.resolve(res.data);
	} catch (error) {
		console.error(error);
		return Promise.reject(error);
	}
};

loginForm?.addEventListener("submit", async (e) => {
	e.preventDefault();
	const username = loginForm.querySelector("input#username").value;
	const password = loginForm.querySelector("input#password").value;
	try {
		const res = await login(username, password);
		document.querySelector(".response").innerHTML = JSON.stringify(res);
	} catch (error) {
		console.log(error.response);
		alert(error?.message ?? "Invalid credentials");
	}
});

registerForm?.addEventListener("submit", async (e) => {
	e.preventDefault();
	const name = registerForm.querySelector("input#name").value;
	const username = registerForm.querySelector("input#username").value;
	const password = registerForm.querySelector("input#password").value;
	try {
		const res = await register(name, username, password);
		document.querySelector(".response").innerHTML = JSON.stringify(res);
		alert("Registered Successfuly");
	} catch (error) {
		console.error(error);
		alert(error?.message ?? "Invalid credentials");
	}
});

resetPasswordForm?.addEventListener("submit", async (e) => {
	e.preventDefault();
	const username = resetPasswordForm.querySelector("input#username").value;
	const oldPassword =
		resetPasswordForm.querySelector("input#old-password").value;
	const newPassword =
		resetPasswordForm.querySelector("input#new-password").value;
	try {
		const res = await resetPassword(username, oldPassword, newPassword);
		document.querySelector(".response").innerHTML = JSON.stringify(res);
		alert("Updated password successfuly");
	} catch (error) {
		console.error(error);
		alert(error?.message ?? "Invalid credentials");
	}
});

deleteAccountForm?.addEventListener("submit", async (e) => {
	e.preventDefault();
	const username = deleteAccountForm.querySelector("input#username").value;
	const password = deleteAccountForm.querySelector("input#password").value;
	try {
		const res = await deleteAccount(username, password);
		document.querySelector(".response").innerHTML = JSON.stringify(res);
		alert("Deleted account successfuly");
	} catch (error) {
		console.log(error.response);
		alert(error?.message ?? "Invalid credentials");
	}
});

document.addEventListener("DOMContentLoaded", async () => {
	if (location.pathname === "/admin") {
		const tableBody = adminTable.querySelector("tbody");
		try {
			const users = await getAllUsers();
			users.forEach((user) => {
				const tr = document.createElement("tr");
				const td1 = document.createElement("td");
				td1.innerText = user[0];
				const td2 = document.createElement("td");
				td2.innerText = user[1];
				const td3 = document.createElement("td");
				td3.innerText = user[2];

				tr.appendChild(td1);
				tr.appendChild(td2);
				tr.appendChild(td3);

				tableBody.appendChild(tr);
			});
		} catch (error) {
			alert(error?.message ?? "Unable to load data");
		}
	}
});

document.querySelector("img.avatar")?.addEventListener("click", () => {
	window.location.href = "http://localhost:8080";
});
