// indented 2 times and used Prettier change later for good look
document.addEventListener("DOMContentLoaded", function () {
	// Use buttons to toggle between views
	document.querySelector("#inbox").addEventListener("click", () =>
		load_mailbox("inbox")
	);
	document.querySelector("#sent").addEventListener("click", () =>
		load_mailbox("sent")
	);
	document.querySelector("#archived").addEventListener("click", () =>
		load_mailbox("archive")
	);
	document.querySelector("#compose").addEventListener(
		"click",
		compose_email
	);
	// Add event listener to the form
	document.querySelector("#compose-form").addEventListener(
		"submit",
		send_email
	);
	// By default, load the inbox
	load_mailbox("inbox");
});

function send_email(event) {
	// Prevents reloading the page after submitting.
	event.preventDefault();

	// Get the required fields.
	const recipients = document.querySelector("#compose-recipients").value;
	const subject = document.querySelector("#compose-subject").value;
	const body = document.querySelector("#compose-body").value;

	// sending data ...copied from cs50 mail website official code for api doc
	fetch("/emails", {
		method: "POST",
		body: JSON.stringify({
			recipients: recipients,
			subject: subject,
			body: body,
		}),
	})
		// Take the return data and parse it in JSON format.
		.then((response) => response.json())
		.then((result) => {
			//Print result
			load_mailbox("sent", result);
			console.log(result);
		})
		.catch((error) => console.log(error));
}

function compose_email() {
	// Show compose view and hide other views
	document.querySelector("#emails-view").style.display = "none";
	document.querySelector("#email-view").style.display = "none";
	document.querySelector("#compose-view").style.display = "block";

	// Clear out composition fields
	document.querySelector("#compose-recipients").value = "";
	document.querySelector("#compose-subject").value = "";
	document.querySelector("#compose-body").value = "";
}

function load_mailbox(mailbox, message = "") {
	//removing messages
	document.querySelector("#div-message").textContent = "";

	// Print a message if any.
	if (message !== "") {
		make_alert(message);
	}

	// Show the mailbox and hide other views
	document.querySelector("#emails-view").style.display = "block";
	document.querySelector("#compose-view").style.display = "none";
	document.querySelector("#email-view").style.display = "none";

	// Show the mailbox name
	document.querySelector("#emails-view").innerHTML = `<h3>${
		mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
	}</h3>`;

	// Get data of the corresponding mailbox from the server.
	fetch(`/emails/${mailbox}`)
		.then((response) => response.json())
		.then((emails) => {
			emails.forEach((item) => {
				const parent_element = document.createElement(
					"div"
				);

				build_emails(item, parent_element, mailbox);

				parent_element.addEventListener("click", () =>
					read_email(item["id"])
				);
				document.querySelector(
					"#emails-view"
				).appendChild(parent_element);
			});
		})
		.catch((error) => console.error(error));
}

// Renders a bootstrap alert with parameter json object message The status message that the server returns
//primary blue
//success green
//dager red
//dark grey
//warning yellow
//info light aqua blue

function make_alert(message) {
	const element = document.createElement("div");
	element.classList.add("alert");

	if (message["message"]) {
		element.classList.add("alert-success");
		element.innerHTML = message["message"];
	} else if (message["error"]) {
		element.classList.add("alert-danger");
		element.innerHTML = message["error"];
	}

	document.querySelector("#div-message").appendChild(element);
}

// To change email div acc to data parameter json item return list Element parent_element The element that will be composed.
// trying return withouth anything ..
// works!!
function build_emails(item, parent_element, mailbox) {
	if (mailbox === "inbox" && item["archived"]) {
		return;
	} else if (mailbox === "archive" && !item["archived"]) {
		return;
	}

	const content = document.createElement("div");

	const recipients = document.createElement("strong");
	if (mailbox === "sent") {
		recipients.innerHTML = item["recipients"].join(", ") + " ";
	} else {
		recipients.innerHTML = item["sender"] + " ";
	}
	content.appendChild(recipients);

	content.innerHTML += item["subject"];

	// Set and style the date.
	const date = document.createElement("div");
	date.innerHTML = item["timestamp"];
	date.style.display = "inline-block";
	date.style.float = "right";

	if (item["read"]) {
		parent_element.style.backgroundColor = "grey";
		date.style.color = "black";
	} else {
		date.className = "text-muted";
	}
	content.appendChild(date);

	content.style.padding = "10px";
	parent_element.appendChild(content);

	// Style the parent element.
	parent_element.style.borderStyle = "solid";
	parent_element.style.borderWidth = "3px";
	parent_element.style.margin = "10px";
}

