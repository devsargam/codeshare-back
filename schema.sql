CREATE Table "user" (
	id SERIAL NOT NULL PRIMARY KEY,
	username VARCHAR(20) UNIQUE NOT NULL,
	password VARCHAR(400) NOT NULL,
	is_admin BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE TABLE "language"(
	 id SERIAL NOT NULL PRIMARY KEY,
	 name character varying(50) NOT NULL,
	 user_id INT NOT NULL,
	 FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE 
);

CREATE TABLE "code"(
	id SERIAL NOT NULL PRIMARY KEY,
	text text NOT NULL,
	language_id int NOT NULL,
	slug VARCHAR(10) NOT NULL UNIQUE,
	user_id int NOT NULL, 
	FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE,
	FOREIGN KEY (language_id) REFERENCES "language"(id) ON DELETE CASCADE
);