//read email function  using put method set it to read and change color
function read_email(id) {
	document.querySelector("#emails-view").style.display = "none";
	document.querySelector("#email-view").style.display = "block";

	// Erase any email that was here
	document.querySelector("#email-view").innerHTML = "";

	// Get the email's info and build the section.
	fetch(`/emails/${id}`)
		.then((response) => response.json())
		.then((result) => {
			build_email(result);
		})
		.catch((error) => console.log(error));

	// Set the email to read.
	fetch(`/emails/${id}`, {
		method: "PUT",
		body: JSON.stringify({
			read: true,
		}),
	});
}

//building and styling an email in accordance to a json object
//copying example from from  w3 color nearly dark
function build_email(data) {
	const from = document.createElement("div");
	const to = document.createElement("div");
	const subject = document.createElement("div");
	const timestamp = document.createElement("div");
	const reply_button = document.createElement("button");
	const archive_button = document.createElement("button");
	const body = document.createElement("div");

	from.innerHTML = `<strong>From: </strong> ${data["sender"]}`;
	to.innerHTML = `<strong>To: </strong> ${data["recipients"].join(", ")}`;
	subject.innerHTML = `<strong>Subject: </strong> ${data["subject"]}`;
	timestamp.innerHTML = `<strong>Timestamp: </strong> ${data["timestamp"]}`;
	body.innerHTML = data["body"];
	// refered to w3 and asked on discord for archive button
	//  Archive button
	archive_button.innerHTML =
		'<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-archive-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M12.643 15C13.979 15 15 13.845 15 12.5V5H1v7.5C1 13.845 2.021 15 3.357 15h9.286zM5.5 7a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1h-5zM.8 1a.8.8 0 0 0-.8.8V3a.8.8 0 0 0 .8.8h14.4A.8.8 0 0 0 16 3V1.8a.8.8 0 0 0-.8-.8H.8z"/></svg>  ';
	if (data["archived"]) {
		archive_button.innerHTML += "Unarchive";
	} else {
		archive_button.innerHTML += "Archive";
	}
	archive_button.classList = "btn btn-outline-primary m-2";
	archive_button.addEventListener("click", () => {
		archive_email(data);
		load_mailbox("inbox");
	});

	//  Reply button
	//  https://scipost-codebases.org/scipost/SciPost/-/blob/c38819531562a967094b435eacdede95a869db90/templates/bi/reply-fill.html for reply button code
	reply_button.innerHTML =
		'<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-reply-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M9.079 11.9l4.568-3.281a.719.719 0 0 0 0-1.238L9.079 4.1A.716.716 0 0 0 8 4.719V6c-1.5 0-6 0-7 8 2.5-4.5 7-4 7-4v1.281c0 .56.606.898 1.079.62z"/></svg>  Reply';
	//get class of the button can't modify only add and remove
	reply_button.classList = "btn btn-outline-primary m-2";
	reply_button.addEventListener("click", () => compose_reply(data));

	document.querySelector("#email-view").appendChild(from);
	document.querySelector("#email-view").appendChild(to);
	document.querySelector("#email-view").appendChild(subject);
	document.querySelector("#email-view").appendChild(timestamp);
	document.querySelector("#email-view").appendChild(archive_button);
	document.querySelector("#email-view").appendChild(reply_button);
	document.querySelector("#email-view").appendChild(
		document.createElement("hr")
	);
	document.querySelector("#email-view").appendChild(body);
}

// Creating archive using put method copied from api doc cs50

function archive_email(data) {
	fetch(`/emails/${data["id"]}`, {
		method: "PUT",
		body: JSON.stringify({
			archived: !data["archived"],
		}),
	});
}

// Loads the compose mailbox with  parameter  json data  of a certain email.

function compose_reply(data) {
	// Show compose view and hide other views
	document.querySelector("#emails-view").style.display = "none";
	document.querySelector("#email-view").style.display = "none";
	document.querySelector("#compose-view").style.display = "block";

	// Clear out composition fields
	document.querySelector("#compose-recipients").value = data["sender"];
	document.querySelector("#compose-subject").value = data[
		"subject"
	].match(/^(Re:)\s/)
		? data["subject"]
		: "Re: " + data["subject"];
	document.querySelector(
		"#compose-body"
	).value = `On ${data["timestamp"]} ${data["sender"]} wrote:\n${data["body"]}\n-------------------------------------\n`;
}
